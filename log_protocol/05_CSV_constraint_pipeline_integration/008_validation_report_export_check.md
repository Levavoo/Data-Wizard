# Protocol — Stage H Validation Report Export Check

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/05_CSV_constraint_pipeline_integration.md` |
| Stage | Stage H — Validation Report Export Check |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Pipeline/report behavior |

---

## Purpose

Verify validation reports are included in diagnostic report export.

---

## Behavior

The CSV pipeline exports the complete diagnostic bundle when `report_path` is provided.

Because constraint validation results are now passed into the diagnostic bundle, exported JSON reports include the validation report.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `data_processor/core/pipeline.py` | Modified | Passes validation results to diagnostic bundle. |
| `tests/test_pipeline.py` | Modified | Confirms diagnostic report export still includes validation report. |
| `log_protocol/05_CSV_constraint_pipeline_integration/008_validation_report_export_check.md` | Created | Records Stage H completion. |

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
