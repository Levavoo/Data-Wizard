# Protocol — <Short Change Title>

## Metadata

| Field | Value |
|---|---|
| Plan | docs/0805_improvement_plan_csv.md |
| Stage | Stage 08 / CSV Improvement Plan |
| Branch | codex |
| Protocol ID | 0805-001 |
| Date | YYYY-MM-DD |
| Status | Completed |
| Commit | <commit-hash-or-pending> |

---

## 1. Purpose

Describe why this change was made.

Example:

This change improves CSV header normalization so imported column names are stable, predictable, and compatible with the canonical `Table` model.

---

## 2. Scope

### Included

- Changed CSV header normalization logic
- Added handling for duplicate normalized headers
- Updated module documentation

### Not Included

- Excel support
- JSON support
- Transformation engine changes
- Constraint engine changes

---

## 3. Changed Files

| File | Action | Reason |
|---|---|---|
| `data_processor/adapters/csv_adapter.py` | Modified | Improved header normalization |
| `data_processor/adapters/csv_adapter.md` | Modified | Documented new behavior |
| `tests/test_csv_adapter.py` | Modified | Added regression tests |

Actions:

```text
Created
Modified
Renamed
Deleted