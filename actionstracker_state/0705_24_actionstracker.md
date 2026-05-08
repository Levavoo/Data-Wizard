Stage 10 — Constraint Engine

New-Item data_processor\validators\constraints.py
New-Item data_processor\validators\constraints.md

Table + rule definitions
→ validation results

required
unique
min_value
max_value
allowed_values
regex_pattern

Recommended design:

Constraint
ValidationResult
validate_table_constraints()
validate_column_constraint()

Constraint engine validates only.
It must not clean, cast, delete, or repair data.

New-Item tests\test_constraints.py
New-Item tests\test_constraints.md

