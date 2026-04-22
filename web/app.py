"""
KealanMemory Web — 本地记忆管理中心
端口 7777
"""
import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_from_directory

ROOT = Path("D:/KealanMemory")
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
    core_files = [
        "profile/identity.md",
        "profile/work_style.md",
        "profile/preferences.md",
        "operating_rules/communication_rules.md",
        "context/active_focus.md",
        "context/global_constraints.md",
    ]
    chunks = ["# KealanMemory — 个人上下文\n"]
    for rel in core_files:
        p = ROOT / rel
        if p.exists():
            chunks.append(f"\n---\n## {rel}\n\n{p.read_text(encoding='utf-8', errors='replace').strip()}")
    if project:
        for fname in ["project_brief.md", "current_status.md", "constraints.md", "next_actions.md"]:
            p = ROOT / "projects" / project / fname
            if p.exists():
                chunks.append(f"\n---\n## projects/{project}/{fname}\n\n{p.read_text(encoding='utf-8', errors='replace').strip()}")
    return "\n".join(chunks)


def get_projects() -> list[str]:
    try:
        data = json.loads((ROOT / "boot/memory_map.json").read_text(encoding="utf-8"))
        return [p for p in data.get("projects", []) if p != "_template"]
    except Exception:
        return []


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
    context = load_memory_context(project)
    return jsonify({"context": context, "project": project})


@app.route("/api/projects")
def api_projects():
    return jsonify(get_projects())


@app.route("/api/focus")
def api_focus():
    p = ROOT / "context/active_focus.md"
    if p.exists():
        return jsonify({"content": p.read_text(encoding="utf-8", errors="replace")})
    return jsonify({"content": ""})


@app.route("/api/copy-memory", methods=["POST"])
def api_copy_memory():
    """组装上下文并复制到剪贴板"""
    project = request.json.get("project", "") if request.json else ""
    context = load_memory_context(project)
    try:
        subprocess.run(
            ["powershell", "-Command", f"Set-Clipboard -Value @'\n{context}\n'@"],
            capture_output=True, timeout=5
        )
        return jsonify({"ok": True, "chars": len(context)})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})


if __name__ == "__main__":
    print("KealanMemory Web 启动中...")
    print("访问 http://localhost:7777")
    app.run(host="127.0.0.1", port=7777, debug=False)
