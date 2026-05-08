Case 17 — Weird Null Tokens

Purpose:

verify which null-like values are currently normalized
and which ones remain as text

Create:

New-Item examples\csv\weird_null_tokens.csv
examples/csv/weird_null_tokens.csv
customer_id,name,email,phone
1,Alice,alice@example.com,-
2,Bob,NULL,#N/A
3,Charlie,NIL,n/a
4,Diana,none,NA
5,Erik,,nan

Run:

python scripts\run_csv_pipeline.py `
    examples\csv\weird_null_tokens.csv `
    data\processed\weird_null_tokens_clean.csv `
    --report-path data\processed\weird_null_tokens_report.json

Inspect:

Get-Content data\processed\weird_null_tokens_clean.csv
Get-Content data\processed\weird_null_tokens_report.json

Expected current behavior:

normalized to missing:
-
NULL
n/a
none
NA
empty string
nan

not currently normalized:
#N/A
NIL

Expected future improvement plan entries:

extend null dictionary
add configurable null tokens
support column-specific null policies
track original null token statistics

Potential future null tokens:

#N/A
NIL
missing
unknown
not available
not_applicable
-- 
?