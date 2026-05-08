# test_validation_report.py

## Purpose

Tests the validation report module.

This verifies that individual validation results can be summarized into useful diagnostics.

Architecture:

```text
ValidationResult List
→ Validation Report
→ Summary Diagnostics
```

---

# Tested File

```text
data_processor/validators/validation_report.py
```

---

# Current Test Coverage

## `test_failures_by_column`

Verifies validation failures are grouped by column.

Example:

```python
{
    "age": 2,
    "email": 1
}
```

---

## `test_failures_by_constraint`

Verifies validation failures are grouped by constraint type.

Example:

```python
{
    "min_value": 1,
    "max_value": 1,
    "regex_pattern": 1
}
```

---

## `test_failed_rows`

Verifies failed row indexes are:

- unique
- sorted
- excluding `None`

Example:

```python
[1, 2]
```

---

## `test_generate_validation_report`

Verifies complete validation report generation.

Checks:

- total result count
- passed result count
- failed result count
- failure existence flag
- grouped failures
- failed rows
- serialized failed results

---

## `test_generate_validation_report_without_failures`

Verifies clean behavior when all validations pass.

Expected:

```python
{
    "has_failures": False,
    "failed_count": 0,
    "failed_rows": []
}
```

---

# Important Design Rule

Validation reports summarize only.

They must never:

- validate constraints directly
- clean values
- mutate tables
- export files

---

# Run Tests

```powershell
pytest tests\test_validation_report.py
```

Expected:

```text
5 passed
```

---

# Recommended Validation Workflow

```powershell
ruff check `
    data_processor\validators\validation_report.py `
    tests\test_validation_report.py

black `
    data_processor\validators\validation_report.py `
    tests\test_validation_report.py

pytest tests\test_validation_report.py
```

---

# Developer Notes

Validation reports will later support:

- CLI output
- JSON export
- Markdown reports
- row quarantine
- migration diagnostics
- UI dashboards