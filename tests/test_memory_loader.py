import importlib
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BOOT_DIR = REPO_ROOT / "boot"


def write_text(root: Path, rel_path: str, content: str) -> None:
    path = root / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def make_memory_root(tmp_path: Path) -> Path:
    memory_map = {
        "version": "1.0",
        "root": str(tmp_path),
        "default_load": ["profile/identity.md"],
        "project_load": ["projects/{project}/project_brief.md"],
        "optional_load": [
            "profile/expertise.md",
            "projects/{project}/decisions.md",
        ],
        "on_demand_only": ["archive/"],
        "projects": ["Demo", "_template"],
        "history_index": "context/history_index.md",
        "output_file": "boot/assembled_context.txt",
    }
    write_text(tmp_path, "boot/memory_map.json", json.dumps(memory_map, ensure_ascii=False))
    write_text(tmp_path, "profile/identity.md", "core identity")
    write_text(tmp_path, "profile/expertise.md", "optional expertise")
    write_text(tmp_path, "projects/Demo/project_brief.md", "demo brief")
    write_text(tmp_path, "projects/Demo/decisions.md", "demo decisions")
    return tmp_path


def import_load_memory(monkeypatch):
    monkeypatch.syspath_prepend(str(BOOT_DIR))
    return importlib.reload(importlib.import_module("load_memory"))


def test_resolve_root_prefers_environment(monkeypatch, tmp_path):
    monkeypatch.syspath_prepend(str(BOOT_DIR))
    memory_loader = importlib.reload(importlib.import_module("memory_loader"))
    monkeypatch.setenv(memory_loader.ENV_ROOT, str(tmp_path))

    assert memory_loader.resolve_root(BOOT_DIR / "load_memory.py") == tmp_path.resolve()


def test_assemble_loads_core_and_project_files(monkeypatch, tmp_path):
    root = make_memory_root(tmp_path)
    load_memory = import_load_memory(monkeypatch)
    monkeypatch.setattr(load_memory, "ROOT", root)
    monkeypatch.setattr(load_memory, "MAP_FILE", root / "boot" / "memory_map.json")

    context = load_memory.assemble(project="Demo")

    assert "# Source: profile/identity.md" in context
    assert "core identity" in context
    assert "# Source: projects/Demo/project_brief.md" in context
    assert "demo brief" in context
    assert "optional expertise" not in context
    assert "demo decisions" not in context


def test_assemble_full_loads_global_and_project_optional(monkeypatch, tmp_path):
    root = make_memory_root(tmp_path)
    load_memory = import_load_memory(monkeypatch)
    monkeypatch.setattr(load_memory, "ROOT", root)
    monkeypatch.setattr(load_memory, "MAP_FILE", root / "boot" / "memory_map.json")

    context = load_memory.assemble(project="Demo", full=True)

    assert "# Source: profile/expertise.md" in context
    assert "optional expertise" in context
    assert "# Source: projects/Demo/decisions.md" in context
    assert "demo decisions" in context
