# test_type_inference.py

## Purpose

Tests the basic type inference module.

This verifies that raw string values can be inspected and classified without converting them.

---

# Tested File

```text
data_processor/inference/type_inference.py
```

---

# Current Test Coverage

## `test_infer_null_column`

Verifies null-like values are detected as:

```text
null
```

Examples:

```text
""
"null"
"None"
"n/a"
```

---

## `test_infer_boolean_column`

Verifies boolean-like values are detected as:

```text
boolean
```

Examples:

```text
true
FALSE
yes
no
```

---

## `test_infer_integer_column`

Verifies integer-like values are detected as:

```text
integer
```

Example:

```text
"300"
```

---

## `test_infer_float_column`

Verifies decimal values are detected as:

```text
float
```

Example:

```text
"300.75"
```

---

## `test_infer_date_column`

Verifies supported date formats are detected as:

```text
date
```

Examples:

```text
2026-01-01
01.02.2026
2026/03/01
```

---

## `test_infer_datetime_column`

Verifies supported datetime formats are detected as:

```text
datetime
```

Examples:

```text
2026-01-01 10:30:00
2026-01-02T11:45:00
```

---

## `test_infer_string_column`

Verifies normal text values are detected as:

```text
string
```

---

## `test_infer_table_types_updates_schema_columns`

Verifies that:

```text
infer_table_types(table)
```

updates:

```text
column.inferred_type
```

inside the table schema.

---

# Important Design Rule

These tests confirm that type inference does not clean or convert data.

Example:

```text
"1"
```

may be inferred as:

```text
integer
```

but it remains stored as:

```text
"1"
```

Actual conversion happens later in cleaner/caster modules.

---

# Run Tests

```powershell
pytest
```

---

# Developer Notes

Type inference should stay:

- deterministic
- explicit
- easy to test
- independent from file formats

Avoid hidden behavior from libraries such as pandas.

---

# Existing Python Value Support

Type inference supports both raw string values and already-cleaned Python values.

This is important because the pipeline runs inference twice:

```text
before casting
after casting
```

Before casting:

```text
"1"
→ integer
"yes"
→ boolean
```

After casting:

```python
1
→ integer

True
→ boolean
```

Supported cleaned Python values:

| Python Value | Inferred Type |
|---|---|
| `bool` | `boolean` |
| `int` | `integer` |
| `float` | `float` |
| `date` | `date` |
| `datetime` | `datetime` |
| `None` | ignored as null |

Important:

```python
bool
```

is checked before:

```python
int
```

because in Python:

```python
isinstance(True, int)
```

returns:

```python
True
```

So booleans must be handled explicitly to avoid treating `True` and `False` as `1` and `0`.