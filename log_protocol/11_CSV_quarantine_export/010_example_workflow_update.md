# Protocol — Stage J Example Workflow Update

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/11_CSV_quarantine_export.md` |
| Stage | Stage J — Example Workflow Update |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Example workflow test and documentation |

---

## Purpose

Update the example workflow test to verify quarantine export outputs.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `tests/test_example_csv_workflow.py` | Modified | Verifies example workflow writes quarantine candidate JSON, quarantine rows CSV, and accepted rows CSV. |
| `tests/test_example_csv_workflow.md` | Modified | Documents quarantine export example workflow coverage. |
| `log_protocol/11_CSV_quarantine_export/010_example_workflow_update.md` | Created | Records Stage J completion. |

---

## Behavior Verified

```text
example workflow writes cleaned CSV
example workflow writes JSON report
example workflow writes HTML report
example workflow writes quarantine candidate JSON
example workflow writes quarantine rows CSV
example workflow writes accepted rows CSV
```

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_example_csv_workflow.py
```

Status:

```text
Not executed by assistant in this environment.
```
