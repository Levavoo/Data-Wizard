# Protocol — Stage D Pipeline Validation Integration

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/05_CSV_constraint_pipeline_integration.md` |
| Stage | Stage D — Pipeline Validation Integration |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Pipeline integration, tests, documentation |

---

## Purpose

Allow the CSV pipeline to validate optional constraints after cleaning and casting.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `data_processor/core/pipeline.py` | Modified | Runs optional constraint validation. |
| `data_processor/core/pipeline.md` | Modified | Documents validation integration. |
| `tests/test_pipeline.py` | Modified | Adds constraint validation pipeline test. |
| `tests/test_pipeline.md` | Modified | Documents constraint validation test. |
| `log_protocol/05_CSV_constraint_pipeline_integration/004_pipeline_validation_integration.md` | Created | Records Stage D completion. |

---

## Behavior Added

```text
constraints are optional
validation runs after cleaning and casting
validation_results are returned
validation report appears in diagnostic_bundle
CSV export still runs
```

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_pipeline.py
```

Status:

```text
Not executed by assistant in this environment.
```
