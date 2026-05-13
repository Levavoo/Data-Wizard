# Protocol — Stage G Example Workflow Test

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/06_CSV_report_usability_and_examples.md` |
| Stage | Stage G — Example Workflow Test |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Workflow test and documentation |

---

## Purpose

Verify the documented example CSV workflow can run through the current pipeline.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `tests/test_example_csv_workflow.py` | Created | Verifies example CSV and constraints work end to end. |
| `tests/test_example_csv_workflow.md` | Created | Documents example workflow test. |
| `log_protocol/06_CSV_report_usability_and_examples/007_example_workflow_test.md` | Created | Records Stage G completion. |

---

## Behavior Verified

```text
example CSV exists
example constraints JSON exists
constraints can be loaded
pipeline writes cleaned CSV
pipeline writes JSON report
diagnostic bundle contains expected sections
validation failures are detected
suspicious rows are detected
```

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_example_csv_workflow.py
python -m pytest
```

Status:

```text
Not executed by assistant in this environment.
```
