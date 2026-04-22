import importlib
import json
from pathlib import Path


def write_text(root: Path, rel_path: str, content: str) -> None:
    path = root / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_routing_check_reports_dangling_skill_and_role(monkeypatch, tmp_path):
    health = importlib.reload(importlib.import_module("boot.check_memory_consistency"))
    monkeypatch.setattr(health, "ROOT", tmp_path)
    write_text(
        tmp_path,
        "boot/routing_map.json",
        json.dumps(
            {
                "intents": [
                    {
                        "role": "missing-role",
                        "skills": ["missing-skill"],
                    }
                ]
            }
        ),
    )
    report = health.Report()

    health.check_routing(report, skill_ids={"known-skill"}, role_ids={"known-role"})

    assert any("missing-skill" in failure for failure in report.failures)
    assert any("missing-role" in failure for failure in report.failures)


def test_frontmatter_check_reports_missing_required_fields(monkeypatch, tmp_path):
    health = importlib.reload(importlib.import_module("boot.check_memory_consistency"))
    monkeypatch.setattr(health, "ROOT", tmp_path)
    write_text(
        tmp_path,
        "skills/bad.md",
        "---\nid: bad\nname: Bad\ncategory: test\n---\nbody",
    )
    write_text(
        tmp_path,
        "roles/good.md",
        "---\nid: good\nname: Good\ncategory: test\ndescription: ok\n---\nbody",
    )
    report = health.Report()

    health.check_frontmatter(report)

    assert any("bad.md" in failure and "description" in failure for failure in report.failures)
