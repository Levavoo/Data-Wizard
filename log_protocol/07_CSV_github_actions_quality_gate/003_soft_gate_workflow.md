# Protocol — Stage C Add Soft-Gate Workflow

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/07_CSV_github_actions_quality_gate.md` |
| Stage | Stage C — Add Soft-Gate Workflow |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | GitHub Actions workflow and documentation |

---

## Purpose

Add the first GitHub Actions workflow for automated quality checks.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `.github/workflows/codex_checks.yml` | Created | Runs CI checks on `codex` pushes and PRs into `master`. |
| `.github/workflows/codex_checks.md` | Created | Documents the workflow. |
| `log_protocol/07_CSV_github_actions_quality_gate/003_soft_gate_workflow.md` | Created | Records Stage C completion. |

---

## Checks Added

```text
ruff check .
black --check .
python -m pytest
```

---

## Gate Policy

```text
soft gate
```

Branch protection was not enabled automatically.

---

## Tests / Checks

Expected verification happens on GitHub after push.

Status:

```text
Not verified by assistant in this environment.
```
