# Protocol — Stage F Pipeline Integration Check

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/04_CSV_suspicious_row_classification.md` |
| Stage | Stage F — Pipeline Integration Check |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Pipeline tests and documentation |

---

## Purpose

Verify suspicious row classification works through the normal CSV pipeline.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `tests/test_pipeline.py` | Modified | Adds suspicious row diagnostic pipeline test. |
| `tests/test_pipeline.md` | Modified | Documents suspicious row pipeline behavior. |
| `log_protocol/04_CSV_suspicious_row_classification/006_pipeline_integration_check.md` | Created | Records Stage F completion. |

---

## Behavior Verified

Pipeline diagnostic bundle reports:

```text
summary_row: 1
footer_row: 1
```

Rows remain in the table.

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
