# test_constraints.py

## Purpose

Tests the constraint validation engine.

This verifies reusable validation rules against table data.

Architecture:

```text
Table + Constraints
→ Constraint Engine
→ Validation Results
```

---

# Tested File

```text
data_processor/validators/constraints.py
```

---

# Current Test Coverage

## `test_validation_result_to_dict`

Verifies validation results serialize correctly.

---

## `test_validate_required`

Verifies required-value validation.

Checks:

```python
None
```

detection.

---

## `test_validate_unique`

Verifies duplicate detection.

---

## `test_validate_min_value`

Verifies minimum numeric validation.

Example:

```python
age >= 18
```

---

## `test_validate_max_value`

Verifies maximum numeric validation.

Example:

```python
age <= 120
```

---

## `test_validate_allowed_values`

Verifies category restriction validation.

Example:

```python
country in allowed_values
```

---

## `test_validate_regex_pattern`

Verifies regex-based validation.

Example:

```python
email pattern validation
```

---

## `test_validate_column_constraint_dispatch`

Verifies constraint dispatching.

---

## `test_validate_unknown_constraint`

Verifies unsupported constraints fail safely.

---

## `test_validate_table_constraints`

Verifies multiple constraints can be applied to one table.

---

# Important Design Rule

Validators only validate.

They must never:

- clean data
- repair values
- delete rows
- export data

---

# Run Tests

```powershell
pytest tests\test_constraints.py
```

Expected:

```text
10 passed
```

---

# Recommended Validation Workflow

```powershell
ruff check `
    data_processor\validators\constraints.py `
    tests\test_constraints.py

black `
    data_processor\validators\constraints.py `
    tests\test_constraints.py

pytest tests\test_constraints.py
```

---

# Developer Notes

Constraint validation is now independent from:

- file format
- parser
- exporter
- cleaning logic

All formats validate through:

```text
Table
```

---

# Future Improvements

Possible future additions:

- composite keys
- foreign keys
- semantic rules
- severity levels
- repair hints
- quarantine support
- YAML/JSON rule definitions
- validation summaries