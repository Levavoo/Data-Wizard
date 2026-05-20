# Protocol — Stage D Quarantine Row Selection Utility

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/11_CSV_quarantine_export.md` |
| Stage | Stage D — Quarantine Row Selection Utility |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Row selection utility, tests, documentation |

---

## Purpose

Add utilities that separate table rows by quarantine candidate row indexes.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `data_processor/reports/quarantine_row_selection.py` | Created | Selects quarantine and accepted rows from candidate indexes. |
| `data_processor/reports/quarantine_row_selection.md` | Created | Documents row selection behavior. |
| `tests/test_quarantine_row_selection.py` | Created | Tests row selection behavior. |
| `tests/test_quarantine_row_selection.md` | Created | Documents row selection tests. |
| `log_protocol/11_CSV_quarantine_export/004_quarantine_row_selection.md` | Created | Records Stage D completion. |

---

## Behavior Added

```text
extract candidate row indexes
select quarantine rows
select accepted rows
avoid mutating original table
```

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_quarantine_row_selection.py
```

Status:

```text
Not executed by assistant in this environment.
```
