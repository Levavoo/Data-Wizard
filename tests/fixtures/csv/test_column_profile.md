# test_column_profile.py

## Purpose

Tests the column profiling module.

This verifies that column statistics are generated correctly.

Architecture:

```text
Table
→ Column Profiler
→ Statistical Column Profiles
```

---

# Tested File

```text
data_processor/analysis/column_profile.py
```

---

# Current Test Coverage

## `test_calculate_ratio`

Verifies safe ratio calculation.

Example:

```python
1 / 4
→ 0.25
```

---

## `test_calculate_ratio_zero_division`

Verifies division-by-zero protection.

Expected:

```python
0.0
```

---

## `test_extract_numeric_values`

Verifies only real numeric values are extracted.

Booleans must be excluded.

Example:

```python
True
False
```

must NOT become:

```python
1
0
```

---

## `test_sample_values`

Verifies unique sample extraction.

Duplicates should be removed.

---

## `test_most_common_values`

Verifies frequency counting.

Example result:

```python
("Germany", 3)
```

---

## `test_profile_column`

Verifies complete column statistics generation.

Checks:

- missing counts
- unique counts
- inferred types
- sample values
- ratios

---

## `test_profile_numeric_column`

Verifies numeric profiling.

Checks:

- minimum value
- maximum value

---

## `test_profile_all_columns`

Verifies full-table profiling.

---

# Important Design Rule

Profilers analyze only.

They must never:

- modify rows
- clean values
- infer schema
- export data

This keeps profiling deterministic and safe.

---

# Run Tests

```powershell
pytest tests\test_column_profile.py
```

Expected:

```text
8 passed
```

---

# Recommended Validation Workflow

```powershell
ruff check `
    data_processor\analysis\column_profile.py `
    tests\test_column_profile.py

black `
    data_processor\analysis\column_profile.py `
    tests\test_column_profile.py

pytest tests\test_column_profile.py
```

---

# Developer Notes

Profiling modules are important because they become the foundation for:

- validation
- reporting
- UI dashboards
- anomaly detection
- future ML-assisted cleaning

---

# Future Improvements

Possible future additions:

- histograms
- quantiles
- standard deviation
- text statistics
- regex analysis
- semantic profiling
- candidate key detection
- cardinality classification