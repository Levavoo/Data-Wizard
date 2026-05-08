Update:

data_processor/adapters/csv_adapter.py
data_processor/adapters/csv_adapter.md
tests/test_csv_adapter.py
tests/test_csv_adapter.md

ruff check data_processor\adapters\csv_adapter.py tests\test_csv_adapter.py

black data_processor\adapters\csv_adapter.py tests\test_csv_adapter.py

pytest tests\test_csv_adapter.py
pytest

python scripts\run_csv_pipeline.py `
    examples\csv\duplicate_headers.csv `
    data\processed\duplicate_headers_clean.csv `
    --report-path data\processed\duplicate_headers_report.json

Get-Content data\processed\duplicate_headers_clean.csv