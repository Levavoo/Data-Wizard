Case 15 — Escaped Quotes

Purpose:

verify valid CSV fields containing escaped quotes are parsed correctly

This is common in notes, comments, names, product descriptions, and exported CRM/ERP text fields.

Create:

New-Item examples\csv\escaped_quotes.csv
examples/csv/escaped_quotes.csv
customer_id,name,notes,active
1,Alice,"She said ""hello""",true
2,Bob,"Customer wrote ""urgent"" in the message",false
3,Charlie,"Quote inside text: ""check again""",true

Run:

python scripts\run_csv_pipeline.py `
    examples\csv\escaped_quotes.csv `
    data\processed\escaped_quotes_clean.csv `
    --report-path data\processed\escaped_quotes_report.json

Inspect:

Get-Content data\processed\escaped_quotes_clean.csv
Get-Content data\processed\escaped_quotes_report.json

Expected type behavior:

customer_id → integer
name        → string
notes       → string
active      → boolean

Expected cleaned values should preserve quotes inside text, for example:

She said "hello"