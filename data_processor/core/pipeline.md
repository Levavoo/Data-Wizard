# pipeline.py

## Purpose

`pipeline.py` orchestrates the full CSV data cleaning workflow.

This module connects existing modules.

It does not contain cleaning, parsing, validation, or export logic itself.

Architecture:

```text
Input CSV
→ CsvAdapter
→ Table
→ Cleaners
→ Inference
→ Quality Report
→ CSV Exporter
→ Cleaned CSV
```

---

# Main Function

## `run_csv_pipeline(input_path, output_path)`

Runs the complete CSV workflow.

---

# Pipeline Steps

## 1. Parse CSV

```python
adapter = CsvAdapter(input_path)
table = adapter.read()
```

Converts:

```text
CSV file
→ Table
```

---

## 2. Clean Nulls

```python
clean_table_nulls(table)
```

Converts null-like values into:

```python
None
```

---

## 3. Clean Text

```python
clean_table_text(table)
```

Trims and normalizes whitespace.

---

## 4. Clean Booleans

```python
clean_table_booleans(table)
```

Converts values such as:

```text
"yes"
"no"
"true"
"false"
```

into:

```python
True
False
```

---

## 5. Clean Numbers

```python
clean_table_numbers(table)
```

Converts numeric strings into:

```python
int
float
```

---

## 6. Clean Dates

```python
clean_table_dates(table)
```

Converts date-like strings into:

```python
date
datetime
```

---

## 7. Infer Types

```python
infer_table_types(table)
```

Updates:

```python
column.inferred_type
```

---

## 8. Infer Schema Metadata

```python
infer_schema_metadata(table)
```

Adds metadata such as:

```text
missing_count
unique_count
sample_values
nullable
```

---

## 9. Generate Quality Report

```python
quality_report = generate_quality_report(table)
```

Creates a quality summary.

---

## 10. Export CSV

```python
export_table_to_csv(table, output_path)
```

Writes cleaned output to disk.

---

# Return Value

The pipeline returns:

```python
{
    "table": table,
    "quality_report": quality_report
}
```

---

# Example

```python
from data_processor.core.pipeline import run_csv_pipeline

result = run_csv_pipeline(
    input_path="data/raw/customers.csv",
    output_path="data/processed/customers_clean.csv",
)

print(result["quality_report"])
```

---

# Important Design Rule

The pipeline only orchestrates.

It should not:

- parse CSV manually
- clean values directly
- infer types directly
- validate rules directly
- write CSV manually

Those responsibilities belong to dedicated modules.

---

# Pipeline Position

This file is the first full workflow coordinator.

It connects:

```text
Adapter Layer
Cleaning Layer
Inference Layer
Validation Layer
Exporter Layer
```

---

# Current Scope

Supported now:

```text
CSV input
CSV output
basic cleaning
basic type inference
basic schema metadata
basic quality report
```

---

# Future Improvements

Possible future additions:

- configurable cleaning steps
- cleaning profiles
- dry-run mode
- report export
- error handling strategy
- row quarantine
- pipeline logging
- Excel pipeline
- JSON pipeline
- config-driven orchestration