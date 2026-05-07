# nulls.py

## Purpose

`nulls.py` standardizes null-like values into Python `None`.

This module belongs to the cleaning layer.

Architecture:

```text
Raw Values
→ Null Cleaner
→ Standardized Missing Values
```

---

# Why Null Normalization Matters

Real-world datasets often represent missing values inconsistently.

Examples:

```text
""
"null"
"NULL"
"None"
"N/A"
"na"
"-"
```

Without normalization:

- validation becomes inconsistent
- type inference becomes unreliable
- aggregations become incorrect
- filtering becomes harder

The project standard is:

```python
None
```

---

# Main Functions

## `normalize_null(value)`

Normalizes one value.

Examples:

```text
""       → None
"null"   → None
" NA "   → None
"-"      → None
```

Non-null values remain unchanged.

Example:

```text
"Alice"
→ "Alice"
```

---

## `clean_table_nulls(table)`

Applies null normalization to every value in the table.

Behavior:

```text
mutates rows in place
```

Example flow:

```text
Table
→ iterate rows
→ iterate values
→ normalize nulls
```

---

# Supported Null Values

Current supported null representations:

```text
""
"null"
"none"
"n/a"
"na"
"nan"
"-"
```

Matching is:

- case-insensitive
- whitespace-trimmed

Example:

```text
" N/A "
→ None
```

---

# Example

```python
from data_processor.cleaners.nulls import clean_table_nulls

clean_table_nulls(table)
```

---

# Before Cleaning

```python
{
    "country": "",
    "email": "N/A",
    "name": "Alice"
}
```

---

# After Cleaning

```python
{
    "country": None,
    "email": None,
    "name": "Alice"
}
```

---

# Important Design Principle

Null cleaning is one dedicated pipeline stage.

This keeps responsibilities separated:

```text
Adapter
→ parsing

Inference
→ detection

Cleaner
→ modification

Validator
→ rule checking
```

---

# Developer Notes

This module intentionally avoids:

- type conversion
- value casting
- schema logic
- validation logic

It only normalizes missing values.

---

# Future Improvements

Possible future additions:

- configurable null policies
- column-specific null rules
- whitespace-only policies
- locale-aware null values
- null statistics
- row quarantine support
- configurable placeholder handling