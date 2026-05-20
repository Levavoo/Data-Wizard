# Protocol — Stage H Example Workflow Profile Test

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/12_CSV_cleaning_profiles.md` |
| Stage | Stage H — Example Workflow Profile Test |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Example workflow test and documentation |

---

## Purpose

Update example workflow tests to verify at least one profile-driven run.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `tests/test_example_csv_workflow.py` | Modified | Adds CLI profile workflow test. |
| `tests/test_example_csv_workflow.md` | Modified | Documents profile workflow coverage. |
| `log_protocol/12_CSV_cleaning_profiles/008_example_workflow_profile_test.md` | Created | Records Stage H completion. |

---

## Behavior Verified

```text
example workflow can run through CLI with --profile migration_audit
existing explicit pipeline workflow still works
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
