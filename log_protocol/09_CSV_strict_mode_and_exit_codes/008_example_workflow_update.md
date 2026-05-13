# Protocol — Stage H Example Workflow Update

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/09_CSV_strict_mode_and_exit_codes.md` |
| Stage | Stage H — Example Workflow Update |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | User guide and example workflow test |

---

## Purpose

Update user examples to show strict and non-strict behavior.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/user_guides/run_csv_pipeline_example.md` | Modified | Documents strict-mode example and exit code `2`. |
| `tests/test_example_csv_workflow.py` | Modified | Confirms example workflow returns pipeline status. |
| `log_protocol/09_CSV_strict_mode_and_exit_codes/008_example_workflow_update.md` | Created | Records Stage H completion. |

---

## Behavior Verified

```text
example workflow includes pipeline_status
non-strict example status does not fail strict policy
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
