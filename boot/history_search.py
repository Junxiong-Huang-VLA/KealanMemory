#!/usr/bin/env python3
"""Search and resolve on-demand history memory files."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from memory_loader import resolve_root
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from memory_loader import resolve_root


ROOT = resolve_root(__file__)
HISTORY_DIR = ROOT / "context" / "history"
HISTORY_INDEX = ROOT / "context" / "history_index.md"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


@dataclass(frozen=True)
class HistoryMatch:
    path: Path
    score: int
    reason: str


def _normalize_path(value: str, root: Path) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = root / path
    return path.resolve()


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def history_files(root: Path = ROOT) -> list[Path]:
    base = root / "context" / "history"
    if not base.exists():
        return []
    return sorted(p for p in base.glob("*.md") if p.is_file())


def _index_mentions(root: Path) -> dict[str, str]:
    index_path = root / "context" / "history_index.md"
    if not index_path.exists():
        return {}

    text = index_path.read_text(encoding="utf-8", errors="replace")
    mentions: dict[str, str] = {}
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        raw = match.group(1).strip()
        if not raw:
            continue
        linked = (index_path.parent / raw).resolve()
        mentions[linked.name.lower()] = raw
    return mentions


def resolve_history(query_or_file: str, root: Path = ROOT, limit: int = 5) -> list[HistoryMatch]:
    """Resolve a history query or an explicit markdown file path."""
    query = query_or_file.strip()
    if not query:
        return []

    explicit = _normalize_path(query, root)
    history_root = (root / "context" / "history").resolve()
    if explicit.exists() and explicit.is_file():
        if explicit.suffix.lower() != ".md":
            raise ValueError(f"History file must be markdown: {explicit}")
        if not (_is_within(explicit, history_root) or explicit == (root / "context" / "history_index.md").resolve()):
            raise ValueError(f"History file must be under context/history or be history_index.md: {explicit}")
        return [HistoryMatch(explicit, 1000, "explicit file")]

    lowered = query.lower()
    terms = [t for t in re.split(r"\s+", lowered) if t]
    index_mentions = _index_mentions(root)
    matches: list[HistoryMatch] = []

    for path in history_files(root):
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        haystack = f"{path.name}\n{content}".lower()
        score = 0
        reasons: list[str] = []

        if lowered in path.name.lower():
            score += 100
            reasons.append("filename")
        if lowered in content.lower():
            score += 50
            reasons.append("content phrase")

        term_hits = sum(1 for term in terms if term in haystack)
        if term_hits:
            score += term_hits * 20
            if "terms" not in reasons:
                reasons.append("terms")

        if score > 0:
            if path.name.lower() in index_mentions:
                score += 10
                reasons.append("indexed")
            matches.append(HistoryMatch(path, score, ", ".join(reasons) or "match"))

    matches.sort(key=lambda item: (-item.score, item.path.name.lower()))
    return matches[:limit]


def format_history_context(matches: list[HistoryMatch]) -> str:
    chunks: list[str] = []
    seen: set[Path] = set()
    for match in matches:
        path = match.path.resolve()
        if path in seen:
            continue
        seen.add(path)
        rel = path.relative_to(ROOT) if _is_within(path, ROOT) else path
        content = path.read_text(encoding="utf-8", errors="replace").strip()
        separator = f"\n\n{'=' * 60}\n# History Source: {rel}\n# Match: {match.reason}\n{'=' * 60}\n"
        chunks.append(separator + content)
    return "\n".join(chunks)


def main() -> int:
    parser = argparse.ArgumentParser(description="Search on-demand history memory files")
    parser.add_argument("query", help="Keyword, phrase, or context/history markdown file")
    parser.add_argument("--limit", "-n", type=int, default=5, help="Maximum matches to show")
    parser.add_argument("--root", default=str(ROOT), help="Memory root path")
    parser.add_argument("--paths-only", action="store_true", help="Print only matched file paths")
    parser.add_argument("--inject", action="store_true", help="Print full history context for injection")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    try:
        matches = resolve_history(args.query, root=root, limit=max(args.limit, 1))
    except ValueError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 2

    if not matches:
        print(f"[miss] No history matched: {args.query}", file=sys.stderr)
        return 1

    if args.inject:
        print(format_history_context(matches))
        return 0

    for match in matches:
        rel = match.path.relative_to(root) if _is_within(match.path, root) else match.path
        if args.paths_only:
            print(rel)
        else:
            print(f"{rel}  score={match.score}  reason={match.reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
