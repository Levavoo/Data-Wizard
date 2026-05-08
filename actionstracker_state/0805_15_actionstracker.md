Case 05 — Duplicates and Missing Values CSV

Purpose:

verify duplicate detection, missing-value detection, row profiles, and quality report behavior

Create file:

New-Item examples\csv\duplicates_missing.csv
examples/csv/duplicates_missing.csv
customer_id,name,country,active,amount,email
1,Alice,Germany,true,100,alice@example.com
2,Bob,France,false,250.50,
2,Bob,France,false,250.50,
3,Charlie,,true,,charlie@example.com
4,,Italy,false,500,

Run pipeline:

python scripts\run_csv_pipeline.py `
    examples\csv\duplicates_missing.csv `
    data\processed\duplicates_missing_clean.csv `
    --report-path data\processed\duplicates_missing_report.json

Inspect:

Get-Content data\processed\duplicates_missing_clean.csv
Get-Content data\processed\duplicates_missing_report.json

Expected quality report highlights:

duplicate_row_count → 1

missing_values_by_column:
name    → 1
country → 1
amount  → 1
email   → 3

Expected row profile highlights:

row 1 and row 2 duplicate_candidate → true
rows with missing fields show missing_count > 0