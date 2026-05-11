# row_classification.py

## Purpose

`row_classification.py` classifies suspicious rows for diagnostics.

This module belongs to the analysis layer.

Architecture:

```text
Table rows
→ Row classification
→ Suspicious row diagnostics
→ Diagnostic bundle
```

---

## Main Functions

### `classify_row(row, row_index)`

Classifies one row.

Returned fields:

```text
row_index
classification
reason
confidence
row
```

---

### `classify_table_rows(table)`

Classifies all rows in a table.

Returned fields:

```text
rows
suspicious_rows
summary
```

---

## Classifications

Current classifications:

```text
normal_row
empty_row
comment_row
summary_row
footer_row
garbage_row
```

---

## Heuristics

### `empty_row`

All values are `None` or empty strings.

### `comment_row`

First non-empty value starts with:

```text
#
//
;
```

### `summary_row`

First non-empty value starts with:

```text
TOTAL
SUM
SUBTOTAL
GRAND TOTAL
```

### `footer_row`

First non-empty value contains:

```text
END OF
GENERATED
EXPORT COMPLETE
REPORT GENERATED
```

### `garbage_row`

Only one value is populated in a multi-column row.

---

## Design Rules

This module must not:

- mutate rows
- remove rows
- quarantine rows
- repair values
- validate constraints
- export files

It only reports suspicious row classifications.

---

## Current Limitations

The heuristics are intentionally conservative and simple.

Future improvements may include:

- configurable row classification rules
- confidence tuning
- source-row index mapping
- quarantine candidate integration
- suspicious row report export
