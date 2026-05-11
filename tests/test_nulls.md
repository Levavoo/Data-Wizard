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

## Tested File

```text
data_processor/cleaners/nulls.py
```

---

## Current Test Coverage

### `test_normalize_empty_string`

Verifies:

```text
"" → None
```

---

### `test_normalize_whitespace_only_strings`

Verifies whitespace-only values become `None`.

Examples:

```text
"   "
"\t"
"\n"
" \t \n "
```

---

### `test_normalize_null_string`

Verifies textual null representations.

Examples:

```text
"null"
"NULL"
" None "
```

---

### `test_normalize_na_values`

Verifies NA-style placeholders.

Examples:

```text
"n/a"
"NA"
" nan "
```

---

### `test_normalize_extended_null_tokens`

Verifies conservative extended null tokens.

Examples:

```text
"#N/A" → None
" NIL " → None
"--" → None
"?" → None
"not available" → None
"NOT AVAILABLE" → None
"not_applicable" → None
```

---

### `test_preserve_ambiguous_null_like_values`

Verifies ambiguous tokens remain normal values by default.

Examples:

```text
"unknown" → "unknown"
"missing" → "missing"
```

---

### `test_preserve_regular_values`

Verifies valid values remain unchanged.

Examples:

```text
"Alice"
"Germany"
```

---

### `test_preserve_non_string_values`

Verifies non-string values are not modified.

Examples:

```python
123
True
```

---

### `test_clean_table_nulls`

Verifies table-wide null cleaning.

---

### `test_clean_table_nulls_handles_whitespace_only_cells`

Verifies table-wide null cleaning also converts whitespace-only strings to `None`.

---

### `test_clean_table_nulls_handles_extended_tokens`

Verifies table-wide null cleaning handles conservative extended null tokens.

---

## Important Design Rule

The cleaner layer is allowed to modify values.

Example:

```text
"N/A" → None
```

This differs from inference modules, which only detect metadata.

---

## Why This Matters

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
"#N/A"
"NIL"
"--"
"?"
"   "
```

would all behave differently.

---

## Run Tests

```bash
python -m pytest tests/test_nulls.py
```

Expected result:

```text
all tests pass
```

---

## Developer Notes

Null normalization should happen early in the cleaning pipeline.

Recommended order:

```text
Parsing
→ Null Cleaning
→ Text Cleaning
→ Type Inference
→ Type-Aware Casting
→ Validation
```

Ambiguous values such as `unknown` and `missing` are intentionally preserved until configurable cleaning profiles exist.

---

## Future Improvements

Possible future additions:

- configurable null dictionaries
- column-specific null rules
- statistics tracking
- quarantine handling
- locale-aware null values
