Case 07 — Duplicate Headers CSV

Purpose:

detect current CSV adapter weakness:
duplicate headers can overwrite values

Create:

New-Item examples\csv\duplicate_headers.csv

examples/csv/duplicate_headers.csv

customer_id,name,name,country,active
1,Alice,Alicia,Germany,true
2,Bob,Robert,France,false
3,Charlie,Charles,Italy,true

Run:

python scripts\run_csv_pipeline.py `
    examples\csv\duplicate_headers.csv `
    data\processed\duplicate_headers_clean.csv `
    --report-path data\processed\duplicate_headers_report.json

Inspect:

Get-Content data\processed\duplicate_headers_clean.csv
Get-Content data\processed\duplicate_headers_report.json

Expected current behavior may be problematic.

Likely issue:

duplicate "name" headers may collapse into one column

FAILURE 

What happened:

CSV headers:
customer_id,name,name,country,active

csv.DictReader uses dictionary keys. Duplicate keys cannot exist in a Python dictionary, so one name field gets overwritten/collapsed.

Then our adapter tries to match:

normalized_headers length → 5
row.keys() length         → 4

So this fails:

zip(row.keys(), normalized_headers, strict=True)
Correct next fix

We should update csv_adapter.py so duplicate headers become unique during normalization.

Example:

name
name

should become:

name
name_2

or:

name
name_duplicate_2

Recommended simple convention:

name
name_2
name_3
Next implementation target

Update:

data_processor/adapters/csv_adapter.py
data_processor/adapters/csv_adapter.md
tests/test_csv_adapter.py
tests/test_csv_adapter.md

Add helper:

_normalize_headers()

Behavior:

["name", "name", "country"]
→ ["name", "name_2", "country"]

Also change row parsing to avoid relying on DictReader for duplicate headers. Use csv.reader instead, so we preserve every field.