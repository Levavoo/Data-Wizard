Case 10 — Mixed-Type Column

Purpose:

verify how the current system handles a column containing numbers plus random text

Create:

New-Item examples\csv\mixed_type_column.csv
examples/csv/mixed_type_column.csv
customer_id,name,amount,status
1,Alice,100,ok
2,Bob,unknown,ok
3,Charlie,250.50,review
4,Diana,n/a,ok
5,Erik,500,failed

Run:

python scripts\run_csv_pipeline.py `
    examples\csv\mixed_type_column.csv `
    data\processed\mixed_type_column_clean.csv `
    --report-path data\processed\mixed_type_column_report.json

Inspect:

Get-Content data\processed\mixed_type_column_clean.csv
Get-Content data\processed\mixed_type_column_report.json

Expected current behavior:

amount → string

Reason:

100
unknown
250.50
None
500

Because one non-null value is "unknown", the current type inference should classify the full column as string.

This is acceptable for now. Later, we can add:

mixed type detection
invalid-type diagnostics
column-level casting confidence
quarantine candidates