import json
from pathlib import Path

from jsonschema import Draft202012Validator

from boot.check_memory_consistency import parse_frontmatter


REPO_ROOT = Path(__file__).resolve().parents[1]


def validate(instance_path: str, schema_path: str) -> None:
    schema = json.loads((REPO_ROOT / schema_path).read_text(encoding="utf-8"))
    instance = json.loads((REPO_ROOT / instance_path).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(instance),
        key=lambda error: list(error.absolute_path),
    )
    assert errors == [], "\n".join(error.message for error in errors)


def test_memory_map_matches_schema():
    validate("boot/memory_map.json", "schemas/memory_map.schema.json")


def test_routing_map_matches_schema():
    validate("boot/routing_map.json", "schemas/routing_map.schema.json")


def validate_instance(instance: dict, schema_path: str) -> None:
    schema = json.loads((REPO_ROOT / schema_path).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(instance),
        key=lambda error: list(error.absolute_path),
    )
    assert errors == [], "\n".join(error.message for error in errors)


def test_role_frontmatter_matches_schema():
    for path in sorted((REPO_ROOT / "roles").glob("*.md")):
        meta = parse_frontmatter(path.read_text(encoding="utf-8"))
        validate_instance(meta, "schemas/role_frontmatter.schema.json")


def test_skill_frontmatter_matches_schema():
    for path in sorted((REPO_ROOT / "skills").glob("*.md")):
        meta = parse_frontmatter(path.read_text(encoding="utf-8"))
        validate_instance(meta, "schemas/skill_frontmatter.schema.json")
