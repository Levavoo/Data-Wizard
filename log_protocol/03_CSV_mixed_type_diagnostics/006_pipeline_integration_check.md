# Protocol — Stage F Pipeline Integration Check

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/03_CSV_mixed_type_diagnostics.md` |
| Stage | Stage F — Pipeline Integration Check |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Pipeline tests and documentation |

---

## Purpose

Verify mixed-type diagnostics work through the normal CSV pipeline.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `tests/test_pipeline.py` | Modified | Adds mixed-type diagnostic pipeline test. |
| `tests/test_pipeline.md` | Modified | Documents mixed-type pipeline behavior. |
| `log_protocol/03_CSV_mixed_type_diagnostics/006_pipeline_integration_check.md` | Created | Records Stage F completion. |

---

## Behavior Verified

Pipeline diagnostic bundle reports:

```text
column = amount
dominant_type = float
invalid value = row 2, unknown
```

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
