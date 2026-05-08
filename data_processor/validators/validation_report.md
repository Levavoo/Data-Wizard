# validation_report.py

## Purpose

`validation_report.py` summarizes validation results from the constraint engine.

This module belongs to the validation/reporting layer.

Architecture:

```text
ValidationResult List
→ Validation Report
→ Summary Diagnostics
```

---

# Why This Module Exists

The constraint engine produces detailed validation results.

Example:

```python
ValidationResult(
    column_name="age",
    constraint_type="min_value",
    passed=False,
    row_index=3,
    value=15,
)
```

That is useful for detail-level diagnostics.

But CLI output, UI screens, and migration reports also need summaries.

This module converts many individual results into a clear report.

---

# Main Function

## `generate_validation_report(results)`

Creates a validation summary dictionary.

Returned fields:

| Field | Description |
|---|---|
| `total_results` | Total number of validation results |
| `passed_count` | Number of passing results |
| `failed_count` | Number of failing results |
| `has_failures` | Whether any failures exist |
| `failures_by_column` | Failure count grouped by column |
| `failures_by_constraint` | Failure count grouped by constraint type |
| `failed_rows` | Sorted unique row indexes with failures |
| `failed_results` | Serialized failed validation results |

---

# Helper Functions

## `failures_by_column(failed_results)`

Counts failures by column.

Example:

```python
{
    "age": 2,
    "email": 1
}
```

---

## `failures_by_constraint(failed_results)`

Counts failures by constraint type.

Example:

```python
{
    "min_value": 2,
    "regex_pattern": 1
}
```

---

## `failed_rows(failed_results)`

Returns sorted unique row indexes that failed validation.

Example:

```python
[1, 3, 5]
```

---

# Example

```python
from data_processor.validators.validation_report import (
    generate_validation_report,
)

report = generate_validation_report(results)

print(report["failed_count"])
print(report["failures_by_column"])
```

---

# Example Output

```python
{
    "total_results": 10,
    "passed_count": 4,
    "failed_count": 6,
    "has_failures": True,
    "failures_by_column": {
        "age": 2,
        "email": 1
    },
    "failures_by_constraint": {
        "min_value": 2,
        "regex_pattern": 1
    },
    "failed_rows": [1, 3, 5],
    "failed_results": [
        {
            "column_name": "age",
            "constraint_type": "min_value",
            "passed": False,
            "message": "Value is below minimum: 18",
            "row_index": 1,
            "value": 15
        }
    ]
}
```

---

# Important Design Rule

This module only summarizes validation results.

It must not:

- validate constraints directly
- clean data
- repair values
- delete rows
- modify tables
- export files

---

# Pipeline Position

Recommended workflow:

```text
Parse
→ Clean
→ Infer Types
→ Type Casting
→ Schema Metadata
→ Analysis
→ Constraint Validation
→ Validation Report
→ Quality Report
→ Export
```

---

# Why This Helps Future Features

Validation reports will support:

- CLI summaries
- UI dashboards
- JSON report export
- row quarantine
- migration diagnostics
- audit logs
- rule severity reports

---

# Developer Notes

This module is intentionally small.

It should remain:

- side-effect free
- deterministic
- format-independent
- easy to test

---

# Current Limitations

Current implementation does not yet support:

- severity levels
- warning vs error distinction
- grouped row diagnostics
- repair hints
- validation score
- report export to JSON/Markdown

---

# Future Improvements

Possible future additions:

- validation quality score
- severity summaries
- row-level grouped errors
- column-level diagnostic summaries
- JSON report exporter
- Markdown report exporter
- quarantine candidate extraction