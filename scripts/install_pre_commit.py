#!/usr/bin/env python3
"""Install a local Git pre-commit hook for KealanMemory."""

from __future__ import annotations

import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK_PATH = ROOT / ".git" / "hooks" / "pre-commit"


HOOK = """#!/bin/sh
exec powershell -NoProfile -ExecutionPolicy Bypass -File "scripts/pre_commit_check.ps1"
"""


def main() -> int:
    if not (ROOT / ".git").exists():
        print("[fail] .git directory not found")
        return 1
    HOOK_PATH.parent.mkdir(parents=True, exist_ok=True)
    if HOOK_PATH.exists():
        backup = HOOK_PATH.with_name("pre-commit.bak")
        backup.write_text(HOOK_PATH.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        print(f"[ok] existing hook backed up to {backup}")
    HOOK_PATH.write_text(HOOK, encoding="utf-8", newline="\n")
    try:
        os.chmod(HOOK_PATH, 0o755)
    except OSError:
        pass
    print(f"[ok] installed {HOOK_PATH}")
    print("Run manually: powershell -NoProfile -ExecutionPolicy Bypass -File scripts/pre_commit_check.ps1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
