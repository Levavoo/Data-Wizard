# Protocol — Stage I User Guide Update

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/11_CSV_quarantine_export.md` |
| Stage | Stage I — User Guide Update |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | User documentation |

---

## Purpose

Update user documentation to explain quarantine export workflow.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/user_guides/run_csv_pipeline_example.md` | Modified | Adds quarantine export command, output explanation, and safety notes. |
| `log_protocol/11_CSV_quarantine_export/009_user_guide_update.md` | Created | Records Stage I completion. |

---

## Behavior Documented

```text
cleaned CSV includes all rows
quarantine_candidates.json is machine-readable
quarantine_rows.csv is for review
accepted_rows.csv is an explicit split output
```
