# Protocol — Stage F Accepted Rows CSV Export

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/11_CSV_quarantine_export.md` |
| Stage | Stage F — Accepted Rows CSV Export |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Pipeline integration, tests, documentation |

---

## Purpose

Export accepted rows to a separate CSV file when explicitly requested.

---

## Pipeline Parameter Added

```python
accepted_rows_path=None
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `data_processor/core/pipeline.py` | Modified | Adds optional accepted rows CSV export. |
| `data_processor/core/pipeline.md` | Modified | Documents accepted rows export. |
| `tests/test_pipeline.py` | Modified | Verifies accepted rows CSV output. |
| `log_protocol/11_CSV_quarantine_export/006_accepted_rows_csv_export.md` | Created | Records Stage F completion. |

---

## Behavior Added

```text
accepted rows CSV is written only when path is provided
accepted rows CSV excludes quarantine candidate rows
normal cleaned CSV remains unchanged
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
