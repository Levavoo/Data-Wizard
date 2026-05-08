# constraints.py

## Purpose

`constraints.py` validates table data against reusable constraint definitions.

This module belongs to the validation layer.

Architecture:

```text
Table + Constraints
→ Constraint Engine
→ Validation Results
```

---

# Important Design Rule

The constraint engine validates only.

It must never:

- clean values
- cast values
- delete rows
- repair data
- export data

It only reports whether rules passed or failed.

---

# Main Classes

## `Constraint`

Defines one validation rule for one column.

Fields:

| Field | Type | Description |
|---|---|---|
| `column_name` | `str` | Column to validate |
| `constraint_type` | `str` | Rule type |
| `value` | `Any` | Optional rule value |

Example:

```python
Constraint(
    column_name="age",
    constraint_type="min_value",
    value=18,
)
```

---

## `ValidationResult`

Represents one validation result.

Fields:

| Field | Type | Description |
|---|---|---|
| `column_name` | `str` | Validated column |
| `constraint_type` | `str` | Applied constraint |
| `passed` | `bool` | Whether validation passed |
| `message` | `str` | Human-readable message |
| `row_index` | `int | None` | Row where failure occurred |
| `value` | `Any` | Offending value if relevant |

---

# Supported Constraints

## `required`

Checks that values are not missing.

Failure example:

```python
None
```

---

## `unique`

Checks that non-null values are unique.

Failure example:

```text
duplicate customer_id
```

---

## `min_value`

Checks that values are greater than or equal to a minimum.

Example:

```python
Constraint("age", "min_value", 18)
```

---

## `max_value`

Checks that values are less than or equal to a maximum.

Example:

```python
Constraint("age", "max_value", 120)
```

---

## `allowed_values`

Checks that values belong to an allowed set.

Example:

```python
Constraint(
    column_name="country",
    constraint_type="allowed_values",
    value=["Germany", "France", "Italy"],
)
```

---

## `regex_pattern`

Checks that string values match a regex pattern.

Example:

```python
Constraint(
    column_name="email",
    constraint_type="regex_pattern",
    value=r"^[^@]+@[^@]+\.[^@]+$",
)
```

---

# Main Functions

## `validate_table_constraints(table, constraints)`

Applies multiple constraints to a table.

Returns:

```python
list[ValidationResult]
```

---

## `validate_column_constraint(table, constraint)`

Dispatches one constraint to the correct validation function.

---

# Validation Result Behavior

If a constraint passes fully, one passing result is returned.

Example:

```python
ValidationResult(
    column_name="age",
    constraint_type="min_value",
    passed=True,
    message="Minimum value constraint passed.",
)
```

If a constraint fails, one result is returned per violation.

Example:

```python
ValidationResult(
    column_name="age",
    constraint_type="min_value",
    passed=False,
    message="Value is below minimum: 18",
    row_index=4,
    value=16,
)
```

---

# Example Usage

```python
from data_processor.validators.constraints import (
    Constraint,
    validate_table_constraints,
)

constraints = [
    Constraint("customer_id", "required"),
    Constraint("customer_id", "unique"),
    Constraint("age", "min_value", 18),
]

results = validate_table_constraints(
    table=table,
    constraints=constraints,
)

failed_results = [
    result
    for result in results
    if not result.passed
]
```

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
→ Quality Report
→ Export
```

---

# Why This Helps Future Formats

All future formats become:

```text
Table
```

Therefore the same constraints work for:

- CSV
- Excel
- JSON
- SQL
- APIs
- Parquet
- Arrow

without rewriting validation logic.

---

# Developer Notes

This module should remain:

- format-independent
- deterministic
- side-effect free
- easy to test
- rule-focused

---

# Current Limitations

Current implementation does not yet support:

- multi-column constraints
- foreign key constraints
- primary key abstraction
- conditional constraints
- severity levels
- validation groups
- quarantine flags
- repair suggestions

---

# Future Improvements

Possible future additions:

- row-level validation reports
- validation summary reports
- severity levels
- constraint profiles
- YAML/JSON constraint config
- cross-field validation
- referential integrity checks
- semantic/business rules