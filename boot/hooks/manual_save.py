#!/usr/bin/env python3
"""Manual memory save hook/script with best-effort redacted logging."""

from __future__ import annotations

import io
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=sys.stdout.encoding or "utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding=sys.stderr.encoding or "utf-8", errors="replace")
    if not sys.stdin.isatty():
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding=sys.getdefaultencoding(), errors="replace")


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


SYNC_PATHS = ("context", "projects")
SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?:API_KEY|AUTH_TOKEN|SECRET)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,}", re.I),
)


def detect_project(cwd: str) -> str:
    cwd_lower = cwd.lower().replace("\\", "/")
    try:
        mem_map = json.loads(MAP_FILE.read_text(encoding="utf-8"))
        for project in mem_map.get("projects", []):
            if project == "_template":
                continue
            if project.lower() in cwd_lower:
                if (MEMORY_ROOT / "projects" / project / "current_status.md").exists():
                    return project
    except Exception:
        pass
    return ""


def ask(prompt: str) -> str:
    print(prompt, end=" ", flush=True)
    return input().strip()


def _replace_or_append_section(content: str, heading: str, block: str, keep_following_sections: bool = False) -> str:
    if heading not in content:
        return content.rstrip() + "\n\n" + block
    idx = content.index(heading)
    if keep_following_sections:
        rest = content[idx:]
        next_h2 = re.search(r"\n## ", rest[3:])
        if next_h2:
            end = idx + 3 + next_h2.start()
            return content[:idx].rstrip() + "\n\n" + block.rstrip() + "\n\n" + content[end:].lstrip()
    return content[:idx].rstrip() + "\n\n" + block


def write_memory(project: str, completed: list[str], next_actions: list[str]) -> dict:
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    written_files: list[str] = []

    if project:
        project_dir = MEMORY_ROOT / "projects" / project
        status_file = project_dir / "current_status.md"
        if status_file.exists():
            content = status_file.read_text(encoding="utf-8", errors="replace")
            block = f"## 最近一次更新\n\n- **时间**：{today}\n- **做了什么**：\n"
            for item in completed:
                block += f"  - {item}\n"
            content = _replace_or_append_section(content, "## 最近一次更新", block)
            status_file.write_text(content, encoding="utf-8", errors="replace")
            print(f"  [ok] {status_file}")
            written_files.append(str(status_file.relative_to(MEMORY_ROOT)))

        if next_actions:
            actions_file = project_dir / "next_actions.md"
            if actions_file.exists():
                content = actions_file.read_text(encoding="utf-8", errors="replace")
                block = f"## 立即要做（更新于 {today}）\n\n"
                for index, item in enumerate(next_actions, 1):
                    block += f"{index}. {item}\n"
                content = _replace_or_append_section(content, "## 立即要做", block, keep_following_sections=True)
                actions_file.write_text(content, encoding="utf-8", errors="replace")
                print(f"  [ok] {actions_file}")
                written_files.append(str(actions_file.relative_to(MEMORY_ROOT)))

    focus_file = MEMORY_ROOT / "context/active_focus.md"
    if focus_file.exists():
        content = focus_file.read_text(encoding="utf-8", errors="replace")
        block = f"## 上次工作摘要（{today}）\n\n"
        if project:
            block += f"**项目**：{project}\n\n"
        for item in completed:
            block += f"- {item}\n"
        content = _replace_or_append_section(content, "## 上次工作摘要", block)
        focus_file.write_text(content, encoding="utf-8", errors="replace")
        print(f"  [ok] {focus_file}")
        written_files.append(str(focus_file.relative_to(MEMORY_ROOT)))

    return {
        "status": "written" if written_files else "skipped",
        "written_file_count": len(written_files),
        "written_files": written_files,
    }


def contains_secret(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return False
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


def sync_memory_changes() -> dict:
    if os.environ.get("KEALAN_MEMORY_AUTO_COMMIT") != "1":
        print("Skipping Git sync: set KEALAN_MEMORY_AUTO_COMMIT=1 to auto-commit.")
        return {"status": "skipped", "reason": "auto_commit_disabled"}

    checked_files: list[Path] = []
    for rel in SYNC_PATHS:
        base = MEMORY_ROOT / rel
        if base.exists():
            checked_files.extend(path for path in base.rglob("*") if path.is_file())

    leaked = [path for path in checked_files if contains_secret(path)]
    if leaked:
        print("Possible secret detected; Git sync cancelled.")
        for path in leaked[:10]:
            print(f"  [secret?] {path}")
        return {"status": "skipped", "reason": "secret_scan_blocked", "secret_hit_count": len(leaked)}

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        subprocess.run(["git", "add", *SYNC_PATHS], cwd=MEMORY_ROOT, check=True)
        diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=MEMORY_ROOT, capture_output=True)
        if diff.returncode == 0:
            print("No memory changes to commit.")
            return {"status": "skipped", "reason": "no_changes"}
        subprocess.run(["git", "commit", "-m", f"sync memory: {date_str}"], cwd=MEMORY_ROOT, check=True)
        pushed = False
        if os.environ.get("KEALAN_MEMORY_AUTO_PUSH") == "1":
            subprocess.run(["git", "push"], cwd=MEMORY_ROOT, check=True)
            pushed = True
            print("Memory committed and pushed.")
        else:
            print("Memory committed. Set KEALAN_MEMORY_AUTO_PUSH=1 to push automatically.")
        return {"status": "committed", "pushed": pushed}
    except subprocess.CalledProcessError:
        print("Git sync failed.")
        return {"status": "failed", "reason": "git_command_failed"}


def main() -> None:
    try:
        cwd = os.getcwd()
        project = detect_project(cwd)
        log_event("manual_save", "project_detected", project=project or None, cwd=cwd)

        print("\n========== 收工记录 ==========")
        if project:
            print(f"检测到项目：{project}")
        else:
            project = ask("未检测到项目，请输入项目名（回车跳过）：")
            log_event("manual_save", "project_entered", project=project or None)

        print("\n本次完成了什么？每行一条，空行结束：")
        completed: list[str] = []
        while True:
            try:
                line = input("  > ").strip()
            except EOFError:
                break
            if not line:
                break
            completed.append(line)

        if not completed:
            print("没有输入内容，已取消。")
            log_event("manual_save", "skip", reason="empty_completed", project=project or None)
            return

        print("\n下次要做什么？每行一条，空行结束：")
        next_actions: list[str] = []
        while True:
            try:
                line = input("  > ").strip()
            except EOFError:
                break
            if not line:
                break
            next_actions.append(line)

        print("\n写入记忆...")
        write_status = write_memory(project, completed, next_actions)
        log_event(
            "manual_save",
            "writeback",
            project=project or None,
            completed_count=len(completed),
            next_action_count=len(next_actions),
            **write_status,
        )

        print("处理 Git 同步...")
        sync_status = sync_memory_changes()
        log_event("manual_save", "git_sync", project=project or None, **sync_status)
        print("\n收工完成，记忆已保存。")
    except Exception as exc:
        log_exception("manual_save", "hook_failed", exc)
        print(f"收工记录失败：{exc}")


if __name__ == "__main__":
    main()
