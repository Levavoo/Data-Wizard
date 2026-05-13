# Protocol — Stage B GitHub Actions Workflow Design

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/07_CSV_github_actions_quality_gate.md` |
| Stage | Stage B — GitHub Actions Workflow Design |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Development documentation |

---

## Purpose

Design the first soft-gate GitHub Actions workflow.

---

## Decision

Workflow trigger policy:

```text
push to codex
pull_request targeting master
```

Check commands:

```text
ruff check .
black --check .
python -m pytest
```

Gate policy:

```text
soft gate
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/development/github_actions_quality_gate.md` | Created | Documents workflow behavior and soft-gate policy. |
| `log_protocol/07_CSV_github_actions_quality_gate/002_workflow_design.md` | Created | Records Stage B completion. |

---

## Production Code Decision

No production code change was made.
