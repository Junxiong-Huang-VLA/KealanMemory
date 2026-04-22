import importlib
import json
from pathlib import Path


def write_text(root: Path, rel_path: str, content: str) -> None:
    path = root / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_memory_api_rejects_unknown_project(monkeypatch, tmp_path):
    memory_map = {"projects": ["Known", "_template"], "default_load": [], "project_load": []}
    write_text(tmp_path, "boot/memory_map.json", json.dumps(memory_map))

    web_app = importlib.reload(importlib.import_module("web.app"))
    monkeypatch.setattr(web_app, "ROOT", tmp_path)
    web_app.app.testing = True

    response = web_app.app.test_client().get("/api/memory?project=MissingProject")

    assert response.status_code == 400
    assert response.get_json()["ok"] is False
    assert "MissingProject" in response.get_json()["error"]


def test_copy_memory_api_rejects_unknown_project_before_clipboard(monkeypatch, tmp_path):
    memory_map = {"projects": ["Known", "_template"], "default_load": [], "project_load": []}
    write_text(tmp_path, "boot/memory_map.json", json.dumps(memory_map))

    web_app = importlib.reload(importlib.import_module("web.app"))
    monkeypatch.setattr(web_app, "ROOT", tmp_path)
    web_app.app.testing = True

    response = web_app.app.test_client().post(
        "/api/copy-memory",
        json={"project": "MissingProject"},
    )

    assert response.status_code == 400
    assert response.get_json()["ok"] is False


def test_edit_file_api_rejects_illegal_path(monkeypatch, tmp_path):
    memory_map = {"projects": ["Known", "_template"], "default_load": [], "project_load": []}
    write_text(tmp_path, "boot/memory_map.json", json.dumps(memory_map))

    web_app = importlib.reload(importlib.import_module("web.app"))
    monkeypatch.setattr(web_app, "ROOT", tmp_path)
    web_app.app.testing = True

    client = web_app.app.test_client()
    responses = [
        client.get("/api/edit-file?path=roles/01_yolo_trainer.md"),
        client.post("/api/diff", json={"path": "../README.md", "content": "x"}),
        client.post("/api/save", json={"path": "projects/Known/project_brief.md", "content": "x"}),
    ]

    assert [response.status_code for response in responses] == [400, 400, 400]
    assert all(response.get_json()["ok"] is False for response in responses)


def test_diff_api_is_read_only_for_whitelisted_file(monkeypatch, tmp_path):
    memory_map = {"projects": ["Known", "_template"], "default_load": [], "project_load": []}
    write_text(tmp_path, "boot/memory_map.json", json.dumps(memory_map))
    write_text(tmp_path, "context/active_focus.md", "old\n")

    web_app = importlib.reload(importlib.import_module("web.app"))
    monkeypatch.setattr(web_app, "ROOT", tmp_path)
    web_app.app.testing = True

    response = web_app.app.test_client().post(
        "/api/diff",
        json={"path": "context/active_focus.md", "content": "new\n"},
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["ok"] is True
    assert payload["changed"] is True
    assert "-old" in payload["diff"]
    assert "+new" in payload["diff"]
    assert (tmp_path / "context/active_focus.md").read_text(encoding="utf-8") == "old\n"


def test_save_api_writes_allowed_project_file_and_runs_health(monkeypatch, tmp_path):
    memory_map = {"projects": ["Known", "_template"], "default_load": [], "project_load": []}
    write_text(tmp_path, "boot/memory_map.json", json.dumps(memory_map))
    write_text(tmp_path, "projects/Known/current_status.md", "old\n")

    web_app = importlib.reload(importlib.import_module("web.app"))
    monkeypatch.setattr(web_app, "ROOT", tmp_path)
    monkeypatch.setattr(web_app, "run_health_check", lambda: {"ok": True, "summary": "Summary: ok", "output": ""})
    web_app.app.testing = True

    response = web_app.app.test_client().post(
        "/api/save",
        json={"path": "projects/Known/current_status.md", "content": "new\n"},
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["ok"] is True
    assert payload["health"]["ok"] is True
    assert (tmp_path / "projects/Known/current_status.md").read_text(encoding="utf-8") == "new\n"
