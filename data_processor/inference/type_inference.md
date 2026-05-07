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

# Important Design Rule

Type inference only DETECTS types.

It does NOT:

- convert values
- clean values
- normalize values

Example:

```text
"123"
→ inferred as integer
```

But the stored value remains:

```text
"123"
```

This separation is intentional and architecturally important.

---

# Supported Logical Types

Current supported types:

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

# Main Functions

## `infer_table_types(table)`

Infers types for all columns inside a table.

Updates:

```python
column.inferred_type
```

Example:

```python
infer_table_types(table)
```

---

## `infer_column_type(values)`

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

Order matters.

Example:

```text
"1"
```

could be:

```text
integer
boolean
```

Current logic prioritizes:

```text
integer
```

---

# Helper Functions

## `is_null(value)`

Detects null-like values.

Supported null values:

```text
""
"null"
"none"
"n/a"
"na"
```

---

## `is_boolean(value)`

Detects boolean-like values.

Supported boolean values:

```text
true
false
yes
no
y
n
1
0
```

Case-insensitive.

---

## `is_integer(value)`

Checks whether integer parsing succeeds.

Example:

```text
"123"
→ True
```

---

## `is_float(value)`

Checks whether float parsing succeeds.

Example:

```text
"123.45"
→ True
```

---

## `is_date(value)`

Checks supported date formats.

Current formats:

```text
%Y-%m-%d
%d.%m.%Y
%Y/%m/%d
```

Examples:

```text
2026-01-01
01.01.2026
2026/01/01
```

---

## `is_datetime(value)`

Checks supported datetime formats.

Current formats:

```text
%Y-%m-%d %H:%M:%S
%Y-%m-%dT%H:%M:%S
```

Examples:

```text
2026-01-01 14:30:00
2026-01-01T14:30:00
```

---

# Example

```python
from data_processor.inference.type_inference import infer_table_types

infer_table_types(table)

for column in table.schema.columns:
    print(column.name, column.inferred_type)
```

---

# Developer Notes

This module should stay deterministic and explicit.

Avoid:

- hidden coercion
- automatic conversions
- locale assumptions
- pandas inference behavior

The pipeline should remain transparent.

---

# Architectural Role

Pipeline position:

```text
CSV
→ Table
→ Type Inference
→ Cleaning
→ Validation
→ Transformation
→ Export
```

---

# Current Limitations

Current implementation does not support:

- decimal precision
- locale-aware numbers
- currency detection
- timezone-aware datetimes
- scientific notation rules
- UUID detection
- email detection
- categorical inference

---

# Future Improvements

Possible future additions:

- confidence scoring
- mixed-type detection
- probabilistic inference
- locale-aware parsing
- configurable type policies
- custom inference plugins
- type statistics
- sampling for large datasets