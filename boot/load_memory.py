#!/usr/bin/env python3
"""
本地记忆拼接器
读取 D:/KealanMemory 中的记忆文件，按加载顺序拼接为单一上下文文本。
用法：
  python load_memory.py                        # 只加载核心记忆
  python load_memory.py --project LabSOPGuard  # 加载核心 + 项目记忆
  python load_memory.py --project LabSOPGuard --full  # 追加 coding/env 规范
  python load_memory.py --list                 # 列出所有可用项目
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path("D:/KealanMemory")
MAP_FILE = ROOT / "boot/memory_map.json"
OUTPUT_FILE = ROOT / "boot/assembled_context.txt"


def load_map() -> dict:
    with open(MAP_FILE, encoding="utf-8") as f:
        return json.load(f)


def read_file(rel_path: str, project: str = "") -> str:
    """读取单个记忆文件，返回带标题分隔符的内容"""
    path = ROOT / rel_path.replace("{project}", project)
    if not path.exists():
        print(f"  [跳过] 文件不存在：{path}", file=sys.stderr)
        return ""
    content = path.read_text(encoding="utf-8").strip()
    separator = f"\n\n{'='*60}\n# 来源：{rel_path.replace('{project}', project)}\n{'='*60}\n"
    return separator + content


def assemble(project: str = "", full: bool = False) -> str:
    memory_map = load_map()
    chunks = []

    # 1. 核心记忆（必加载）
    print("加载核心记忆...")
    for rel_path in memory_map["default_load"]:
        chunk = read_file(rel_path)
        if chunk:
            chunks.append(chunk)
            print(f"  [ok] {rel_path}")

    # 2. 项目记忆（按需加载）
    if project:
        if project not in memory_map["projects"]:
            print(f"[警告] 项目 '{project}' 不在 memory_map.json 中，尝试继续加载...", file=sys.stderr)
        print(f"\n加载项目记忆：{project}...")
        for rel_path in memory_map["project_load"]:
            chunk = read_file(rel_path, project)
            if chunk:
                chunks.append(chunk)
                print(f"  [ok] {rel_path.replace('{project}', project)}")

    # 3. 可选规范（--full 时加载）
    if full:
        print("\n加载完整规范...")
        optional_rules = [
            p for p in memory_map["optional_load"]
            if not p.startswith("projects/")
        ]
        for rel_path in optional_rules:
            chunk = read_file(rel_path, project)
            if chunk:
                chunks.append(chunk)
                print(f"  [ok] {rel_path}")

    return "\n".join(chunks)


def main():
    parser = argparse.ArgumentParser(description="本地记忆拼接器")
    parser.add_argument("--project", "-p", default="", help="项目名称，如 LabSOPGuard")
    parser.add_argument("--full", "-f", action="store_true", help="追加完整规范（coding/env/project rules）")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有可用项目")
    parser.add_argument("--output", "-o", default=str(OUTPUT_FILE), help="输出文件路径")
    parser.add_argument("--print", action="store_true", help="直接打印到终端而不写文件")
    args = parser.parse_args()

    # 列出项目
    if args.list:
        memory_map = load_map()
        print("可用项目：")
        for p in memory_map["projects"]:
            if p != "_template":
                brief_path = ROOT / f"projects/{p}/project_brief.md"
                status = "[ok]" if brief_path.exists() else "[--]"
                print(f"  {status} {p}")
        return

    # 拼接记忆
    context = assemble(project=args.project, full=args.full)

    # 添加头部说明
    header = f"""# 个人记忆上下文（自动生成）
# 项目：{args.project or '（无）'}
# 加载模式：{'完整' if args.full else '标准'}
# 使用方式：将此文件内容粘贴给 Claude，或参考 boot/startup_prompt.md

"""
    full_output = header + context

    if args.print:
        print(full_output)
    else:
        output_path = Path(args.output)
        output_path.write_text(full_output, encoding="utf-8")
        size_kb = output_path.stat().st_size / 1024
        print(f"\n[ok] 已输出到：{output_path}（{size_kb:.1f} KB）")
        print(f"  直接复制文件内容粘贴给 Claude 即可。")


if __name__ == "__main__":
    main()
