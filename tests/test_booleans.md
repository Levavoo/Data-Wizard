# test_booleans.py

## Purpose

Tests the boolean cleaning module.

This verifies that inconsistent boolean representations are normalized into Python `bool` values.

Architecture:

```text
Raw Values
→ Boolean Cleaner
→ Standardized Boolean Values
```

---

# Tested File

```text
data_processor/cleaners/booleans.py
```

---

# Current Test Coverage

## `test_normalize_true_values`

Verifies true-like values become:

```python
True
```

Examples:

```text
"true"
"YES"
" y "
"1"
"ON"
```

---

## `test_normalize_false_values`

Verifies false-like values become:

```python
False
```

Examples:

```text
"false"
"NO"
" n "
"0"
"OFF"
```

---

## `test_preserve_none`

Verifies:

```python
None
```

remains unchanged.

---

## `test_preserve_existing_boolean_values`

Verifies existing Python bool values remain unchanged.

Examples:

```python
True
False
```

---

## `test_preserve_non_boolean_strings`

Verifies unrelated strings are preserved.

Examples:

```text
"Alice"
"Germany"
```

---

## `test_preserve_non_string_values`

Verifies non-string values remain unchanged.

Examples:

```python
123
45.6
```

---

## `test_clean_table_booleans`

Verifies table-wide boolean normalization.

Flow:

```text
Table
→ iterate rows
→ normalize booleans
→ update rows
```

---

# Important Design Rule

The boolean cleaner modifies values.

Example:

```text
"YES"
→ True
```

This differs from inference modules, which only detect metadata.

---

# Why Boolean Normalization Matters

Without normalization:

```text
"yes"
"YES"
"1"
"true"
```

would all behave differently.

Standardizing values improves:

- filtering
- validation
- aggregation
- consistency
- downstream processing

---

# Run Tests

```powershell
pytest tests\test_booleans.py
```

Expected result:

```text
7 passed
```

---

# Recommended Validation Workflow

```powershell
ruff check data_processor\cleaners\booleans.py tests\test_booleans.py

black data_processor\cleaners\booleans.py tests\test_booleans.py

pytest tests\test_booleans.py
```

---

# Developer Notes

Boolean normalization should stay:

- deterministic
- explicit
- configurable
- format-independent

Avoid hidden semantic assumptions.

---

# Future Improvements

Possible future additions:

- locale-aware booleans
- configurable dictionaries
- strict parsing mode
- column-specific policies
- statistics tracking
- ambiguity detection