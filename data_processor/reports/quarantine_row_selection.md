# quarantine_row_selection.py

## Purpose

`quarantine_row_selection.py` selects quarantine rows and accepted rows from a `Table` using existing quarantine candidate row indexes.

It belongs to the report/selection layer.

Architecture:

```text
Table + quarantine_candidates
→ row selection utilities
→ quarantine Table / accepted Table
```

---

## Main Functions

### `get_quarantine_row_indexes(quarantine_candidates)`

Returns a set of zero-based row indexes from the candidate report.

---

### `select_quarantine_rows(table, quarantine_candidates)`

Returns a new `Table` containing only rows listed as quarantine candidates.

---

### `select_accepted_rows(table, quarantine_candidates)`

Returns a new `Table` containing rows not listed as quarantine candidates.

---

## Behavior

The utility:

```text
uses zero-based row indexes
copies row dictionaries
preserves schema reference
copies metadata dictionary
returns new Table objects
```

---

## Design Rules

This module must not:

- mutate the original table
- write files
- build quarantine candidates
- change candidate severity
- change default CSV export behavior

File writing belongs to exporters.
