# test_text.py

## Purpose

Tests the text cleaning module.

This verifies that generic text normalization works correctly.

Architecture:

```text
Raw Text
→ Text Cleaner
→ Normalized Text
```

---

# Tested File

```text
data_processor/cleaners/text.py
```

---

# Current Test Coverage

## `test_trim_whitespace`

Verifies surrounding whitespace is removed.

Example:

```text
" Alice "
→ "Alice"
```

---

## `test_collapse_repeated_whitespace`

Verifies repeated internal whitespace is collapsed.

Example:

```text
"hello     world"
→ "hello world"
```

---

## `test_lowercase_normalization`

Verifies lowercase normalization.

Example:

```text
"GERMANY"
→ "germany"
```

---

## `test_uppercase_normalization`

Verifies uppercase normalization.

Example:

```text
"de"
→ "DE"
```

---

## `test_titlecase_normalization`

Verifies title case normalization.

Example:

```text
"john doe"
→ "John Doe"
```

---

## `test_preserve_none`

Verifies `None` values are preserved.

Example:

```python
None
→ None
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

## `test_invalid_case_option`

Verifies unsupported case options raise:

```python
ValueError
```

This ensures deterministic behavior.

---

## `test_clean_table_text`

Verifies table-wide text normalization.

Flow:

```text
Table
→ iterate rows
→ normalize text
→ update rows
```

---

# Important Design Rule

The text cleaner performs generic normalization only.

It should not:

- translate values
- map categories
- infer meaning
- apply business rules

Example:

```text
"DE"
```

should NOT automatically become:

```text
"Germany"
```

---

# Run Tests

```powershell
pytest tests\test_text.py
```

Expected result:

```text
9 passed
```

---

# Recommended Validation Workflow

```powershell
ruff check data_processor\cleaners\text.py tests\test_text.py

black data_processor\cleaners\text.py tests\test_text.py

pytest tests\test_text.py
```

---

# Developer Notes

Text normalization should stay:

- deterministic
- transparent
- configurable
- format-independent

Avoid hidden assumptions or semantic interpretation.

---

# Future Improvements

Possible future additions:

- Unicode normalization
- configurable punctuation cleanup
- locale-aware casing
- invisible character removal
- column-specific policies