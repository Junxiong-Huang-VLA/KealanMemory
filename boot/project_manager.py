#!/usr/bin/env python3
"""Project lifecycle CLI for local memory projects."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

try:
    from memory_loader import memory_map_path, resolve_root
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from memory_loader import memory_map_path, resolve_root


ROOT = resolve_root(__file__)
REQUIRED_PROJECT_FILES = (
    "project_brief.md",
    "current_status.md",
    "constraints.md",
    "next_actions.md",
)
SAFE_PROJECT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,79}$")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def load_map(root: Path) -> dict:
    path = memory_map_path(root)
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def write_map(root: Path, memory_map: dict) -> None:
    path = memory_map_path(root)
    path.write_text(json.dumps(memory_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_project_name(name: str) -> None:
    if not SAFE_PROJECT_RE.fullmatch(name):
        raise ValueError("Project name must use letters, numbers, underscore, or hyphen and cannot contain path separators.")
    if name == "_template":
        raise ValueError("_template is reserved.")


def registered_projects(memory_map: dict) -> list[str]:
    return [p for p in memory_map.get("projects", []) if p != "_template"]


def set_project_registered(memory_map: dict, name: str, present: bool) -> None:
    projects = [p for p in memory_map.get("projects", []) if p != name and p != "_template"]
    if present:
        projects.append(name)
    projects = sorted(dict.fromkeys(projects), key=str.lower)
    if "_template" in memory_map.get("projects", []):
        projects.append("_template")
    memory_map["projects"] = projects


def copy_template(root: Path, name: str) -> None:
    source = root / "projects" / "_template"
    target = root / "projects" / name
    if not source.exists():
        raise FileNotFoundError(f"Template project not found: {source}")
    shutil.copytree(source, target)


def command_create(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve()
    validate_project_name(args.name)
    target = root / "projects" / args.name
    memory_map = load_map(root)

    if target.exists():
        print(f"[error] Project directory already exists: {target}", file=sys.stderr)
        return 1
    if args.name in registered_projects(memory_map):
        print(f"[error] Project already registered: {args.name}", file=sys.stderr)
        return 1

    if args.dry_run:
        print(f"[dry-run] Would create {target}")
        print(f"[dry-run] Would register {args.name} in boot/memory_map.json")
        return 0

    copy_template(root, args.name)
    set_project_registered(memory_map, args.name, True)
    write_map(root, memory_map)
    print(f"[ok] Created project: {args.name}")
    return 0


def command_list(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve()
    memory_map = load_map(root)
    print(f"Memory root: {root}")
    print("Active projects:")
    for name in registered_projects(memory_map):
        base = root / "projects" / name
        status = "[ok]" if base.exists() else "[missing]"
        print(f"  {status} {name}")

    if args.archived:
        archive_root = root / "archive" / "old_projects"
        print("Archived projects:")
        if not archive_root.exists():
            print("  [--] none")
        else:
            archived = sorted(p for p in archive_root.iterdir() if p.is_dir())
            if not archived:
                print("  [--] none")
            for path in archived:
                print(f"  [ok] {path.name}")
    return 0


def archive_target(root: Path, name: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    base = root / "archive" / "old_projects" / f"{name}-{timestamp}"
    target = base
    counter = 1
    while target.exists():
        counter += 1
        target = Path(f"{base}-{counter}")
    return target


def command_archive(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve()
    validate_project_name(args.name)
    source = root / "projects" / args.name
    memory_map = load_map(root)

    if not source.exists():
        print(f"[error] Project directory not found: {source}", file=sys.stderr)
        return 1
    target = archive_target(root, args.name)

    if args.dry_run:
        print(f"[dry-run] Would move {source} -> {target}")
        print(f"[dry-run] Would unregister {args.name} from boot/memory_map.json")
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(target))
    set_project_registered(memory_map, args.name, False)
    write_map(root, memory_map)
    print(f"[ok] Archived project: {args.name} -> {target.relative_to(root)}")
    return 0


def command_validate(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    try:
        memory_map = load_map(root)
    except Exception as exc:
        print(f"[fail] Cannot read boot/memory_map.json: {exc}", file=sys.stderr)
        return 2

    for name in registered_projects(memory_map):
        base = root / "projects" / name
        if not base.exists():
            errors.append(f"registered project directory missing: {name}")
            continue
        missing = [filename for filename in REQUIRED_PROJECT_FILES if not (base / filename).exists()]
        if missing:
            errors.append(f"{name} missing files: {', '.join(missing)}")

    for path in sorted((root / "projects").iterdir() if (root / "projects").exists() else []):
        if not path.is_dir() or path.name == "_template":
            continue
        if path.name not in registered_projects(memory_map):
            warnings.append(f"project directory not registered: {path.name}")

    for warning in warnings:
        print(f"[warn] {warning}")
    for error in errors:
        print(f"[fail] {error}", file=sys.stderr)

    if errors:
        print(f"[summary] validation failed: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"[ok] validation passed: {len(registered_projects(memory_map))} active project(s), {len(warnings)} warning(s)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage local memory project lifecycle")
    parser.add_argument("--root", default=str(ROOT), help="Memory root path")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create", help="Create a project from projects/_template")
    create.add_argument("name", help="Project name")
    create.add_argument("--dry-run", action="store_true", help="Show intended changes without writing")
    create.set_defaults(func=command_create)

    list_cmd = subparsers.add_parser("list", help="List active projects")
    list_cmd.add_argument("--archived", action="store_true", help="Also list archive/old_projects")
    list_cmd.set_defaults(func=command_list)

    archive = subparsers.add_parser("archive", help="Move a project to archive/old_projects and unregister it")
    archive.add_argument("name", help="Project name")
    archive.add_argument("--dry-run", action="store_true", help="Show intended changes without writing")
    archive.set_defaults(func=command_archive)

    validate = subparsers.add_parser("validate", help="Validate project directories and registration")
    validate.set_defaults(func=command_validate)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except ValueError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
