"""Shared path helpers for memory loading scripts."""

from __future__ import annotations

import os
from pathlib import Path


ENV_ROOT = "KEALAN_MEMORY_ROOT"


def resolve_root(anchor: str | Path | None = None) -> Path:
    """Resolve the repository root.

    KEALAN_MEMORY_ROOT wins when set. Otherwise infer the root from a file inside
    boot/ by taking its parent directory's parent.
    """
    env_root = os.environ.get(ENV_ROOT)
    if env_root:
        return Path(env_root).expanduser().resolve()

    anchor_path = Path(anchor) if anchor is not None else Path(__file__)
    return anchor_path.resolve().parent.parent


def memory_map_path(root: Path) -> Path:
    return root / "boot" / "memory_map.json"


def default_output_path(root: Path) -> Path:
    return root / "boot" / "assembled_context.txt"
