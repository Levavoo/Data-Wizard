Case 04 — Semicolon Delimiter CSV

Purpose:

verify delimiter detection works for semicolon-separated CSV files

Create file:

New-Item examples\csv\semicolon_customers.csv
examples/csv/semicolon_customers.csv
customer_id;name;country;active;amount;signup_date
1;Alice;Germany;yes;1000;2026-01-01
2;Bob;France;no;250.50;02.01.2026
3;Charlie;Italy;true;300;2026/01/03

Run pipeline:

python scripts\run_csv_pipeline.py `
    examples\csv\semicolon_customers.csv `
    data\processed\semicolon_customers_clean.csv `
    --report-path data\processed\semicolon_customers_report.json

Inspect:

Get-Content data\processed\semicolon_customers_clean.csv
Get-Content data\processed\semicolon_customers_report.json

Expected cleaned CSV:

customer_id,name,country,active,amount,signup_date
1,Alice,Germany,true,1000,2026-01-01
2,Bob,France,false,250.5,2026-01-02
3,Charlie,Italy,true,300,2026-01-03

Expected report metadata should include:

delimiter → 