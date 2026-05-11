# test_numbers.py

## Purpose

Tests the number cleaning module.

This verifies that numeric-like string values are normalized into Python numeric types.

---

## Tested File

```text
data_processor/cleaners/numbers.py
```

---

## Current Test Coverage

### Basic integers

Verifies integer-like strings become `int`.

Examples:

```text
"100" → 100
" 42 " → 42
```

---

### US thousands separators

Verifies US-style commas are handled.

Example:

```text
"1,000" → 1000
```

---

### Underscore separators

Verifies underscores are removed before parsing.

Example:

```text
"1_000" → 1000
```

---

### Basic floats

Verifies float-like strings become `float`.

Examples:

```text
"100.5" → 100.5
" 42.25 " → 42.25
```

---

### US floats

Verifies US comma-separated floats are normalized.

Example:

```text
"1,000.50" → 1000.5
```

---

### European decimals

Verifies EU-style numeric strings are normalized.

Examples:

```text
"1.000,50" → 1000.5
"250,75" → 250.75
"5.500,00" → 5500.0
```

---

### Explicit format policies

Verifies explicit `number_format` policies.

Examples:

```python
normalize_number("1,000.50", number_format="us")
normalize_number("1.000,50", number_format="eu")
```

---

### Invalid values

Verifies invalid numeric values remain unchanged.

Examples:

```text
"Alice"
"100 EUR"
```

---

### Preserved values

Verifies these are preserved:

```python
None
True
False
```

---

### Table-wide normalization

Verifies `clean_table_numbers()` handles both US and EU-style numbers.

---

## Run Tests

```bash
python -m pytest tests/test_numbers.py
```

---

## Developer Notes

Number normalization should stay:

- deterministic
- explicit
- format-independent
- easy to test

Locale-aware behavior belongs in the cleaner layer, not the CSV adapter.
