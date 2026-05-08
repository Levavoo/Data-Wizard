Case 06 — Empty Columns and Empty Rows

Purpose:

verify empty column detection
verify empty row detection
verify high-null detection

Create:

New-Item examples\csv\empty_columns_rows.csv

Content:

customer_id,name,country,unused_column,active
1,Alice,Germany,,true
2,Bob,France,,false
3,Charlie,Italy,,true
,,,,
4,Diana,Germany,,false

Run:

python scripts\run_csv_pipeline.py `
    examples\csv\empty_columns_rows.csv `
    data\processed\empty_columns_rows_clean.csv `
    --report-path data\processed\empty_columns_rows_report.json

Expected report highlights:

empty_columns → ["unused_column"]
high_null_columns → ["unused_column"]
one row should have empty_row → true