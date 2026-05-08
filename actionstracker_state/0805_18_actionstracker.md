Case 08 — Short Rows and Extra Fields

Purpose:

verify current behavior for rows with missing or extra fields

Create:

New-Item examples\csv\short_extra_rows.csv
examples/csv/short_extra_rows.csv
customer_id,name,country,active
1,Alice,Germany,true
2,Bob,France
3,Charlie,Italy,true,unexpected_extra_value
4,Diana,,false

Run:

python scripts\run_csv_pipeline.py `
    examples\csv\short_extra_rows.csv `
    data\processed\short_extra_rows_clean.csv `
    --report-path data\processed\short_extra_rows_report.json

Inspect:

Get-Content data\processed\short_extra_rows_clean.csv
Get-Content data\processed\short_extra_rows_report.json

Expected current behavior:

row 2 active → missing / empty in output
row 3 extra value → ignored
country missing count → 1
active missing count → 1

extra fields are ignored silently

For migration software, silent ignoring is risky. Later we should add parser diagnostics like:

"parse_diagnostics": {
    "rows_with_extra_fields": [2],
    "rows_with_missing_fields": [1],
    "extra_field_count": 1,
    "missing_field_count": 1
}