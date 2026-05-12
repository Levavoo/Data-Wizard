# Protocol — Stage D Local Quality Command Guide

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/07_CSV_github_actions_quality_gate.md` |
| Stage | Stage D — Local Quality Command Guide |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Development documentation |

---

## Purpose

Document local commands equivalent to the GitHub Actions workflow.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/development/local_quality_commands.md` | Created | Documents local pytest, ruff, and black commands. |
| `log_protocol/07_CSV_github_actions_quality_gate/004_local_quality_command_guide.md` | Created | Records Stage D completion. |

---

## Commands Documented

```text
ruff check .
black --check .
python -m pytest
```

---

## Production Code Decision

No production code change was made.
