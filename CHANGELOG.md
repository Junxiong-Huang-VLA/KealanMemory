# Changelog

## 2026-04-22 - Optimization baseline

This release converts KealanMemory from a mostly manual memory folder into a more verifiable local memory platform.

Recommended commit groups:

1. Security and install governance: `.gitignore`, `install/*`, `boot/hooks/*`
2. Loader and launch scripts: `boot/memory_loader.py`, `boot/load_memory.py`, `boot/load_memory.ps1`, `boot/start_memory.bat`
3. Role/skill routing: `boot/routing_map.*`, `roles/`, `skills/`, `boot/write_skills.py`
4. Web operations UI: `web/app.py`, `web/templates/`, `web/static/`
5. Verification: `boot/check_memory_consistency.py`, `tests/`, `schemas/`, `scripts/`
6. Project and history CLI: `boot/project_manager.py`, `boot/history_search.py`
7. Planning and docs: `README.md`, `OPTIMIZATION_TASKBOOK.md`, `REMAINING_OPTIMIZATION_TASKBOOK.md`

Before each commit group, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/pre_commit_check.ps1
```

Key changes:

- Removed real secrets from install templates and added local secret ignores.
- Added shared memory root resolution through `KEALAN_MEMORY_ROOT`.
- Added health checks, schemas, pytest tests, and pre-commit checks.
- Added project lifecycle and history search CLIs.
- Added Web Ops panels for routing, projects, history, and health.
- Standardized role and skill metadata.

