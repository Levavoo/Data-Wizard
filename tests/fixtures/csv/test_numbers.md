# test_numbers.py

## Purpose

Tests the number cleaning module.

This verifies that numeric-like string values are normalized into Python numeric types.

Architecture:

```text
Raw Values
→ Number Cleaner
→ Standardized Numeric Values
```

---

# Tested File

```text
data_processor/cleaners/numbers.py
```

---

# Current Test Coverage

## `test_normalize_integer_basic`

Verifies integer-like strings become:

```python
int
```

Examples:

```text
"100"
" 42 "
```

---

## `test_normalize_integer_with_commas`

Verifies commas are removed before parsing.

Example:

```text
"1,000"
→ 1000
```

---

## `test_normalize_integer_with_underscores`

Verifies underscores are removed before parsing.

Example:

```text
"1_000"
→ 1000
```

---

## `test_normalize_float_basic`

Verifies float-like strings become:

```python
float
```

Examples:

```text
"100.5"
" 42.25 "
```

---

## `test_normalize_float_with_commas`

Verifies comma-separated floats are normalized.

Example:

```text
"1,000.50"
→ 1000.5
```

---

## `test_normalize_number_prefers_integer`

Verifies integer conversion is prioritized.

Example:

```text
"100"
→ 100
```

---

## `test_normalize_number_uses_float_when_needed`

Verifies float conversion is used when integer parsing fails.

Example:

```text
"100.25"
→ 100.25
```

---

## `test_preserve_invalid_values`

Verifies invalid numeric values remain unchanged.

Examples:

```text
"Alice"
"100 EUR"
```

---

## `test_preserve_none`

Verifies:

```python
None
```

remains unchanged.

---

## `test_preserve_booleans`

Verifies Python bool values remain unchanged.

Examples:

```python
True
False
```

---

## `test_clean_table_numbers`

Verifies table-wide number normalization.

Flow:

```text
Table
→ iterate rows
→ normalize numbers
→ update rows
```

---

# Important Design Rule

The number cleaner is allowed to cast values.

Example:

```text
"100"
→ 100
```

This differs from inference modules, which only detect likely types.

---

# Why Number Normalization Matters

Without normalization:

```text
"100"
"1,000"
"100.50"
```

would remain text values.

This causes problems for:

- sorting
- aggregation
- validation
- calculations
- statistics

---

# Run Tests

```powershell
pytest tests\test_numbers.py
```

Expected result:

```text
11 passed
```

---

# Recommended Validation Workflow

```powershell
ruff check data_processor\cleaners\numbers.py tests\test_numbers.py

black data_processor\cleaners\numbers.py tests\test_numbers.py

pytest tests\test_numbers.py
```

---

# Developer Notes

Number normalization should stay:

- deterministic
- explicit
- format-independent
- easy to test

Avoid adding locale-aware logic too early.

---

# Future Improvements

Possible future additions:

- locale-aware numbers
- Decimal support
- currency parsing
- percentages
- accounting formats
- scientific notation
- precision control