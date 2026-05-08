# test_row_profile.py

## Purpose

Tests the row profiling module.

This verifies that row-level quality statistics are generated correctly.

Architecture:

```text
Table
→ Row Profiler
→ Row Quality Profiles
```

---

# Tested File

```text
data_processor/analysis/row_profile.py
```

---

# Current Test Coverage

## `test_calculate_ratio`

Verifies safe ratio calculation.

---

## `test_calculate_ratio_zero_division`

Verifies division-by-zero protection.

Expected:

```python
0.0
```

---

## `test_count_missing_values`

Verifies missing values are counted correctly.

Missing values are:

```python
None
```

---

## `test_create_row_signature`

Verifies deterministic row signatures.

This is important for duplicate detection.

---

## `test_find_duplicate_signatures`

Verifies duplicate row candidates are detected.

Rows with identical key/value pairs should produce the same signature.

---

## `test_profile_row_complete`

Verifies complete row profile generation.

Checks:

- row index
- missing values
- non-null values
- duplicate detection
- empty row detection

---

## `test_profile_empty_row`

Verifies fully empty rows are detected.

An empty row means:

```python
all expected schema values are None
```

---

## `test_profile_all_rows`

Verifies complete table profiling.

---

# Important Design Rule

Row profiling is analysis only.

This module must never:

- modify rows
- delete rows
- quarantine rows
- clean values
- validate business rules

---

# Run Tests

```powershell
pytest tests\test_row_profile.py
```

Expected:

```text
8 passed
```

---

# Recommended Validation Workflow

```powershell
ruff check `
    data_processor\analysis\row_profile.py `
    tests\test_row_profile.py

black `
    data_processor\analysis\row_profile.py `
    tests\test_row_profile.py

pytest tests\test_row_profile.py
```

---

# Developer Notes

Row profiling is a foundational diagnostic layer.

Later systems will use it for:

- quarantine workflows
- anomaly detection
- migration diagnostics
- repair suggestions
- quality scoring

---

# Future Improvements

Possible future additions:

- row quality scoring
- anomaly detection
- repair hints
- constraint diagnostics
- lineage tracking
- row-level audit metadata