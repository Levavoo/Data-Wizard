0805_02_actionstracker

You now have several separate diagnostics:

quality_report
validation_report
column_profiles
row_profiles

Create one module that combines them into a single structured report object.

Why this is next

It will make CLI/report export much cleaner:

pipeline result
→ diagnostic bundle
→ JSON report

Instead of exporting many separate reports manually

New-Item data_processor\reports\diagnostic_bundle.py
New-Item data_processor\reports\diagnostic_bundle.md

mkdir data_processor\reports
New-Item data_processor\reports\__init__.py

Goal
Table + optional validation results
→ complete diagnostic report

Recommended output:

{
    "table_name": "customers",
    "quality_report": {...},
    "column_profiles": {...},
    "row_profiles": [...],
    "validation_report": {...}
}

New-Item tests\test_diagnostic_bundle.py
New-Item tests\test_diagnostic_bundle.md

ruff check `
    data_processor\reports\diagnostic_bundle.py `
    tests\test_diagnostic_bundle.py

black `
    data_processor\reports\diagnostic_bundle.py `
    tests\test_diagnostic_bundle.py

pytest tests\test_diagnostic_bundle.py
pytest