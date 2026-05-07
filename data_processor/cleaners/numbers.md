# numbers.py

## Purpose

`numbers.py` standardizes numeric-like values into Python numeric types.

This module belongs to the cleaning layer.

Architecture:

```text
Raw Values
→ Number Cleaner
→ Standardized Numeric Values
```

---

# Why Number Normalization Matters

Real-world datasets often represent numbers as text.

Examples:

```text
"100"
"100.50"
" 1,000 "
"1_000"
```

Without normalization:

- sorting can be incorrect
- numeric validation becomes harder
- aggregation becomes unreliable
- calculations may fail

Project standard:

```python
int
float
```

---

# Main Functions

## `normalize_integer(value)`

Attempts to convert integer-like values into Python `int`.

Examples:

```text
"100"
→ 100

" 1,000 "
→ 1000

"1_000"
→ 1000
```

Invalid values remain unchanged.

Example:

```text
"Alice"
→ "Alice"
```

---

## `normalize_float(value)`

Attempts to convert float-like values into Python `float`.

Examples:

```text
"100.50"
→ 100.5

" 1,000.25 "
→ 1000.25
```

Invalid values remain unchanged.

---

## `normalize_number(value)`

Generic number normalizer.

Behavior:

```text
try integer first
→ if integer fails, try float
→ if both fail, preserve original value
```

Examples:

```text
"100"
→ 100

"100.50"
→ 100.5

"Alice"
→ "Alice"
```

---

## `clean_table_numbers(table)`

Applies number normalization to every value in a table.

Behavior:

```text
mutates rows in place
```

Flow:

```text
Table
→ iterate rows
→ normalize numbers
→ update rows
```

---

# Helper Functions

## `_clean_numeric_string(value)`

Prepares string values for numeric parsing.

Current cleanup:

```text
trim whitespace
remove commas
remove underscores
```

Examples:

```text
" 1,000 "
→ "1000"

"1_000"
→ "1000"
```

---

# Preserved Values

The cleaner preserves:

```python
None
True
False
```

It also preserves invalid strings:

```text
"Alice"
"Germany"
"100 EUR"
```

---

# Important Design Principle

The number cleaner is allowed to cast values.

Example:

```text
"100"
→ 100
```

This differs from inference modules, which only detect likely types.

---

# Current Scope

Supported:

```text
integers
floats
commas
underscores
surrounding whitespace
existing int values
existing float values
None values
```

Not supported yet:

```text
locale-aware numbers
currency symbols
percentages
scientific notation policies
decimal precision control
accounting formats
```

---

# Pipeline Position

Recommended pipeline order:

```text
Parsing
→ Null Cleaning
→ Text Cleaning
→ Boolean Cleaning
→ Number Cleaning
→ Type Inference
→ Validation
```

---

# Example

```python
from data_processor.cleaners.numbers import clean_table_numbers

clean_table_numbers(table)
```

Before:

```python
{
    "quantity": "1,000",
    "price": "25.50",
    "name": "Alice"
}
```

After:

```python
{
    "quantity": 1000,
    "price": 25.5,
    "name": "Alice"
}
```

---

# Developer Notes

This module should remain:

- deterministic
- format-independent
- explicit
- easy to test

Avoid adding locale or currency logic here too early.

Those should be separate specialized features later.

---

# Future Improvements

Possible future additions:

- locale-aware parsing
- currency normalization
- percentage parsing
- Decimal support
- strict parsing mode
- column-specific numeric policies
- numeric error reporting
- precision preservation