#!/usr/bin/env python3
"""
SessionStart Hook — 对话开始时自动注入记忆到 Claude 上下文。
Claude Code 会把 stdout 内容追加进对话上下文，无需手动 /me。

输入：stdin 收到 JSON，包含 cwd / session_id / source 等字段
输出：stdout 输出记忆文本 → 自动注入 Claude 上下文
"""

import json
import os
import sys
from pathlib import Path


def find_memory_root() -> Path:
    env_root = os.environ.get("KEALAN_MEMORY_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


MEMORY_ROOT = find_memory_root()
MAP_FILE = MEMORY_ROOT / "boot/memory_map.json"
sys.path.insert(0, str(MEMORY_ROOT / "boot"))

try:
    from hook_logging import log_event, log_exception
except Exception:
    def log_event(*args, **kwargs):
        return None

    def log_exception(*args, **kwargs):
        return None


def load_map() -> dict:
    try:
        return json.loads(MAP_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def parse_hook_input() -> dict:
    if hasattr(sys.stdin, "buffer"):
        raw = sys.stdin.buffer.read().decode("utf-8-sig", errors="replace")
    else:
        raw = sys.stdin.read()
    starts = [idx for idx in (raw.find("{"), raw.find("[")) if idx >= 0]
    if starts:
        raw = raw[min(starts):]
    return json.loads(raw)


def detect_project(cwd: str) -> str:
    """根据 cwd 自动匹配记忆系统中的项目名"""
    if not cwd:
        return ""
    cwd_lower = cwd.lower().replace("\\", "/")
    projects = load_map().get("projects", [])
    for p in projects:
        if p == "_template":
            continue
        if p.lower() in cwd_lower:
            brief = MEMORY_ROOT / f"projects/{p}/project_brief.md"
            if brief.exists():
                return p
    return ""


def read_file(rel_path: str) -> str:
    path = MEMORY_ROOT / rel_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def build_context(project: str = "") -> str:
    mem_map = load_map()
    lines = ["# [记忆系统自动加载]", ""]

    # 核心记忆
    for rel in mem_map.get("default_load", []):
        content = read_file(rel)
        if content:
            lines.append(f"## {rel}")
            lines.append(content)
            lines.append("")

    # 项目记忆（若匹配到）
    if project:
        lines.append(f"## 当前项目：{project}")
        for rel_template in mem_map.get("project_load", []):
            rel = rel_template.replace("{project}", project)
            content = read_file(rel)
            if content:
                lines.append(f"### {Path(rel).name}")
                lines.append(content)
                lines.append("")
        lines.append("---")
        lines.append(f"记忆已自动加载（项目：{project}）。直接开始工作，无需重复说明背景。")
    else:
        lines.append("---")
        lines.append("核心记忆已自动加载。如需加载项目记忆，输入 `/me 项目名`。")

    return "\n".join(lines)


def load_summary(project: str = "") -> dict:
    mem_map = load_map()
    default_files = [rel for rel in mem_map.get("default_load", []) if (MEMORY_ROOT / rel).exists()]
    project_files = []
    if project:
        for rel_template in mem_map.get("project_load", []):
            rel = rel_template.replace("{project}", project)
            if (MEMORY_ROOT / rel).exists():
                project_files.append(rel)
    return {
        "default_file_count": len(default_files),
        "project_file_count": len(project_files),
        "default_files": [Path(rel).name for rel in default_files],
        "project_files": [Path(rel).name for rel in project_files],
    }


def main():
    try:
        # 读取 hook 输入
        try:
            hook_input = parse_hook_input()
        except Exception as exc:
            log_exception("session_start", "parse_input", exc)
            hook_input = {}

        cwd = hook_input.get("cwd", os.getcwd())
        source = hook_input.get("source", "startup")

        # resume 时不重复注入（已有上下文）
        if source == "resume":
            log_event("session_start", "skip", source=source)
            sys.exit(0)

        project = detect_project(cwd)
        log_event("session_start", "project_detected", project=project or None, cwd=cwd)
        context = build_context(project)
        log_event(
            "session_start",
            "load_summary",
            project=project or None,
            output_chars=len(context),
            **load_summary(project),
        )
        print(context)
    except Exception as exc:
        log_exception("session_start", "hook_failed", exc)
    sys.exit(0)


if __name__ == "__main__":
    main()
