# type_caster.py

## Purpose

`type_caster.py` casts values based on each column's inferred type.

This module belongs to the cleaning layer, but it depends on schema metadata.

Architecture:

```text
Table + Inferred Column Types
→ Type Caster
→ Correctly Cast Table Values
```

---

# Why This Module Exists

Earlier cleaners were able to process every value.

That caused a problem:

```text
"1"
→ True
```

because the boolean cleaner interpreted `"1"` as a boolean value.

But in a column like:

```text
customer_id
```

the value should remain numeric:

```text
"1"
→ 1
```

The correct solution is:

```text
infer column type first
→ cast values according to column type
```

---

# Main Responsibility

The type caster decides which cleaner should handle each column.

Example:

```text
integer column
→ number cleaner

boolean column
→ boolean cleaner

date column
→ date cleaner

string column
→ no casting
```

---

# Main Functions

## `cast_table_by_schema(table)`

Casts all table values based on schema column types.

Flow:

```text
Table
→ iterate schema columns
→ cast each column
→ update rows
```

This function mutates the table in place.

---

## `cast_column_values(table, column)`

Casts all values in one column.

Uses:

```python
column.inferred_type
```

to decide how values should be cast.

---

## `cast_value_by_type(value, inferred_type)`

Casts one value according to a logical type.

Current type behavior:

| Inferred Type | Cleaner Used |
|---|---|
| `integer` | `normalize_integer()` |
| `float` | `normalize_float()` |
| `boolean` | `normalize_boolean()` |
| `date` | `normalize_date_or_datetime()` |
| `datetime` | `normalize_date_or_datetime()` |
| `string` | unchanged |
| `null` | unchanged |
| `unknown` | unchanged |

---

# Example

Before type casting:

```python
{
    "customer_id": "1",
    "active": "yes",
    "amount": "1,000"
}
```

Schema:

```python
customer_id.inferred_type = "integer"
active.inferred_type = "boolean"
amount.inferred_type = "integer"
```

After type casting:

```python
{
    "customer_id": 1,
    "active": True,
    "amount": 1000
}
```

---

# Corrected Pipeline Order

Recommended order:

```text
Parsing
→ Null Cleaning
→ Text Cleaning
→ Type Inference
→ Type-Aware Casting
→ Schema Metadata Inference
→ Quality Report
→ Export
```

---

# Important Design Principle

Do not apply all cleaners to all values.

Instead:

```text
infer type
→ choose correct cleaner
```

This is safer, more predictable, and easier to extend.

---

# Why This Helps Future Formats

CSV, Excel, and JSON can all become:

```text
Table
```

Then this module can cast values using the same logic.

This means future formats do not need separate casting systems.

---

# Developer Notes

This module should remain:

- format-independent
- schema-driven
- deterministic
- small
- easy to test

Do not add format-specific logic here.

---

# Current Limitations

Current implementation depends on:

```python
column.inferred_type
```

being set before casting.

If a column type is still:

```text
unknown
```

values are preserved unchanged.

---

# Future Improvements

Possible future additions:

- strict casting mode
- casting error reporting
- row quarantine for failed casts
- column-specific casting policies
- confidence-aware casting
- custom type handlers
- decimal support
- locale-aware casting