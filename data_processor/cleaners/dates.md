# dates.py

## Purpose

`dates.py` standardizes date-like and datetime-like values into Python date objects.

This module belongs to the cleaning layer.

Architecture:

```text
Raw Values
→ Date Cleaner
→ Standardized Date/Datetime Values
```

---

# Why Date Normalization Matters

Real-world datasets often store dates as text.

Examples:

```text
"2026-01-31"
"31.01.2026"
"2026/01/31"
"2026-01-31 14:30:00"
```

Without normalization:

- comparisons become unreliable
- sorting may be incorrect
- filtering becomes harder
- date calculations become difficult

Project standard:

```python
date
datetime
```

---

# Supported Formats

## Date Formats

Current supported date formats:

```text
%Y-%m-%d
%d.%m.%Y
%Y/%m/%d
```

Examples:

```text
2026-01-31
31.01.2026
2026/01/31
```

---

## Datetime Formats

Current supported datetime formats:

```text
%Y-%m-%d %H:%M:%S
%Y-%m-%dT%H:%M:%S
```

Examples:

```text
2026-01-31 14:30:00
2026-01-31T14:30:00
```

---

# Main Functions

## `normalize_date(value)`

Attempts to convert date-like strings into Python `date`.

Example:

```text
"2026-01-31"
→ date(2026, 1, 31)
```

Invalid values remain unchanged.

---

## `normalize_datetime(value)`

Attempts to convert datetime-like strings into Python `datetime`.

Example:

```text
"2026-01-31 14:30:00"
→ datetime(...)
```

Invalid values remain unchanged.

---

## `normalize_date_or_datetime(value)`

Generic date normalizer.

Behavior:

```text
try datetime first
→ if datetime fails, try date
→ if both fail, preserve original value
```

---

## `clean_table_dates(table)`

Applies date normalization across an entire table.

Behavior:

```text
mutates rows in place
```

Flow:

```text
Table
→ iterate rows
→ normalize dates
→ update rows
```

---

# Preserved Values

The cleaner preserves:

```python
None
existing date objects
existing datetime objects
```

It also preserves invalid strings:

```text
"Alice"
"Germany"
"31-31-2026"
```

---

# Important Design Principle

The date cleaner is allowed to cast values.

Example:

```text
"2026-01-31"
→ date(2026, 1, 31)
```

This differs from inference modules, which only detect likely types.

---

# Pipeline Position

Recommended pipeline order:

```text
Parsing
→ Null Cleaning
→ Text Cleaning
→ Boolean Cleaning
→ Number Cleaning
→ Date Cleaning
→ Type Inference
→ Validation
```

---

# Example

```python
from data_processor.cleaners.dates import clean_table_dates

clean_table_dates(table)
```

Before:

```python
{
    "created_at": "2026-01-31 14:30:00",
    "birth_date": "31.01.2026",
    "name": "Alice"
}
```

After:

```python
{
    "created_at": datetime(...),
    "birth_date": date(...),
    "name": "Alice"
}
```

---

# Developer Notes

This module should remain:

- deterministic
- explicit
- format-independent
- easy to test

Avoid locale-aware parsing too early.

---

# Current Limitations

Current implementation does not support:

```text
timezones
locale-aware dates
partial dates
natural language dates
UNIX timestamps
microseconds
custom parsing policies
```

---

# Future Improvements

Possible future additions:

- timezone-aware parsing
- locale-aware parsing
- configurable formats
- strict parsing mode
- date validation rules
- partial date support
- timestamp support
- parsing diagnostics