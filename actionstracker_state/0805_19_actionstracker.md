Case 09 — Empty Headers CSV

Purpose:

verify empty headers become unnamed_column
verify duplicate empty headers become unnamed_column_2

Create:

New-Item examples\csv\empty_headers.csv

Content:

customer_id,,country,,active
1,Alice,Germany,Note A,true
2,Bob,France,Note B,false
3,Charlie,Italy,,true

Run:

python scripts\run_csv_pipeline.py `
    examples\csv\empty_headers.csv `
    data\processed\empty_headers_clean.csv `
    --report-path data\processed\empty_headers_report.json

Expected cleaned header:

customer_id,unnamed_column,country,unnamed_column_2,active