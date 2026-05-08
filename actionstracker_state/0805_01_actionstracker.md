Stage 11 — Validation Summary Report

New-Item data_processor\validators\validation_report.py
New-Item data_processor\validators\validation_report.md

list[ValidationResult]
→ validation summary

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
    "failed_rows": [1, 3, 5]
}

New-Item tests\test_validation_report.py
New-Item tests\test_validation_report.md

ruff check `
    data_processor\validators\validation_report.py `
    tests\test_validation_report.py

black `
    data_processor\validators\validation_report.py `
    tests\test_validation_report.py

pytest tests\test_validation_report.py
pytest

git add .
git commit -m "Add validation reporting"
git push