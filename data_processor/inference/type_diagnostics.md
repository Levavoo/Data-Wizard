# type_diagnostics.py

## Purpose

`type_diagnostics.py` analyzes type evidence without mutating values or changing schema inference.

It belongs to the inference/reporting boundary.

Architecture:

```text
Table values
→ Type evidence analysis
→ Mixed-type diagnostics
→ Diagnostic bundle
```

---

## Main Functions

### `analyze_column_type_evidence(values, column_name, threshold=0.8)`

Analyzes one column and returns a diagnostic dictionary.

Returned fields include:

```text
column
dominant_type
total_values
non_null_count
null_count
valid_count
invalid_count
candidate_counts
invalid_values
is_mixed_type
```

---

### `analyze_table_type_evidence(table, threshold=0.8)`

Analyzes all columns in a table.

Returned fields:

```text
columns
mixed_type_columns
```

---

## Dominant Type Logic

The default dominant-type threshold is:

```text
0.8
```

Null values are ignored for dominance and invalid-value calculation.

Example:

```text
100
250.75
unknown
300
400
```

Result:

```text
dominant_type = float
invalid value = unknown
```

---

## Design Rules

This module must not:

- mutate table values
- set schema inferred types
- cast values
- quarantine rows
- validate constraints

It only reports type evidence.

---

## Current Scope

Supported diagnostic candidates:

```text
boolean
integer
float
datetime
date
```

Text values are treated as invalid only when another dominant type exists.

---

## Future Improvements

Possible future additions:

- configurable dominance threshold
- column-level type policy
- richer date/datetime diagnostics
- diagnostics export as CSV issue files
- integration with quarantine candidates
