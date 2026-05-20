# Protocol — Stage E Quarantine Rows CSV Export

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/11_CSV_quarantine_export.md` |
| Stage | Stage E — Quarantine Rows CSV Export |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Pipeline integration, tests, documentation |

---

## Purpose

Export quarantine candidate rows to a separate CSV file when explicitly requested.

---

## Pipeline Parameter Added

```python
quarantine_rows_path=None
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `data_processor/core/pipeline.py` | Modified | Adds optional quarantine rows CSV export. |
| `data_processor/core/pipeline.md` | Modified | Documents quarantine rows export. |
| `tests/test_pipeline.py` | Modified | Verifies quarantine rows CSV output. |
| `log_protocol/11_CSV_quarantine_export/005_quarantine_rows_csv_export.md` | Created | Records Stage E completion. |

---

## Behavior Added

```text
quarantine rows CSV is written only when path is provided
normal cleaned CSV still includes all rows
quarantine rows CSV contains candidate rows only
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
