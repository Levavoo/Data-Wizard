Case 16 — European Decimal Numbers

Purpose:

test locale-style numbers common in Germany/EU

Create:

New-Item examples\csv\european_decimals.csv

Content:

customer_id,name,amount
1,Alice,"1.000,50"
2,Bob,"250,75"
3,Charlie,"5.500,00"

Run:

python scripts\run_csv_pipeline.py `
    examples\csv\european_decimals.csv `
    data\processed\european_decimals_clean.csv `
    --report-path data\processed\european_decimals_report.json

Expected current behavior:

amount → string

because the current number parser assumes US-style numbers:

1,000.50

not EU-style:

1.000,50

Add to future improvement plan:

locale-aware numeric parsing
German/EU decimal support
configurable number format policy