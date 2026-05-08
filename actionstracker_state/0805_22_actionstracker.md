Case 11 — Garbage / Comment Lines

Purpose:

verify how the current system handles random non-table text inside a CSV

Create:

New-Item examples\csv\garbage_lines.csv
examples/csv/garbage_lines.csv
customer_id,name,country,active
1,Alice,Germany,true
THIS IS A RANDOM NOTE LINE
2,Bob,France,false
3,Charlie,Italy,true

Run:

python scripts\run_csv_pipeline.py `
    examples\csv\garbage_lines.csv `
    data\processed\garbage_lines_clean.csv `
    --report-path data\processed\garbage_lines_report.json

Inspect:

Get-Content data\processed\garbage_lines_clean.csv
Get-Content data\processed\garbage_lines_report.json

Expected current behavior:

garbage line becomes a short row
customer_id = "THIS IS A RANDOM NOTE LINE"
name = missing
country = missing
active = missing

This is not ideal, but it is useful. It proves we need a future parser diagnostics layer to flag suspicious rows instead of silently accepting them.