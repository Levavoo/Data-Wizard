# quality_report.py

## Purpose

`quality_report.py` generates basic data quality reports from the internal `Table` model.

This module belongs to the validation/reporting layer.

Architecture:

```text
Table
→ Quality Report
→ Data Quality Summary
```

---

# Main Responsibilities

The quality report detects:

- row count
- column count
- missing values by column
- duplicate rows
- empty columns
- high-null columns

---

# Main Functions

## `generate_quality_report(table, high_null_threshold=0.5)`

Creates a complete quality report dictionary.

Returned fields:

| Field | Description |
|---|---|
| `table_name` | Name of the dataset |
| `row_count` | Number of rows |
| `column_count` | Number of columns |
| `missing_values_by_column` | Missing values per column |
| `duplicate_row_count` | Number of duplicate rows |
| `empty_columns` | Columns where all values are missing |
| `high_null_columns` | Columns with many missing values |

---

## `missing_values_by_column(table)`

Counts missing values per schema column.

Only Python `None` is considered missing.

This assumes null cleaning has already run.

Example:

```python
{
    "name": 0,
    "email": 2
}
```

---

## `duplicate_row_count(table)`

Counts duplicate rows.

Example:

```text
Row 1: Alice, Germany
Row 2: Alice, Germany
```

Result:

```text
1 duplicate row
```

---

## `empty_columns(table)`

Detects columns where all values are missing.

Example:

```python
{
    "unused_column": None
}
```

If every row has `None`, the column is considered empty.

---

## `high_null_columns(table, threshold=0.5)`

Detects columns where the missing-value ratio is greater than or equal to the threshold.

Example:

```text
threshold = 0.5
```

Means:

```text
flag columns where at least 50% of values are missing
```

---

# Example

```python
from data_processor.validators.quality_report import generate_quality_report

report = generate_quality_report(table)

print(report)
```

Example output:

```python
{
    "table_name": "customers",
    "row_count": 100,
    "column_count": 5,
    "missing_values_by_column": {
        "email": 12
    },
    "duplicate_row_count": 3,
    "empty_columns": [],
    "high_null_columns": [
        "secondary_phone"
    ]
}
```

---

# Important Design Rule

This module reports quality issues.

It does not:

- clean data
- transform data
- delete rows
- enforce constraints
- export files

Later modules may use this report to decide what actions to take.

---

# Pipeline Position

Recommended pipeline order:

```text
Parsing
→ Cleaning
→ Type Inference
→ Schema Inference
→ Quality Report
→ Transformation
→ Export
```

---

# Developer Notes

This module assumes previous cleaning stages normalized missing values into:

```python
None
```

Therefore, missing value detection only checks:

```python
value is None
```

This keeps the logic simple and deterministic.

---

# Current Limitations

Current implementation does not detect:

- invalid types
- invalid constraints
- outliers
- min/max violations
- allowed-value violations
- referential integrity errors
- semantic/business rule errors

Those belong to future validator modules.

---

# Future Improvements

Possible future additions:

- invalid type counts
- min/max validation
- allowed value checks
- outlier detection
- column quality scores
- row quality scores
- report export to JSON/Markdown
- severity levels
- warning messages