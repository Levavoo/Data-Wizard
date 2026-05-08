tests/test_pipeline.py
tests/test_pipeline.md

Add coverage for:

report_path argument
diagnostic_bundle return value
JSON report file creation

ruff check `
    data_processor\core\pipeline.py `
    scripts\run_csv_pipeline.py `
    tests\test_pipeline.py

black `
    data_processor\core\pipeline.py `
    scripts\run_csv_pipeline.py `
    tests\test_pipeline.py

pytest tests\test_pipeline.py
pytest

python scripts\run_csv_pipeline.py `
    examples\sample_dirty.csv `
    data\processed\sample_clean.csv `
    --report-path data\processed\sample_clean_report.json

Get-Content data\processed\sample_clean.csv
Get-Content data\processed\sample_clean_report.json