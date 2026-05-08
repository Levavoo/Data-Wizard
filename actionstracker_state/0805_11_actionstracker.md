Case 02 — Messy But Valid CSV

Purpose:

verify whitespace, nulls, booleans, numbers, and dates are cleaned correctly

Create file:

New-Item examples\csv\messy_customers.csv
examples/csv/messy_customers.csv
 Customer ID , Name , Country , Active , Amount , Signup Date
 1 , Alice , Germany , YES , "1,000" , 2026-01-01
 2 , Bob , France , no , 250.50 , 02.01.2026
 3 , Charlie , , TRUE , , 2026/01/03
 4 , , Italy , false , "5,500.75" ,

Run pipeline:

python scripts\run_csv_pipeline.py `
    examples\csv\messy_customers.csv `
    data\processed\messy_customers_clean.csv `
    --report-path data\processed\messy_customers_report.json

Inspect:

Get-Content data\processed\messy_customers_clean.csv
Get-Content data\processed\messy_customers_report.json

Expected cleaned CSV:

customer_id,name,country,active,amount,signup_date
1,Alice,Germany,true,1000,2026-01-01
2,Bob,France,false,250.5,2026-01-02
3,Charlie,,true,,2026-01-03
4,,Italy,false,5500.75,

Expected report highlights:

customer_id → integer
name        → string
country     → string
active      → boolean
amount      → float
signup_date → date
missing values detected in name, country, amount, signup_date