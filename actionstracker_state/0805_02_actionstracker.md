Stage 12 — Report Export

quality_report
validation_report
column_profiles
row_profiles

New-Item data_processor\exporters\json_report_exporter.py
New-Item data_processor\exporters\json_report_exporter.md

report dictionary
→ JSON file

Useful for:

CLI output
audit trail
migration diagnostics
future UI
debugging

export_report_to_json()
serialize_report_value()

New-Item tests\test_json_report_exporter.py
New-Item tests\test_json_report_exporter.md

ruff check `
    data_processor\exporters\json_report_exporter.py `
    tests\test_json_report_exporter.py

black `
    data_processor\exporters\json_report_exporter.py `
    tests\test_json_report_exporter.py

pytest tests\test_json_report_exporter.py
pytest