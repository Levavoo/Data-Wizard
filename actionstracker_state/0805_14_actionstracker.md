The CSV adapter stores it here:

table.metadata["delimiter"]

But the diagnostic bundle currently does not include table.metadata.

So the parser detected the semicolon, but the report does not show it yet.

Current place in code:

table.add_metadata("source_format", "csv")
table.add_metadata("encoding", encoding)
table.add_metadata("delimiter", delimiter)

in:

data_processor/adapters/csv_adapter.py

Recommended next fix:

Add table metadata to diagnostic_bundle.py

Then the report can show:

"metadata": {
    "source_format": "csv",
    "encoding": "utf-8",
    "delimiter": ";"
}

ruff check `
    data_processor\reports\diagnostic_bundle.py `
    tests\test_diagnostic_bundle.py

black `
    data_processor\reports\diagnostic_bundle.py `
    tests\test_diagnostic_bundle.py

pytest tests\test_diagnostic_bundle.py
pytest

python scripts\run_csv_pipeline.py `
    examples\csv\semicolon_customers.csv `
    data\processed\semicolon_customers_clean.csv `
    --report-path data\processed\semicolon_customers_report.json