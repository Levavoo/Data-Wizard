Stage 06 — Quality Report

Table + schema metadata
→ basic data quality summary

New-Item data_processor\validators\quality_report.py
New-Item data_processor\validators\quality_report.md

table_name
row_count
column_count
missing_values_by_column
duplicate_row_count
empty_columns
high_null_columns

New-Item tests\test_quality_report.py
New-Item tests\test_quality_report.md

ruff check `
    data_processor\validators\quality_report.py `
    tests\test_quality_report.py

black `
    data_processor\validators\quality_report.py `
    tests\test_quality_report.py

pytest tests\test_quality_report.py

pytest

git add .

git commit -m "Implement quality reporting module"