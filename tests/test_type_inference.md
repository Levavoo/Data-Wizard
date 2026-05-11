# test_type_inference.py

## Purpose

Tests the type inference module.

This verifies that raw values can be inspected and classified without converting them.

---

## Tested File

```text
data_processor/inference/type_inference.py
```

---

## Current Test Coverage

### Null columns

Verifies null-like values are detected as:

```text
null
```

---

### Boolean columns

Verifies boolean-like values are detected as:

```text
boolean
```

---

### Integer columns

Verifies integer-like values are detected as:

```text
integer
```

---

### Float columns

Verifies decimal values are detected as:

```text
float
```

Examples:

```text
1.5
2.0
300.75
```

---

### European float columns

Verifies EU-style decimal values are detected as:

```text
float
```

Examples:

```text
1.000,50
250,75
5.500,00
```

---

### Date and datetime columns

Verifies supported date and datetime formats are detected correctly.

---

### Existing Python values

Type inference supports both raw strings and already-cleaned Python values.

Supported cleaned Python values:

| Python Value | Inferred Type |
|---|---|
| `bool` | `boolean` |
| `int` | `integer` |
| `float` | `float` |
| `date` | `date` |
| `datetime` | `datetime` |
| `None` | ignored as null |

---

## Important Design Rule

These tests confirm that type inference does not clean or convert data.

Example:

```text
"1.000,50"
```

may be inferred as:

```text
float
```

but it remains stored as:

```text
"1.000,50"
```

Actual conversion happens later in cleaner/caster modules.

---

## Run Tests

```bash
python -m pytest tests/test_type_inference.py
```

---

## Developer Notes

Type inference should stay:

- deterministic
- explicit
- easy to test
- independent from file formats

Avoid hidden behavior from libraries such as pandas.
