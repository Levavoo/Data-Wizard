# test_nulls.py

## Purpose

Tests the null cleaning module.

This verifies that inconsistent missing-value representations are normalized into Python `None`.

Architecture:

```text
Raw Values
→ Null Cleaner
→ Standardized Missing Values
```

---

# Tested File

```text
data_processor/cleaners/nulls.py
```

---

# Current Test Coverage

## `test_normalize_empty_string`

Verifies:

```text
""
→ None
```

---

## `test_normalize_null_string`

Verifies textual null representations.

Examples:

```text
"null"
"NULL"
" None "
```

Expected result:

```python
None
```

---

## `test_normalize_na_values`

Verifies NA-style placeholders.

Examples:

```text
"n/a"
"NA"
" nan "
```

Expected result:

```python
None
```

---

## `test_preserve_regular_values`

Verifies valid values remain unchanged.

Examples:

```text
"Alice"
"Germany"
```

---

## `test_preserve_non_string_values`

Verifies non-string values are not modified.

Examples:

```python
123
True
```

---

## `test_clean_table_nulls`

Verifies table-wide null cleaning.

Flow:

```text
Table
→ iterate rows
→ normalize values
→ update rows
```

---

# Important Design Rule

The cleaner layer is allowed to modify values.

Example:

```text
"N/A"
→ None
```

This differs from inference modules, which only detect metadata.

---

# Why This Matters

Consistent null handling improves:

- validation
- filtering
- aggregation
- statistics
- schema consistency
- type casting reliability

Without normalization:

```text
""
"null"
"N/A"
```

would all behave differently.

---

# Run Tests

```powershell
pytest
```

Expected result:

```text
all tests pass
```

---

# Developer Notes

Null normalization should happen early in the cleaning pipeline.

Recommended order:

```text
Parsing
→ Null Cleaning
→ Type Inference
→ Value Cleaning
→ Validation
```

---

# Future Improvements

Possible future additions:

- configurable null dictionaries
- column-specific null rules
- whitespace-only policies
- statistics tracking
- quarantine handling
- locale-aware null values