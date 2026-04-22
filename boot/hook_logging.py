#!/usr/bin/env python3
"""Best-effort, redacted hook logging for KealanMemory."""

from __future__ import annotations

import json
import os
import re
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]{12,}"),
    re.compile(r"(?:api[_-]?key|auth[_-]?token|secret|password)\s*[:=]\s*['\"]?[^'\"\s,;]{8,}", re.I),
    re.compile(r"bearer\s+[A-Za-z0-9_./+=-]{12,}", re.I),
)
SENSITIVE_KEYS = {
    "api_key",
    "apikey",
    "auth",
    "authorization",
    "content",
    "conversation",
    "daschscope_api_key",
    "dashscope_api_key",
    "message",
    "messages",
    "password",
    "prompt",
    "secret",
    "text",
    "token",
}
MAX_STRING = 300


def _log_dir() -> Path:
    configured = os.environ.get("KEALAN_MEMORY_LOG_DIR")
    if configured:
        return Path(configured).expanduser()
    return Path.home() / ".kealan_memory" / "logs"


def _redact_string(value: str) -> str:
    redacted = value
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    if len(redacted) > MAX_STRING:
        redacted = redacted[:MAX_STRING] + "...[truncated]"
    return redacted


def _sanitize(value: Any, key: str = "") -> Any:
    key_l = key.lower()
    if key_l in SENSITIVE_KEYS or any(part in key_l for part in ("token", "secret", "password", "api_key")):
        return "[REDACTED]"
    if isinstance(value, str):
        return _redact_string(value)
    if isinstance(value, Path):
        return _redact_string(str(value))
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    if isinstance(value, dict):
        return {str(k): _sanitize(v, str(k)) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_sanitize(item) for item in list(value)[:20]]
    return _redact_string(repr(value))


def log_event(hook: str, event: str, event_status: str | None = None, **fields: Any) -> None:
    """Write one JSONL event; never raise into hook code."""
    try:
        status = event_status or str(fields.pop("status", "ok"))
        log_dir = _log_dir()
        log_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "hook": hook,
            "event": event,
            "status": status,
            "fields": _sanitize(fields),
        }
        log_path = log_dir / f"hooks-{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
    except Exception:
        return


def log_exception(hook: str, event: str, exc: BaseException, **fields: Any) -> None:
    """Write a sanitized exception event; never raise into hook code."""
    log_event(
        hook,
        event,
        "error",
        error_type=type(exc).__name__,
        error=str(exc),
        traceback_tail=traceback.format_exception_only(type(exc), exc)[-1].strip(),
        **fields,
    )
