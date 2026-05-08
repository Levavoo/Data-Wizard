Stage 09.01 — Real Example Dataset

New-Item examples
New-Item data
New-Item data\processed

New-Item examples\sample_dirty.csv
New-Item examples\sample_dirty.md

real semi-messy CSV
→ run manually through CLI
→ inspect cleaned output

Recommended content for examples/sample_dirty.csv:

Name, Active , Amount , Birth_Date , Country
 Alice , YES , "1,000" , 1990-01-15 , germany
Bob,no,25.50,15.02.1985, DE
 Charlie , TRUE , , 1988/03/20 , Deutschland
Diana,False,"5,500.75",, France

This dataset intentionally contains:

whitespace
mixed booleans
mixed number formatting
mixed date formatting
missing values
mixed country naming

Purpose:

manual pipeline validation

Then run:

python scripts\run_csv_pipeline.py `
    examples\sample_dirty.csv `
    data\processed\sample_clean.csv

Then inspect:

Get-Content data\processed\sample_clean.csv


REPORT:

had to change pipeline order, id 1 was changed to true

The better long-term plan is:

Parse CSV
→ normalize nulls/text only
→ infer column types from raw-ish values
→ clean/cast values based on inferred column type
→ infer schema metadata
→ quality report
→ export

The key idea:

Do not ask every cleaner to touch every value.

Right now this happens:

customer_id = "1"
→ boolean cleaner sees "1"
→ converts to True

But the system should know:

customer_id column = integer

so only the number cleaner should touch it.

Better pipeline
1. Parse CSV
2. Normalize nulls
3. Normalize text whitespace
4. Infer column types
5. Cast/clean by column type
6. Infer schema metadata
7. Generate quality report
8. Export
Needed next module

Create a type-aware casting module:

data_processor/cleaners/type_caster.py
data_processor/cleaners/type_caster.md

Purpose:

column.inferred_type
→ choose correct cleaner

Example logic:

integer → normalize_integer
float → normalize_float
boolean → normalize_boolean
date/datetime → normalize_date_or_datetime
string → keep text-cleaned value
null → keep None

Then pipeline becomes:

clean_table_nulls(table)
clean_table_text(table)

infer_table_types(table)

cast_table_by_schema(table)

infer_schema_metadata(table)
quality_report = generate_quality_report(table)
export_table_to_csv(table, output_path)

This is the professional architecture.