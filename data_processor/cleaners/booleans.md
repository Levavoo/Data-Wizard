# booleans.py

## Purpose

`booleans.py` standardizes boolean-like values into Python `bool`.

This module belongs to the cleaning layer.

Architecture:

```text
Raw Values
→ Boolean Cleaner
→ Standardized Boolean Values
```

---

# Why Boolean Normalization Matters

Real-world datasets often represent booleans inconsistently.

Examples:

```text
"yes"
"YES"
"true"
"1"
"on"

"no"
"FALSE"
"0"
"off"
```

Without normalization:

- filtering becomes inconsistent
- validation becomes unreliable
- aggregations become incorrect
- logical comparisons become harder

Project standard:

```python
True
False
```

---

# Main Functions

## `normalize_boolean(value)`

Normalizes one boolean-like value.

Examples:

```text
"yes"
→ True

"0"
→ False
```

Unrecognized values remain unchanged.

Example:

```text
"Alice"
→ "Alice"
```

---

## `clean_table_booleans(table)`

Applies boolean normalization to every value in a table.

Behavior:

```text
mutates rows in place
```

Flow:

```text
Table
→ iterate rows
→ normalize booleans
→ update rows
```

---

# Supported True Values

Current supported true representations:

```text
"true"
"yes"
"y"
"1"
"on"
```

Matching is:

- case-insensitive
- whitespace-trimmed

Example:

```text
" YES "
→ True
```

---

# Supported False Values

Current supported false representations:

```text
"false"
"no"
"n"
"0"
"off"
```

Example:

```text
" OFF "
→ False
```

---

# Example

```python
from data_processor.cleaners.booleans import clean_table_booleans

clean_table_booleans(table)
```

---

# Before Cleaning

```python
{
    "active": "YES",
    "verified": "0",
    "name": "Alice"
}
```

---

# After Cleaning

```python
{
    "active": True,
    "verified": False,
    "name": "Alice"
}
```

---

# Important Design Principle

Boolean normalization is isolated into a dedicated cleaner stage.

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

# Pipeline Position

Recommended pipeline order:

```text
Parsing
→ Null Cleaning
→ Text Cleaning
→ Boolean Cleaning
→ Type Inference
→ Validation
```

---

# Developer Notes

This module intentionally avoids:

- semantic interpretation
- category mapping
- schema logic
- validation rules
- type inference logic

It only standardizes boolean-like values.

---

# Future Improvements

Possible future additions:

- configurable boolean dictionaries
- locale-aware boolean values
- column-specific boolean policies
- strict boolean mode
- boolean statistics
- configurable preservation rules