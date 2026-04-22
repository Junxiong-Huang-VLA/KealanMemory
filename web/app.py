"""
KealanMemory Web — 本地记忆管理中心
端口 7777
"""
import json
import os
import subprocess
import sys
import difflib
from pathlib import Path, PurePosixPath

from flask import Flask, jsonify, render_template, request


def find_memory_root() -> Path:
    env_root = os.environ.get("KEALAN_MEMORY_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    return Path(__file__).resolve().parents[1]


ROOT = find_memory_root()
app = Flask(__name__, template_folder="templates", static_folder="static")


# ── 工具函数 ──────────────────────────────────────────────

def parse_frontmatter(text: str) -> tuple[dict, str]:
    meta, body = {}, text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
            body = parts[2].strip()
    return meta, body


def load_memory_map() -> dict:
    try:
        return json.loads((ROOT / "boot/memory_map.json").read_text(encoding="utf-8"))
    except Exception:
        return {}


def load_json(rel_path: str) -> dict:
    try:
        return json.loads((ROOT / rel_path).read_text(encoding="utf-8"))
    except Exception:
        return {}


def safe_read(rel_path: str) -> str:
    path = (ROOT / rel_path).resolve()
    try:
        path.relative_to(ROOT)
    except ValueError:
        return ""
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace").strip()


def validate_edit_path(rel_path: str) -> tuple[Path | None, str | None]:
    raw_path = str(rel_path or "").strip().replace("\\", "/")
    if not raw_path or raw_path.startswith("/") or "\x00" in raw_path:
        return None, "invalid path"

    posix_path = PurePosixPath(raw_path)
    parts = posix_path.parts
    if any(part in ("", ".", "..") for part in parts):
        return None, "invalid path"

    normalized = str(posix_path)
    allowed = normalized == "context/active_focus.md"
    if not allowed and len(parts) == 3 and parts[0] == "projects":
        allowed = parts[1] in get_projects() and parts[2] in {"current_status.md", "next_actions.md"}
    if not allowed:
        return None, "path is not editable"

    path = (ROOT / normalized).resolve()
    try:
        path.relative_to(ROOT)
    except ValueError:
        return None, "invalid path"
    return path, None


def make_diff(rel_path: str, old_content: str, new_content: str) -> str:
    return "\n".join(difflib.unified_diff(
        old_content.splitlines(),
        new_content.splitlines(),
        fromfile=f"a/{rel_path}",
        tofile=f"b/{rel_path}",
        lineterm="",
    ))


def rel_file_info(path: Path) -> dict:
    try:
        rel = str(path.resolve().relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        rel = str(path)
    exists = path.exists() and path.is_file()
    return {
        "path": rel,
        "exists": exists,
        "bytes": path.stat().st_size if exists else 0,
        "modified": path.stat().st_mtime if exists else None,
    }


def load_skills() -> list[dict]:
    skills_dir = ROOT / "skills"
    skills = []
    for p in sorted(skills_dir.glob("*.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        meta, body = parse_frontmatter(text)
        skills.append({
            "id": meta.get("id", p.stem),
            "name": meta.get("name", p.stem),
            "category": meta.get("category", "其他"),
            "description": meta.get("description", ""),
            "body": body,
            "file": p.name,
        })
    return skills


def load_roles() -> list[dict]:
    roles_dir = ROOT / "roles"
    roles = []
    for p in sorted(roles_dir.glob("*.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        meta, body = parse_frontmatter(text)
        roles.append({
            "id": meta.get("id", p.stem),
            "name": meta.get("name", p.stem),
            "category": meta.get("category", "其他"),
            "description": meta.get("description", ""),
            "body": body,
            "file": p.name,
        })
    return roles


def load_memory_context(project: str = "") -> str:
    memory_map = load_memory_map()
    core_files = memory_map.get("default_load", [])
    project_files = memory_map.get("project_load", [])
    chunks = ["# KealanMemory — 个人上下文\n"]
    for rel in core_files:
        content = safe_read(rel)
        if content:
            chunks.append(f"\n---\n## {rel}\n\n{content}")
    if project:
        for rel in project_files:
            rel_path = rel.replace("{project}", project)
            content = safe_read(rel_path)
            if content:
                chunks.append(f"\n---\n## {rel_path}\n\n{content}")
    return "\n".join(chunks)


def get_projects() -> list[str]:
    data = load_memory_map()
    return [p for p in data.get("projects", []) if p != "_template"]


def list_editable_files() -> list[dict]:
    files = [{"path": "context/active_focus.md", "label": "Core / active_focus.md"}]
    for project in get_projects():
        files.extend([
            {"path": f"projects/{project}/current_status.md", "label": f"{project} / current_status.md"},
            {"path": f"projects/{project}/next_actions.md", "label": f"{project} / next_actions.md"},
        ])
    return files


def load_project_status() -> list[dict]:
    statuses = []
    for project in get_projects():
        base = ROOT / "projects" / project
        files = {
            "brief": rel_file_info(base / "project_brief.md"),
            "status": rel_file_info(base / "current_status.md"),
            "constraints": rel_file_info(base / "constraints.md"),
            "next_actions": rel_file_info(base / "next_actions.md"),
        }
        current_status = safe_read(f"projects/{project}/current_status.md")
        next_actions = safe_read(f"projects/{project}/next_actions.md")
        latest_modified = max((item["modified"] or 0 for item in files.values()), default=0)
        statuses.append({
            "name": project,
            "files": files,
            "missing": [name for name, item in files.items() if not item["exists"]],
            "status_preview": current_status[:900],
            "next_actions_preview": next_actions[:700],
            "modified": latest_modified or None,
        })
    return statuses


def summarize_routing(data: dict) -> dict:
    routes = data.get("routes") or data.get("intents") or []
    roles = data.get("roles") or {}
    skills = data.get("skills") or {}
    return {
        "route_count": len(routes) if isinstance(routes, list) else 0,
        "role_count": len(roles) if isinstance(roles, dict) else 0,
        "skill_count": len(skills) if isinstance(skills, dict) else 0,
        "fallback_role": data.get("policy", {}).get("fallback_role"),
        "fallback_skills": data.get("policy", {}).get("fallback_skills", []),
    }


def search_history(query: str) -> list[dict]:
    q = query.casefold().strip()
    candidates = [ROOT / "context/history_index.md", *sorted((ROOT / "context/history").glob("*.md"))]
    results = []
    for path in candidates:
        if not path.exists() or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        haystack = f"{path.name}\n{text}".casefold()
        if q and q not in haystack:
            continue
        snippet_source = text
        if q:
            idx = haystack.find(q)
            start = max(0, idx - 180)
            end = min(len(text), idx + 520)
            snippet_source = text[start:end]
        results.append({
            "file": str(path.relative_to(ROOT)).replace("\\", "/"),
            "title": next((line.lstrip("# ").strip() for line in text.splitlines() if line.strip().startswith("#")), path.name),
            "snippet": snippet_source.strip()[:900],
            "modified": path.stat().st_mtime,
        })
    return results


def run_health_check() -> dict:
    script = ROOT / "boot/check_memory_consistency.py"
    if not script.exists():
        return {"ok": False, "exit_code": None, "summary": "health check script not found", "output": ""}
    try:
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=20,
        )
    except Exception as exc:
        return {"ok": False, "exit_code": None, "summary": str(exc), "output": ""}
    output = (result.stdout or result.stderr or "").strip()
    summary = next((line.strip() for line in output.splitlines() if line.strip().startswith("Summary:")), "")
    return {
        "ok": result.returncode == 0,
        "exit_code": result.returncode,
        "summary": summary,
        "output": output[-6000:],
    }


def validate_project(project: str) -> tuple[bool, str | None]:
    if not project:
        return True, None
    if project not in get_projects():
        return False, f"未知项目：{project}"
    return True, None


# ── 路由 ─────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/skills")
def api_skills():
    return jsonify(load_skills())


@app.route("/api/roles")
def api_roles():
    return jsonify(load_roles())


@app.route("/api/memory")
def api_memory():
    project = request.args.get("project", "")
    ok, error = validate_project(project)
    if not ok:
        return jsonify({"ok": False, "error": error}), 400
    context = load_memory_context(project)
    return jsonify({"ok": True, "context": context, "project": project})


@app.route("/api/projects")
def api_projects():
    return jsonify(get_projects())


@app.route("/api/routing")
def api_routing():
    data = load_json("boot/routing_map.json")
    return jsonify({
        "ok": bool(data),
        "summary": summarize_routing(data),
        "routing": data,
        "projects": load_project_status(),
    })


@app.route("/api/history")
def api_history():
    query = request.args.get("q", "")
    return jsonify({"ok": True, "query": query, "results": search_history(query)})


@app.route("/api/health")
def api_health():
    data = run_health_check()
    status = 200 if data["ok"] else 503
    return jsonify(data), status


@app.route("/api/focus")
def api_focus():
    p = ROOT / "context/active_focus.md"
    if p.exists():
        return jsonify({"content": p.read_text(encoding="utf-8", errors="replace")})
    return jsonify({"content": ""})


@app.route("/api/editable-files")
def api_editable_files():
    return jsonify({"ok": True, "files": list_editable_files()})


@app.route("/api/edit-file")
def api_edit_file():
    rel_path = request.args.get("path", "")
    path, error = validate_edit_path(rel_path)
    if error:
        return jsonify({"ok": False, "error": error}), 400
    content = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    return jsonify({"ok": True, "path": str(PurePosixPath(rel_path.replace("\\", "/"))), "content": content})


@app.route("/api/diff", methods=["POST"])
def api_diff():
    payload = request.get_json(silent=True) or {}
    rel_path = str(payload.get("path", "")).strip().replace("\\", "/")
    path, error = validate_edit_path(rel_path)
    if error:
        return jsonify({"ok": False, "error": error}), 400

    old_content = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    new_content = str(payload.get("content", ""))
    return jsonify({
        "ok": True,
        "path": rel_path,
        "changed": old_content != new_content,
        "diff": make_diff(rel_path, old_content, new_content),
    })


@app.route("/api/save", methods=["POST"])
def api_save():
    payload = request.get_json(silent=True) or {}
    rel_path = str(payload.get("path", "")).strip().replace("\\", "/")
    path, error = validate_edit_path(rel_path)
    if error:
        return jsonify({"ok": False, "error": error}), 400

    old_content = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    new_content = str(payload.get("content", ""))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(new_content, encoding="utf-8")
    health = run_health_check()
    return jsonify({
        "ok": True,
        "path": rel_path,
        "changed": old_content != new_content,
        "diff": make_diff(rel_path, old_content, new_content),
        "health": health,
    })


@app.route("/api/copy-memory", methods=["POST"])
def api_copy_memory():
    """组装上下文并复制到剪贴板"""
    payload = request.get_json(silent=True) or {}
    project = payload.get("project", "")
    ok, error = validate_project(project)
    if not ok:
        return jsonify({"ok": False, "error": error}), 400
    context = load_memory_context(project)
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", "Set-Clipboard -Value ([Console]::In.ReadToEnd())"],
            input=context,
            text=True,
            capture_output=True,
            timeout=5,
            check=True,
        )
        return jsonify({"ok": True, "chars": len(context)})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})


if __name__ == "__main__":
    print("KealanMemory Web 启动中...")
    print("访问 http://localhost:7777")
    app.run(host="127.0.0.1", port=7777, debug=False)
