# text.py

## Purpose

`text.py` provides generic text normalization utilities.

This module belongs to the cleaning layer.

Architecture:

```text
Raw Text Values
→ Text Cleaner
→ Normalized Text Values
```

---

# Main Responsibilities

The text cleaner handles:

- trimming surrounding whitespace
- collapsing repeated internal whitespace
- optional casing normalization
- preserving `None`
- preserving non-string values

---

# What This Module Does Not Do

This module does not handle:

- category mapping
- translation
- spell correction
- semantic normalization
- fuzzy matching
- locale-specific casing
- Unicode transliteration

Those features belong to later specialized modules.

---

# Main Functions

## `normalize_text(value, case=None)`

Normalizes one value.

If the value is a string:

```text
trim whitespace
→ collapse repeated whitespace
→ optionally apply casing
```

If the value is not a string, it is returned unchanged.

---

# Supported Case Options

| Option | Behavior |
|---|---|
| `None` | Preserve original casing |
| `"lower"` | Convert to lowercase |
| `"upper"` | Convert to uppercase |
| `"title"` | Convert to title case |

---

# Examples

## Trim Whitespace

```text
" Alice "
→ "Alice"
```

---

## Collapse Repeated Whitespace

```text
"hello     world"
→ "hello world"
```

---

## Lowercase

```text
"GERMANY"
→ "germany"
```

---

## Uppercase

```text
"de"
→ "DE"
```

---

## Preserve None

```python
None
→ None
```

---

## Preserve Non-String Values

```python
123
→ 123
```

---

# `clean_table_text(table, case=None)`

Applies text normalization to every value in a table.

Behavior:

```text
mutates rows in place
```

Example:

```python
from data_processor.cleaners.text import clean_table_text

clean_table_text(table, case="lower")
```

---

# Before Cleaning

```python
{
    "name": " Alice ",
    "country": " GERMANY ",
    "note": "hello     world"
}
```

---

# After Cleaning With `case=None`

```python
{
    "name": "Alice",
    "country": "GERMANY",
    "note": "hello world"
}
```

---

# After Cleaning With `case="lower"`

```python
{
    "name": "alice",
    "country": "germany",
    "note": "hello world"
}
```

---

# Important Design Principle

Text cleaning is generic.

It should not make business-specific assumptions.

Example:

```text
"DE"
```

should not automatically become:

```text
"Germany"
```

That belongs to category standardization later.

---

# Pipeline Position

Recommended early pipeline order:

```text
Parsing
→ Null Cleaning
→ Text Cleaning
→ Type Inference
→ Validation
```

---

# Developer Notes

This module is intentionally small.

Keep it focused on text-level cleanup only.

Avoid adding:

- country normalization
- currency normalization
- product/category mapping
- business rules
- language detection

---

# Future Improvements

Possible future additions:

- Unicode normalization
- configurable whitespace rules
- column-specific casing rules
- punctuation cleanup
- invisible character removal
- configurable text policies