# pipeline.py

## Purpose

`pipeline.py` orchestrates the full CSV data cleaning workflow.

This module connects existing modules.

It does not contain cleaning, parsing, validation, reporting, or export logic itself.

Architecture:

```text
Input CSV
→ CsvAdapter
→ Table
→ Cleaners
→ Type Inference
→ Type-Aware Casting
→ Schema Metadata
→ Quality Report
→ Diagnostic Bundle
→ CSV Exporter
→ Optional JSON Report Exporter
→ Cleaned CSV + Diagnostic Report
```

---

# Main Function

## `run_csv_pipeline(input_path, output_path, report_path=None)`

Runs the complete CSV workflow.

---

# Arguments

| Argument | Type | Description |
|---|---|---|
| `input_path` | `str | Path` | Source CSV file path |
| `output_path` | `str | Path` | Target cleaned CSV output path |
| `report_path` | `str | Path | None` | Optional diagnostic JSON report output path |

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

Trims surrounding whitespace and collapses repeated internal whitespace.

---

## 4. Infer Types

```python
infer_table_types(table)
```

Detects likely column types before casting.

Example:

```text
"1"
→ inferred as integer
```

The value is not converted yet.

---

## 5. Type-Aware Casting

```python
cast_table_by_schema(table)
```

Casts values according to each column's inferred type.

Example:

```text
customer_id column inferred as integer
"1"
→ 1

active column inferred as boolean
"yes"
→ True
```

This prevents incorrect global cleaner behavior such as:

```text
customer_id = "1"
→ True
```

---

## 6. Refresh Type Inference

```python
infer_table_types(table)
```

Runs type inference again after casting so schema metadata reflects cleaned values.

---

## 7. Infer Schema Metadata

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

## 8. Generate Quality Report

```python
quality_report = generate_quality_report(table)
```

Creates a basic quality summary.

Includes:

```text
row count
column count
missing values
duplicate rows
empty columns
high-null columns
```

---

## 9. Build Diagnostic Bundle

```python
diagnostic_bundle = build_diagnostic_bundle(table)
```

Creates one combined diagnostic report.

Includes:

```text
quality report
column profiles
row profiles
validation report
```

At this stage, validation results are not yet integrated into the CSV pipeline, so the validation report section is present but empty.

---

## 10. Export Cleaned CSV

```python
export_table_to_csv(table, output_path)
```

Writes cleaned data to disk.

---

## 11. Optionally Export Diagnostic JSON Report

```python
if report_path is not None:
    export_report_to_json(
        report=diagnostic_bundle,
        output_path=report_path,
    )
```

Writes the diagnostic bundle to JSON if a report path is provided.

---

# Return Value

The pipeline returns:

```python
{
    "table": table,
    "quality_report": quality_report,
    "diagnostic_bundle": diagnostic_bundle,
}
```

---

# Example Without Report Export

```python
from data_processor.core.pipeline import run_csv_pipeline

result = run_csv_pipeline(
    input_path="data/raw/customers.csv",
    output_path="data/processed/customers_clean.csv",
)

print(result["quality_report"])
```

---

# Example With Report Export

```python
from data_processor.core.pipeline import run_csv_pipeline

result = run_csv_pipeline(
    input_path="data/raw/customers.csv",
    output_path="data/processed/customers_clean.csv",
    report_path="data/processed/customers_report.json",
)

print(result["diagnostic_bundle"])
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
- build report internals manually

Those responsibilities belong to dedicated modules.

---

# Current CSV Workflow

```text
CSV File
↓
CsvAdapter
↓
Table
↓
Null/Text Cleaning
↓
Type Inference
↓
Type-Aware Casting
↓
Type Inference Refresh
↓
Schema Metadata
↓
Diagnostic Bundle
↓
Cleaned CSV
↓
Optional Diagnostic JSON Report
```

---

# Current Scope

Supported now:

```text
CSV input
CSV output
optional JSON diagnostic report
basic cleaning
type inference
type-aware casting
schema metadata
column profiling
row profiling
quality reporting
```

---

# Not Yet Integrated

The following systems exist but are not fully connected to the CSV pipeline yet:

```text
constraint validation
validation results from user-provided rules
CLI constraint configuration
strict/tolerant CSV modes
row quarantine
```

---

# Future Improvements

Possible future additions:

- optional constraints argument
- validation report integration
- report path auto-generation
- strict/tolerant parsing mode
- source file metadata in diagnostic bundle
- output file metadata in diagnostic bundle
- execution duration
- pipeline version
- cleaning profile support
- batch CSV processing