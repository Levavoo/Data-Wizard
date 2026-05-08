Case 03 — Quoted Values CSV

Purpose:

verify quoted commas and quoted text values parse correctly

Create file:

New-Item examples\csv\quoted_values.csv
examples/csv/quoted_values.csv
customer_id,name,city,notes,amount
1,Alice,"Berlin, Germany","Prefers morning appointments","1,000.50"
2,Bob,"Paris, France","VIP customer, priority support","250.75"
3,Charlie,"Rome, Italy","Needs follow-up, send reminder",""

Run pipeline:

python scripts\run_csv_pipeline.py `
    examples\csv\quoted_values.csv `
    data\processed\quoted_values_clean.csv `
    --report-path data\processed\quoted_values_report.json

Inspect:

Get-Content data\processed\quoted_values_clean.csv
Get-Content data\processed\quoted_values_report.json

Expected cleaned CSV:

customer_id,name,city,notes,amount
1,Alice,"Berlin, Germany",Prefers morning appointments,1000.5
2,Bob,"Paris, France","VIP customer, priority support",250.75
3,Charlie,"Rome, Italy","Needs follow-up, send reminder",

Expected report highlights:

customer_id → integer
name        → string
city        → string
notes       → string
amount      → float