Case 13 — Footer / Summary Lines.

Create:

New-Item examples\csv\footer_summary_rows.csv

Content:

customer_id,name,amount,active
1,Alice,100,true
2,Bob,250.50,false
3,Charlie,300,true
TOTAL,,650.50,

Run:

python scripts\run_csv_pipeline.py `
    examples\csv\footer_summary_rows.csv `
    data\processed\footer_summary_rows_clean.csv `
    --report-path data\processed\footer_summary_rows_report.json

Inspect:

Get-Content data\processed\footer_summary_rows_clean.csv
Get-Content data\processed\footer_summary_rows_report.json

Expected current observation:

TOTAL row is treated as data
customer_id likely becomes string
row with TOTAL has missing name and active

Add to future improvement plan:

footer / summary row detection
column constraint: customer_id must be integer
row classification: possible_footer_row
optional removal/quarantine of summary rows