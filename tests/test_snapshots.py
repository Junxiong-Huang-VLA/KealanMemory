import importlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BOOT_DIR = REPO_ROOT / "boot"
SNAPSHOT_DIR = REPO_ROOT / "tests" / "snapshots"


def write_text(root: Path, rel_path: str, content: str) -> None:
    path = root / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def make_memory_root(tmp_path: Path) -> Path:
    memory_map = {
        "version": "1.0",
        "root": str(tmp_path),
        "default_load": [
            "profile/identity.md",
            "profile/work_style.md",
        ],
        "project_load": [
            "projects/{project}/project_brief.md",
            "projects/{project}/current_status.md",
        ],
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
    write_text(tmp_path, "profile/identity.md", "Identity: Kealan test memory")
    write_text(tmp_path, "profile/work_style.md", "Work style: concise and evidence-driven")
    write_text(tmp_path, "profile/expertise.md", "Expertise: detection pipelines")
    write_text(tmp_path, "projects/Demo/project_brief.md", "Project brief: demo project")
    write_text(tmp_path, "projects/Demo/current_status.md", "Current status: green")
    write_text(tmp_path, "projects/Demo/decisions.md", "Decision log: keep snapshots stable")
    return tmp_path


def import_load_memory(monkeypatch):
    monkeypatch.syspath_prepend(str(BOOT_DIR))
    return importlib.reload(importlib.import_module("load_memory"))


def read_snapshot(name: str) -> str:
    return (SNAPSHOT_DIR / name).read_text(encoding="utf-8").replace("\r\n", "\n").removesuffix("\n")


def test_standard_context_matches_golden_snapshot(monkeypatch, tmp_path):
    root = make_memory_root(tmp_path)
    load_memory = import_load_memory(monkeypatch)
    monkeypatch.setattr(load_memory, "ROOT", root)
    monkeypatch.setattr(load_memory, "MAP_FILE", root / "boot" / "memory_map.json")

    context = load_memory.assemble(project="Demo")

    assert context.replace("\r\n", "\n") == read_snapshot("standard_context.txt")


def test_full_context_matches_golden_snapshot(monkeypatch, tmp_path):
    root = make_memory_root(tmp_path)
    load_memory = import_load_memory(monkeypatch)
    monkeypatch.setattr(load_memory, "ROOT", root)
    monkeypatch.setattr(load_memory, "MAP_FILE", root / "boot" / "memory_map.json")

    context = load_memory.assemble(project="Demo", full=True)

    assert context.replace("\r\n", "\n") == read_snapshot("full_context.txt")
