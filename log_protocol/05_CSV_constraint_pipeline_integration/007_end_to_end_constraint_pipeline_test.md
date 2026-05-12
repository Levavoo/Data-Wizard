# Protocol — Stage G End-to-End Constraint Pipeline Test

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/05_CSV_constraint_pipeline_integration.md` |
| Stage | Stage G — End-to-End Constraint Pipeline Test |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Pipeline test and documentation |

---

## Purpose

Verify full CSV constraint validation behavior through the pipeline.

---

## Behavior Verified

The pipeline validates constraints after cleaning and casting.

Covered failures:

```text
unique customer_id
allowed country values
regex email pattern
minimum amount
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `tests/test_pipeline.py` | Modified | Adds end-to-end constraint validation test. |
| `tests/test_pipeline.md` | Modified | Documents constraint validation test. |
| `log_protocol/05_CSV_constraint_pipeline_integration/007_end_to_end_constraint_pipeline_test.md` | Created | Records Stage G completion. |

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_pipeline.py
python -m pytest
```

Status:

```text
Not executed by assistant in this environment.
```
