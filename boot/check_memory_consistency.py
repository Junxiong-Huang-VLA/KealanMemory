#!/usr/bin/env python3
"""Read-only health checks for KealanMemory."""

from __future__ import annotations

import json
import os
import py_compile
import re
import subprocess
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - exercised only when dependency is absent.
    Draft202012Validator = None


ROOT = Path(os.environ.get("KEALAN_MEMORY_ROOT", Path(__file__).resolve().parents[1])).resolve()
SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?:API_KEY|AUTH_TOKEN|SECRET)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,}", re.I),
)
TEXT_SUFFIXES = {".bat", ".css", ".html", ".json", ".md", ".ps1", ".py", ".txt", ".yaml", ".yml"}
IGNORED_DIRS = {".git", "__pycache__"}
IGNORED_FILES = {
    ROOT / "boot" / "assembled_context.txt",
    ROOT / "boot" / "check_memory_consistency.py",
    ROOT / "OPTIMIZATION_TASKBOOK.md",
}
REQUIRED_PROJECT_FILES = {
    "project_brief.md",
    "current_status.md",
    "constraints.md",
    "next_actions.md",
}
SCHEMA_TARGETS = {
    "boot/memory_map.json": "schemas/memory_map.schema.json",
    "boot/routing_map.json": "schemas/routing_map.schema.json",
}
FRONTMATTER_SCHEMA_TARGETS = {
    "roles": "schemas/role_frontmatter.schema.json",
    "skills": "schemas/skill_frontmatter.schema.json",
}


class Report:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.warnings: list[str] = []

    def ok(self, message: str) -> None:
        print(f"[ok] {message}")

    def warn(self, message: str) -> None:
        self.warnings.append(message)
        print(f"[warn] {message}")

    def fail(self, message: str) -> None:
        self.failures.append(message)
        print(f"[fail] {message}")


def iter_text_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if path in IGNORED_FILES:
            continue
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            files.append(path)
    return files


def parse_frontmatter(text: str) -> dict:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break
    if end_index is None:
        return {}

    meta: dict[str, object] = {}
    current_list_key: str | None = None
    for raw_line in lines[1:end_index]:
        if not raw_line.strip():
            continue
        stripped = raw_line.strip()
        if stripped.startswith("- ") and current_list_key:
            existing = meta.setdefault(current_list_key, [])
            if isinstance(existing, list):
                existing.append(unquote_scalar(stripped[2:].strip()))
            continue
        if raw_line[:1].isspace() or ":" not in raw_line:
            current_list_key = None
            continue

        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value:
            meta[key] = unquote_scalar(value)
            current_list_key = None
        else:
            meta[key] = []
            current_list_key = key
    return meta


def unquote_scalar(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def check_json(report: Report) -> dict:
    memory_map: dict = {}
    for path in [ROOT / "boot/memory_map.json", ROOT / "install/claude_settings.json"]:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            report.ok(f"JSON 可解析：{path.relative_to(ROOT)}")
            if path.name == "memory_map.json":
                memory_map = data
        except Exception as exc:
            report.fail(f"JSON 解析失败：{path.relative_to(ROOT)} ({exc})")
    return memory_map


def check_json_schemas(report: Report) -> None:
    if Draft202012Validator is None:
        report.fail("jsonschema dependency is missing; install requirements.txt")
        return

    for instance_rel, schema_rel in SCHEMA_TARGETS.items():
        instance_path = ROOT / instance_rel
        schema_path = ROOT / schema_rel
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            instance = json.loads(instance_path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            errors = sorted(
                Draft202012Validator(schema).iter_errors(instance),
                key=lambda error: list(error.absolute_path),
            )
        except Exception as exc:
            report.fail(f"Schema validation setup failed: {instance_rel} ({exc})")
            continue

        if errors:
            first_errors = "; ".join(error.message for error in errors[:5])
            report.fail(f"Schema validation failed: {instance_rel} ({first_errors})")
        else:
            report.ok(f"Schema validation passed: {instance_rel}")


def validate_with_schema(report: Report, instance: dict, schema_rel: str, label: str) -> bool:
    if Draft202012Validator is None:
        report.fail("jsonschema dependency is missing; install requirements.txt")
        return False

    try:
        schema = json.loads((ROOT / schema_rel).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        errors = sorted(
            Draft202012Validator(schema).iter_errors(instance),
            key=lambda error: list(error.absolute_path),
        )
    except Exception as exc:
        report.fail(f"Schema validation setup failed: {label} ({exc})")
        return False

    if errors:
        first_errors = "; ".join(error.message for error in errors[:5])
        report.fail(f"Schema validation failed: {label} ({first_errors})")
        return False
    return True


def check_python(report: Report) -> None:
    for directory in ["boot", "install", "web"]:
        for path in (ROOT / directory).rglob("*.py"):
            try:
                py_compile.compile(str(path), doraise=True)
            except Exception as exc:
                report.fail(f"Python 编译失败：{path.relative_to(ROOT)} ({exc})")
    report.ok("Python 文件编译检查完成")


def check_powershell(report: Report) -> None:
    ps_files = [ROOT / "boot/load_memory.ps1"]
    for path in ps_files:
        command = (
            "$tokens=$null; $errors=$null; "
            f"[System.Management.Automation.Language.Parser]::ParseFile('{path}', [ref]$tokens, [ref]$errors) > $null; "
            "if ($errors.Count -gt 0) { $errors | ForEach-Object { $_.Message }; exit 1 }"
        )
        result = subprocess.run(["powershell", "-NoProfile", "-Command", command], capture_output=True, text=True)
        if result.returncode == 0:
            report.ok(f"PowerShell 可解析：{path.relative_to(ROOT)}")
        else:
            report.fail(f"PowerShell 解析失败：{path.relative_to(ROOT)} ({result.stdout.strip() or result.stderr.strip()})")


def check_path_and_secret_scan(report: Report) -> None:
    drift_hits: list[str] = []
    secret_hits: list[str] = []
    for path in iter_text_files():
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        rel = str(path.relative_to(ROOT))
        if "D:/ClaudeMemory" in text or "D:\\ClaudeMemory" in text:
            drift_hits.append(rel)
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            secret_hits.append(rel)
    if drift_hits:
        report.fail("发现旧路径引用：" + ", ".join(drift_hits[:10]))
    else:
        report.ok("未发现 D:/ClaudeMemory 旧路径引用")
    if secret_hits:
        report.fail("发现疑似密钥：" + ", ".join(secret_hits[:10]))
    else:
        report.ok("未发现疑似密钥")


def check_projects(report: Report, memory_map: dict) -> None:
    projects = [p for p in memory_map.get("projects", []) if p != "_template"]
    if not projects:
        report.warn("memory_map.json 未注册真实项目")
        return
    for project in projects:
        base = ROOT / "projects" / project
        if not base.exists():
            report.fail(f"项目已注册但目录不存在：{project}")
            continue
        missing = [name for name in REQUIRED_PROJECT_FILES if not (base / name).exists()]
        if missing:
            report.fail(f"项目缺少必需文件：{project} ({', '.join(missing)})")
    report.ok(f"项目索引检查完成：{len(projects)} 个项目")


def check_frontmatter(report: Report) -> tuple[set[str], set[str]]:
    skill_ids: set[str] = set()
    role_ids: set[str] = set()
    for folder, ids in [("skills", skill_ids), ("roles", role_ids)]:
        schema_rel = FRONTMATTER_SCHEMA_TARGETS[folder]
        for path in sorted((ROOT / folder).glob("*.md")):
            meta = parse_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
            missing = [key for key in ("id", "name", "category", "description") if key not in meta]
            if missing:
                report.fail(f"{folder} frontmatter 缺字段：{path.name} ({', '.join(missing)})")
            validate_with_schema(report, meta, schema_rel, f"{folder}/{path.name}")
            ids.add(meta.get("id", path.stem))
            if folder == "roles" and meta.get("slug"):
                ids.add(meta["slug"])
    report.ok(f"frontmatter 检查完成：{len(skill_ids)} skills, {len(role_ids)} roles")
    return skill_ids, role_ids


def check_routing(report: Report, skill_ids: set[str], role_ids: set[str]) -> None:
    route_path = ROOT / "boot/routing_map.json"
    if not route_path.exists():
        report.warn("未找到 boot/routing_map.json")
        return
    try:
        routes = json.loads(route_path.read_text(encoding="utf-8"))
    except Exception as exc:
        report.fail(f"routing_map.json 解析失败：{exc}")
        return
    route_items = routes.get("routes") or routes.get("intents") or []
    for item in route_items:
        for skill in item.get("skills", []):
            if skill not in skill_ids:
                report.fail(f"routing skill 不存在：{skill}")
        role = item.get("role")
        if role and role not in role_ids:
            report.fail(f"routing role 不存在：{role}")
    report.ok(f"routing map 检查完成：{len(route_items)} 条路由")


def main() -> int:
    report = Report()
    print(f"KealanMemory health check: {ROOT}")
    memory_map = check_json(report)
    check_json_schemas(report)
    check_python(report)
    check_powershell(report)
    check_path_and_secret_scan(report)
    check_projects(report, memory_map)
    skill_ids, role_ids = check_frontmatter(report)
    check_routing(report, skill_ids, role_ids)
    print(f"\nSummary: {len(report.failures)} failed, {len(report.warnings)} warnings")
    return 1 if report.failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
