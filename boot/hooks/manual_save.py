#!/usr/bin/env python3
"""
手动收工脚本 — 在任何终端运行，交互式记录本次工作进展并写回记忆系统。
用法：python D:/KealanMemory/boot/hooks/manual_save.py
"""

import io
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Windows 终端用系统编码（GBK/UTF-8），统一用系统默认避免 surrogate 问题
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=sys.stdout.encoding or "utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding=sys.stderr.encoding or "utf-8", errors="replace")
    if not sys.stdin.isatty():
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding=sys.getdefaultencoding(), errors="replace")

MEMORY_ROOT = Path("D:/KealanMemory")
MAP_FILE = MEMORY_ROOT / "boot/memory_map.json"


def detect_project(cwd: str) -> str:
    cwd_lower = cwd.lower().replace("\\", "/")
    try:
        mem_map = json.loads(MAP_FILE.read_text(encoding="utf-8"))
        for p in mem_map.get("projects", []):
            if p == "_template":
                continue
            if p.lower() in cwd_lower:
                if (MEMORY_ROOT / f"projects/{p}/current_status.md").exists():
                    return p
    except Exception:
        pass
    return ""


def ask(prompt: str) -> str:
    print(prompt, end=" ", flush=True)
    return input().strip()


def write_memory(project: str, completed: list, next_actions: list):
    today = datetime.now().strftime("%Y-%m-%d %H:%M")

    # current_status.md
    if project:
        status_file = MEMORY_ROOT / f"projects/{project}/current_status.md"
        if status_file.exists():
            content = status_file.read_text(encoding="utf-8", errors="replace")
            block = f"\n\n## 最近一次更新\n\n- **时间**：{today}\n- **做了什么**：\n"
            for item in completed:
                block += f"  - {item}\n"
            if "## 最近一次更新" in content:
                idx = content.index("## 最近一次更新")
                content = content[:idx].rstrip() + block
            else:
                content = content.rstrip() + block
            status_file.write_text(content, encoding="utf-8", errors="replace")
            print(f"  [ok] {status_file}")

    # next_actions.md
    if project and next_actions:
        actions_file = MEMORY_ROOT / f"projects/{project}/next_actions.md"
        if actions_file.exists():
            content = actions_file.read_text(encoding="utf-8", errors="replace")
            block = f"## 立即要做（更新于 {today}）\n\n"
            for i, item in enumerate(next_actions, 1):
                block += f"{i}. {item}\n"
            if "## 立即要做" in content:
                idx = content.index("## 立即要做")
                # 找下一个 ## 标题的位置
                rest = content[idx:]
                next_h2 = re.search(r"\n## ", rest[3:])
                if next_h2:
                    end = idx + 3 + next_h2.start()
                    content = content[:idx] + block + "\n" + content[end:]
                else:
                    content = content[:idx] + block
            else:
                content = block + "\n" + content
            actions_file.write_text(content, encoding="utf-8", errors="replace")
            print(f"  [ok] {actions_file}")

    # active_focus.md
    focus_file = MEMORY_ROOT / "context/active_focus.md"
    if focus_file.exists():
        content = focus_file.read_text(encoding="utf-8", errors="replace")
        block = f"## 上次工作摘要（{today}）\n\n"
        if project:
            block += f"**项目**：{project}\n\n"
        for item in completed:
            block += f"- {item}\n"
        if "## 上次工作摘要" in content:
            idx = content.index("## 上次工作摘要")
            content = content[:idx].rstrip() + "\n\n" + block
        else:
            content = content.rstrip() + "\n\n" + block
        focus_file.write_text(content, encoding="utf-8", errors="replace")
        print(f"  [ok] {focus_file}")


def main():
    cwd = os.getcwd()
    project = detect_project(cwd)

    print("\n========== 收工记录 ==========")
    if project:
        print(f"检测到项目：{project}")
    else:
        project = ask("未检测到项目，请输入项目名（回车跳过）：")

    print("\n本次完成了什么？每行一条，空行结束：")
    completed = []
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
        return

    print("\n下次要做什么？每行一条，空行结束：")
    next_actions = []
    while True:
        try:
            line = input("  > ").strip()
        except EOFError:
            break
        if not line:
            break
        next_actions.append(line)

    print("\n写入记忆...")
    write_memory(project, completed, next_actions)
    print("\n收工完成。")


if __name__ == "__main__":
    main()
