Case 14 — Multi-Line Quoted Fields

Purpose:

verify valid CSV fields containing line breaks are parsed correctly

This is common in exported notes, comments, CRM data, support tickets, and medical/veterinary records.

Create:

New-Item examples\csv\multiline_quoted_fields.csv
examples/csv/multiline_quoted_fields.csv
customer_id,name,notes,active
1,Alice,"First line
second line",true
2,Bob,"Normal note",false
3,Charlie,"Follow-up needed
call next week",true

Run:

python scripts\run_csv_pipeline.py `
    examples\csv\multiline_quoted_fields.csv `
    data\processed\multiline_quoted_fields_clean.csv `
    --report-path data\processed\multiline_quoted_fields_report.json

Inspect:

Get-Content data\processed\multiline_quoted_fields_clean.csv
Get-Content data\processed\multiline_quoted_fields_report.json

Expected:

customer_id → integer
name        → string
notes       → string
active      → boolean

The output CSV should preserve quoted multi-line text safely.