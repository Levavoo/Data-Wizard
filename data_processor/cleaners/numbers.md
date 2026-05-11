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

## Supported Number Formats

The number cleaner supports these policies:

```text
auto
us
eu
```

Default:

```python
number_format="auto"
```

---

## US Format

Examples:

```text
1,000.50 → 1000.5
250.75   → 250.75
5,500.00 → 5500.0
```

Use explicitly:

```python
normalize_number("1,000.50", number_format="us")
```

---

## European Format

Examples:

```text
1.000,50 → 1000.5
250,75   → 250.75
5.500,00 → 5500.0
```

Use explicitly:

```python
normalize_number("1.000,50", number_format="eu")
```

---

## Auto Detection

Auto mode detects likely format from one value.

Rules:

```text
comma after dot → EU
comma with one or two decimal digits and no dot → EU
default fallback → US
```

Examples:

```text
1.000,50 → EU → 1000.5
250,75   → EU → 250.75
1,000.50 → US → 1000.5
```

Single-value auto detection cannot resolve every ambiguous case perfectly.

---

## Main Functions

### `normalize_integer(value, number_format="auto")`

Attempts to convert integer-like values into Python `int`.

Invalid values remain unchanged.

---

### `normalize_float(value, number_format="auto")`

Attempts to convert float-like values into Python `float`.

Invalid values remain unchanged.

---

### `normalize_number(value, number_format="auto")`

Generic number normalizer.

Behavior:

```text
try integer first
→ if integer fails, try float
→ if both fail, preserve original value
```

---

### `clean_table_numbers(table, number_format="auto")`

Applies number normalization to every value in a table.

Behavior:

```text
mutates rows in place
```

---

## Preserved Values

The cleaner preserves:

```python
None
True
False
```

It also preserves invalid strings:

```text
Alice
Germany
100 EUR
```

---

## Important Design Principle

The number cleaner is allowed to cast values.

Example:

```text
"100" → 100
```

This differs from inference modules, which only detect likely types.

Adapters must not parse numeric locale semantics.

---

## Pipeline Position

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

## Current Limitations

Not implemented yet:

```text
column-level number format detection
numeric parsing diagnostics
currency symbols
percentages
Decimal precision preservation
accounting formats
```

---

## Developer Notes

This module should remain:

- deterministic
- format-independent
- explicit
- easy to test

Locale-aware behavior is implemented in the cleaner layer, not the CSV adapter.
