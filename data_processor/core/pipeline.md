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
→ Optional Constraint Validation
→ Quality Report
→ Diagnostic Bundle
→ CSV Exporter
→ Optional JSON Report Exporter
→ Cleaned CSV + Diagnostic Report
```

---

## Main Function

### `run_csv_pipeline(input_path, output_path, report_path=None, constraints=None)`

Runs the complete CSV workflow.

---

## Arguments

| Argument | Type | Description |
|---|---|---|
| `input_path` | `str | Path` | Source CSV file path |
| `output_path` | `str | Path` | Target cleaned CSV output path |
| `report_path` | `str | Path | None` | Optional diagnostic JSON report output path |
| `constraints` | `list[Constraint] | None` | Optional validation constraints |

---

## Pipeline Steps

### 1. Parse CSV

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

### 2. Clean Nulls

```python
clean_table_nulls(table)
```

Converts null-like values into:

```python
None
```

---

### 3. Clean Text

```python
clean_table_text(table)
```

Trims surrounding whitespace and collapses repeated internal whitespace.

---

### 4. Infer Types

```python
infer_table_types(table)
```

Detects likely column types before casting.

---

### 5. Type-Aware Casting

```python
cast_table_by_schema(table)
```

Casts values according to each column's inferred type.

---

### 6. Refresh Type Inference

```python
infer_table_types(table)
```

Runs type inference again after casting so schema metadata reflects cleaned values.

---

### 7. Infer Schema Metadata

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

### 8. Optional Constraint Validation

```python
validation_results = validate_table_constraints(
    table=table,
    constraints=constraints,
)
```

Runs after cleaning and casting.

If no constraints are provided, validation results are empty and existing behavior is preserved.

---

### 9. Generate Quality Report

```python
quality_report = generate_quality_report(table)
```

Creates a basic quality summary.

---

### 10. Build Diagnostic Bundle

```python
diagnostic_bundle = build_diagnostic_bundle(
    table=table,
    validation_results=validation_results,
)
```

Creates one combined diagnostic report.

Includes:

```text
parse diagnostics
quality report
column profiles
row profiles
row classification
type diagnostics
validation report
```

---

### 11. Export Cleaned CSV

```python
export_table_to_csv(table, output_path)
```

Writes cleaned data to disk.

---

### 12. Optionally Export Diagnostic JSON Report

```python
if report_path is not None:
    export_report_to_json(
        report=diagnostic_bundle,
        output_path=report_path,
    )
```

Writes the diagnostic bundle to JSON if a report path is provided.

---

## Return Value

The pipeline returns:

```python
{
    "table": table,
    "quality_report": quality_report,
    "validation_results": validation_results,
    "diagnostic_bundle": diagnostic_bundle,
}
```

---

## Example With Constraints

```python
from data_processor.core.pipeline import run_csv_pipeline
from data_processor.validators.constraints import Constraint

constraints = [
    Constraint(column_name="customer_id", constraint_type="required"),
    Constraint(column_name="customer_id", constraint_type="unique"),
]

result = run_csv_pipeline(
    input_path="data/raw/customers.csv",
    output_path="data/processed/customers_clean.csv",
    report_path="data/processed/customers_report.json",
    constraints=constraints,
)
```

---

## Important Design Rule

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

## Current CSV Workflow

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
Optional Constraint Validation
↓
Diagnostic Bundle
↓
Cleaned CSV
↓
Optional Diagnostic JSON Report
```

---

## Current Scope

Supported now:

```text
CSV input
CSV output
optional JSON diagnostic report
optional constraint validation
basic cleaning
type inference
type-aware casting
schema metadata
column profiling
row profiling
row classification
mixed-type diagnostics
quality reporting
validation reporting
```

---

## Future Improvements

Possible future additions:

- report path auto-generation
- strict/tolerant parsing mode
- source file metadata in diagnostic bundle
- output file metadata in diagnostic bundle
- execution duration
- pipeline version
- cleaning profile support
- batch CSV processing
- export-blocking validation policy
- quarantine support
