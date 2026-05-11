# test_quality_report.py

## Purpose

Tests the quality reporting module.

This verifies that basic dataset quality metrics are calculated correctly.

Architecture:

```text
Table
→ Quality Report
→ Data Quality Summary
```

---

# Tested File

```text
data_processor/validators/quality_report.py
```

---

# Current Test Coverage

## `test_missing_values_by_column`

Verifies missing values are counted correctly for each column.

Example:

```python
{
    "email": 2
}
```

---

## `test_duplicate_row_count`

Verifies duplicate rows are detected correctly.

Example:

```text
Alice, Germany
Alice, Germany
```

Expected result:

```text
1 duplicate row
```

---

## `test_empty_columns`

Verifies fully empty columns are detected.

Rule:

```text
all values are None
```

---

## `test_high_null_columns`

Verifies columns with many missing values are flagged.

Example threshold:

```python
0.5
```

Means:

```text
50% or more values are missing
```

---

## `test_high_null_columns_invalid_threshold`

Verifies invalid thresholds raise:

```python
ValueError
```

Allowed range:

```text
0.0 → 1.0
```

---

## `test_generate_quality_report`

Verifies complete report generation.

Checks:

- table metadata
- duplicate counts
- missing values
- empty columns
- high-null columns

---

## `test_high_null_columns_empty_table`

Verifies empty tables return no high-null columns.

---

# Important Design Rule

The quality report module only reports issues.

It does not:

- clean data
- delete rows
- enforce rules
- transform values

This keeps reporting separate from modification logic.

---

# Why Quality Reporting Matters

Quality reports help:

- detect bad datasets
- identify cleaning priorities
- support validation workflows
- generate diagnostics
- support future UI/reporting systems

---

# Run Tests

```powershell
pytest tests\test_quality_report.py
```

Expected result:

```text
7 passed
```

---

# Recommended Validation Workflow

```powershell
ruff check `
    data_processor\validators\quality_report.py `
    tests\test_quality_report.py

black `
    data_processor\validators\quality_report.py `
    tests\test_quality_report.py

pytest tests\test_quality_report.py
```

---

# Developer Notes

This module assumes missing values are already normalized to:

```python
None
```

by earlier cleaner stages.

---

# Future Improvements

Possible future additions:

- invalid type reports
- outlier detection
- min/max violations
- uniqueness violations
- quality scoring
- severity levels
- report export
- row-level diagnostics