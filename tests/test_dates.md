# test_dates.py

## Purpose

Tests the date cleaning module.

This verifies that date-like and datetime-like string values are normalized into Python date objects.

Architecture:

```text
Raw Values
→ Date Cleaner
→ Standardized Date/Datetime Values
```

---

# Tested File

```text
data_processor/cleaners/dates.py
```

---

# Current Test Coverage

## `test_normalize_iso_date`

Verifies ISO date parsing.

Example:

```text
"2026-01-31"
→ date(2026, 1, 31)
```

---

## `test_normalize_european_date`

Verifies European date parsing.

Example:

```text
"31.01.2026"
→ date(2026, 1, 31)
```

---

## `test_normalize_slash_date`

Verifies slash-separated date parsing.

Example:

```text
"2026/01/31"
→ date(2026, 1, 31)
```

---

## `test_normalize_datetime`

Verifies datetime parsing.

Example:

```text
"2026-01-31 14:30:00"
→ datetime(...)
```

---

## `test_normalize_iso_datetime`

Verifies ISO datetime parsing.

Example:

```text
"2026-01-31T14:30:00"
→ datetime(...)
```

---

## `test_normalize_date_or_datetime_prefers_datetime`

Verifies datetime parsing has priority over date parsing.

---

## `test_preserve_invalid_values`

Verifies invalid values remain unchanged.

Examples:

```text
"Alice"
"not-a-date"
```

---

## `test_preserve_none`

Verifies:

```python
None
```

remains unchanged.

---

## `test_preserve_existing_date_objects`

Verifies existing `date` objects remain unchanged.

---

## `test_preserve_existing_datetime_objects`

Verifies existing `datetime` objects remain unchanged.

---

## `test_clean_table_dates`

Verifies table-wide date normalization.

Flow:

```text
Table
→ iterate rows
→ normalize dates
→ update rows
```

---

# Important Design Rule

The date cleaner is allowed to cast values.

Example:

```text
"2026-01-31"
→ date(2026, 1, 31)
```

This differs from inference modules, which only detect likely types.

---

# Why Date Normalization Matters

Without normalization:

```text
"2026-01-31"
"31.01.2026"
```

remain text values.

This causes problems for:

- sorting
- filtering
- date calculations
- validation
- comparisons

---

# Run Tests

```powershell
pytest tests\test_dates.py
```

Expected result:

```text
11 passed
```

---

# Recommended Validation Workflow

```powershell
ruff check data_processor\cleaners\dates.py tests\test_dates.py

black data_processor\cleaners\dates.py tests\test_dates.py

pytest tests\test_dates.py
```

---

# Developer Notes

Date normalization should stay:

- deterministic
- explicit
- format-independent
- easy to test

Avoid locale-aware parsing too early.

---

# Future Improvements

Possible future additions:

- timezone support
- locale-aware formats
- UNIX timestamps
- microseconds
- partial dates
- configurable parsing policies
- parsing diagnostics