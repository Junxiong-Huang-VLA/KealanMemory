#!/usr/bin/env python3
"""Assemble local memory files into one context document."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from history_search import format_history_context, resolve_history
from memory_loader import default_output_path, memory_map_path, resolve_root


ROOT = resolve_root(__file__)
MAP_FILE = memory_map_path(ROOT)
OUTPUT_FILE = default_output_path(ROOT)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def load_map() -> dict:
    with MAP_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def read_file(rel_path: str, project: str = "", *, optional: bool = False) -> str:
    """Read one memory file and return it with a source separator."""
    display_path = rel_path.replace("{project}", project)
    path = ROOT / display_path
    if not path.exists():
        if not optional:
            print(f"  [skip] Missing file: {path}", file=sys.stderr)
        return ""

    content = path.read_text(encoding="utf-8").strip()
    separator = f"\n\n{'=' * 60}\n# Source: {display_path}\n{'=' * 60}\n"
    return separator + content


def optional_paths(memory_map: dict, project: str) -> list[str]:
    paths: list[str] = []
    for rel_path in memory_map.get("optional_load", []):
        is_project_path = rel_path.startswith("projects/")
        if is_project_path and not project:
            continue
        paths.append(rel_path)
    return paths


def assemble(project: str = "", full: bool = False, history: list[str] | None = None) -> str:
    memory_map = load_map()
    chunks: list[str] = []

    print(f"Memory root: {ROOT}")
    print("Loading core memory...")
    for rel_path in memory_map.get("default_load", []):
        chunk = read_file(rel_path)
        if chunk:
            chunks.append(chunk)
            print(f"  [ok] {rel_path}")

    if project:
        if project not in memory_map.get("projects", []):
            print(
                f"[warning] Project '{project}' is not listed in memory_map.json; trying to load it anyway.",
                file=sys.stderr,
            )
        print(f"\nLoading project memory: {project}...")
        for rel_path in memory_map.get("project_load", []):
            chunk = read_file(rel_path, project)
            if chunk:
                chunks.append(chunk)
                print(f"  [ok] {rel_path.replace('{project}', project)}")

    if full:
        print("\nLoading optional memory...")
        for rel_path in optional_paths(memory_map, project):
            chunk = read_file(rel_path, project, optional=True)
            if chunk:
                chunks.append(chunk)
                print(f"  [ok] {rel_path.replace('{project}', project)}")

    for item in history or []:
        print(f"\nLoading history memory: {item}...")
        try:
            matches = resolve_history(item, root=ROOT, limit=5)
        except ValueError as exc:
            print(f"  [error] {exc}", file=sys.stderr)
            continue
        if not matches:
            print(f"  [miss] No history matched: {item}", file=sys.stderr)
            continue
        chunks.append(format_history_context(matches))
        for match in matches:
            rel = match.path.relative_to(ROOT) if match.path.is_relative_to(ROOT) else match.path
            print(f"  [ok] {rel}")

    return "\n".join(chunks)


def main() -> None:
    parser = argparse.ArgumentParser(description="Local memory assembler")
    parser.add_argument("--project", "-p", default="", help="Project name, for example LabSOPGuard")
    parser.add_argument("--full", "-f", action="store_true", help="Also load optional global and project memory")
    parser.add_argument("--history", action="append", default=[], help="Append matching context/history file by keyword or file path")
    parser.add_argument("--list", "-l", action="store_true", help="List available projects")
    parser.add_argument("--output", "-o", default=str(OUTPUT_FILE), help="Output file path")
    parser.add_argument("--print", action="store_true", help="Print to stdout instead of writing a file")
    args = parser.parse_args()

    if args.list:
        memory_map = load_map()
        print(f"Memory root: {ROOT}")
        print("Available projects:")
        for project in memory_map.get("projects", []):
            if project == "_template":
                continue
            brief_path = ROOT / "projects" / project / "project_brief.md"
            status = "[ok]" if brief_path.exists() else "[--]"
            print(f"  {status} {project}")
        return

    context = assemble(project=args.project, full=args.full, history=args.history)
    mode = "full" if args.full else "standard"
    project_name = args.project or "(none)"
    history_name = ", ".join(args.history) if args.history else "(none)"
    header = f"""# Personal Memory Context (generated)
# Project: {project_name}
# Load mode: {mode}
# History: {history_name}
# Usage: paste this file into Claude, or see boot/startup_prompt.md

"""
    full_output = header + context

    if args.print:
        print(full_output)
        return

    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(full_output, encoding="utf-8")
    size_kb = output_path.stat().st_size / 1024
    print(f"\n[ok] Wrote output to: {output_path} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
