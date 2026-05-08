Case 01 — Simple Clean CSV

verify the pipeline works on normal clean CSV input

Create folder if needed:

mkdir examples\csv

Create file:

New-Item examples\csv\simple_customers.csv
examples/csv/simple_customers.csv
customer_id,name,country,active,amount,signup_date
1,Alice,Germany,true,100,2026-01-01
2,Bob,France,false,250.5,2026-01-02
3,Charlie,Italy,true,300,2026-01-03

Run pipeline:

python scripts\run_csv_pipeline.py `
    examples\csv\simple_customers.csv `
    data\processed\simple_customers_clean.csv `
    --report-path data\processed\simple_customers_report.json

Inspect output:

Get-Content data\processed\simple_customers_clean.csv
Get-Content data\processed\simple_customers_report.json

Expected cleaned CSV:

customer_id,name,country,active,amount,signup_date
1,Alice,Germany,true,100,2026-01-01
2,Bob,France,false,250.5,2026-01-02
3,Charlie,Italy,true,300,2026-01-03

In the report, expected inferred types:

customer_id → integer
name        → string
country     → string
active      → boolean
amount      → float
signup_date → date