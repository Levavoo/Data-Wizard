# type_inference.py

## Purpose

`type_inference.py` detects likely logical types from raw table values.

This module belongs to the inference layer.

Architecture:

```text
Raw Table Values
→ Type Inference
→ Schema Type Metadata
```

---

## Important Design Rule

Type inference only detects types.

It does not:

- convert values
- clean values
- normalize values

Example:

```text
"123" → inferred as integer
```

The stored value remains:

```text
"123"
```

---

## Supported Logical Types

```text
null
boolean
integer
float
date
datetime
string
```

---

## Numeric Inference

Numeric inference uses the same locale-aware numeric string preparation as the number cleaner.

Supported number format behavior:

```text
auto-detect US/EU-style numeric strings
preserve original values during inference
only use cleaned representation for detection
```

Examples detected as numeric:

```text
1,000.50
1.000,50
250,75
5.500,00
```

---

## Main Functions

### `infer_table_types(table)`

Infers types for all columns inside a table.

Updates:

```python
column.inferred_type
```

---

### `infer_column_type(values)`

Infers the most likely type for one column.

Detection order:

```text
null
→ boolean
→ integer
→ float
→ datetime
→ date
→ string
```

---

## Helper Functions

### `clean_numeric_string(value)`

Prepares a numeric string for inference using locale-aware auto mode.

It does not mutate the source value.

---

### `is_integer(value)`

Checks whether integer parsing succeeds.

---

### `is_float(value)`

Checks whether float parsing succeeds.

---

### `is_date(value)`

Checks supported date formats.

---

### `is_datetime(value)`

Checks supported datetime formats.

---

## Developer Notes

This module should stay deterministic and explicit.

Avoid:

- hidden coercion
- automatic value mutation
- pandas inference behavior

The pipeline should remain transparent.

---

## Current Limitations

Current implementation does not support:

- decimal precision
- currency detection
- timezone-aware datetimes
- scientific notation policies
- UUID detection
- email detection
- categorical inference
- mixed-type diagnostics

---

## Future Improvements

Possible future additions:

- confidence scoring
- mixed-type detection
- probabilistic inference
- configurable type policies
- custom inference plugins
- type statistics
- sampling for large datasets
