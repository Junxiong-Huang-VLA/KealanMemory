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

MEMORY_ROOT = Path("D:/KealanMemory")
MAP_FILE = MEMORY_ROOT / "boot/memory_map.json"

# 核心记忆文件（每次必加载，保持轻量）
CORE_FILES = [
    "profile/identity.md",
    "profile/work_style.md",
    "profile/preferences.md",
    "operating_rules/communication_rules.md",
    "context/active_focus.md",
    "context/global_constraints.md",
]


def detect_project(cwd: str) -> str:
    """根据 cwd 自动匹配记忆系统中的项目名"""
    if not cwd:
        return ""
    cwd_lower = cwd.lower().replace("\\", "/")
    try:
        mem_map = json.loads(MAP_FILE.read_text(encoding="utf-8"))
        projects = mem_map.get("projects", [])
    except Exception:
        return ""
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
    lines = ["# [记忆系统自动加载]", ""]

    # 核心记忆
    for rel in CORE_FILES:
        content = read_file(rel)
        if content:
            lines.append(f"## {rel}")
            lines.append(content)
            lines.append("")

    # 项目记忆（若匹配到）
    if project:
        lines.append(f"## 当前项目：{project}")
        for fname in ["project_brief.md", "current_status.md", "constraints.md", "next_actions.md"]:
            rel = f"projects/{project}/{fname}"
            content = read_file(rel)
            if content:
                lines.append(f"### {fname}")
                lines.append(content)
                lines.append("")
        lines.append("---")
        lines.append(f"记忆已自动加载（项目：{project}）。直接开始工作，无需重复说明背景。")
    else:
        lines.append("---")
        lines.append("核心记忆已自动加载。如需加载项目记忆，输入 `/me 项目名`。")

    return "\n".join(lines)


def main():
    # 读取 hook 输入
    try:
        hook_input = json.loads(sys.stdin.read())
    except Exception:
        hook_input = {}

    cwd = hook_input.get("cwd", os.getcwd())
    source = hook_input.get("source", "startup")

    # resume 时不重复注入（已有上下文）
    if source == "resume":
        sys.exit(0)

    project = detect_project(cwd)
    context = build_context(project)
    print(context)
    sys.exit(0)


if __name__ == "__main__":
    main()
