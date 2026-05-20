# pipeline.py

## Purpose

`pipeline.py` orchestrates the full CSV data cleaning workflow.

This module connects existing modules.

It does not contain cleaning, parsing, validation, reporting, export, or CLI exit logic itself.

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
→ Pipeline Status
→ CSV Exporter
→ Optional JSON Report Exporter
→ Optional HTML Report Exporter
→ Optional Quarantine Exporters
→ Cleaned CSV + Diagnostic Reports + Review Outputs + Status
```

---

## Main Function

### `run_csv_pipeline(input_path, output_path, report_path=None, html_report_path=None, quarantine_candidates_path=None, quarantine_rows_path=None, accepted_rows_path=None, constraints=None, strict_mode=False)`

Runs the complete CSV workflow.

---

## Arguments

| Argument | Type | Description |
|---|---|---|
| `input_path` | `str | Path` | Source CSV file path |
| `output_path` | `str | Path` | Target cleaned CSV output path |
| `report_path` | `str | Path | None` | Optional diagnostic JSON report output path |
| `html_report_path` | `str | Path | None` | Optional diagnostic HTML report output path |
| `quarantine_candidates_path` | `str | Path | None` | Optional quarantine candidates JSON output path |
| `quarantine_rows_path` | `str | Path | None` | Optional quarantine candidate rows CSV output path |
| `accepted_rows_path` | `str | Path | None` | Optional accepted rows CSV output path |
| `constraints` | `list[Constraint] | None` | Optional validation constraints |
| `strict_mode` | `bool` | Optional strict policy status mode |

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
quarantine candidates
```

---

### 11. Build Pipeline Status

```python
pipeline_status = build_pipeline_status(
    diagnostic_bundle=diagnostic_bundle,
    strict_mode=strict_mode,
)
```

Creates automation-friendly status information.

Strict mode is opt-in and defaults to `False`.

---

### 12. Export Cleaned CSV

```python
export_table_to_csv(table, output_path)
```

Writes cleaned data to disk.

Strict policy failure does not block CSV export.

The normal cleaned CSV still includes all rows.

---

### 13. Optionally Export Diagnostic JSON Report

```python
if report_path is not None:
    export_report_to_json(
        report=diagnostic_bundle,
        output_path=report_path,
    )
```

Writes the diagnostic bundle to JSON if a report path is provided.

---

### 14. Optionally Export Diagnostic HTML Report

```python
if html_report_path is not None:
    html_report = render_html_report(
        diagnostic_bundle=diagnostic_bundle,
        pipeline_status=pipeline_status,
    )
    export_report_to_html(
        html_report=html_report,
        output_path=html_report_path,
    )
```

Writes a static, self-contained HTML report if an HTML report path is provided.

---

### 15. Optionally Export Quarantine Candidate JSON

```python
if quarantine_candidates_path is not None:
    export_quarantine_candidates_to_json(
        quarantine_candidates=quarantine_candidates,
        output_path=quarantine_candidates_path,
    )
```

Writes only the `quarantine_candidates` report section as JSON.

---

### 16. Optionally Export Quarantine Rows CSV

```python
if quarantine_rows_path is not None:
    quarantine_rows = select_quarantine_rows(table, quarantine_candidates)
    export_table_to_csv(quarantine_rows, quarantine_rows_path)
```

Writes only rows listed as quarantine candidates.

---

### 17. Optionally Export Accepted Rows CSV

```python
if accepted_rows_path is not None:
    accepted_rows = select_accepted_rows(table, quarantine_candidates)
    export_table_to_csv(accepted_rows, accepted_rows_path)
```

Writes rows not listed as quarantine candidates.

---

## Return Value

The pipeline returns:

```python
{
    "table": table,
    "quality_report": quality_report,
    "validation_results": validation_results,
    "diagnostic_bundle": diagnostic_bundle,
    "pipeline_status": pipeline_status,
}
```

---

## Example With Constraints, Strict Mode, Reports, and Quarantine Exports

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
    html_report_path="data/processed/customers_report.html",
    quarantine_candidates_path="data/processed/quarantine_candidates.json",
    quarantine_rows_path="data/processed/quarantine_rows.csv",
    accepted_rows_path="data/processed/accepted_rows.csv",
    constraints=constraints,
    strict_mode=True,
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
- decide CLI exit codes directly
- render HTML manually
- build quarantine row-selection logic directly

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
Pipeline Status
↓
Cleaned CSV
↓
Optional JSON Diagnostic Report
↓
Optional HTML Diagnostic Report
↓
Optional Quarantine Candidate JSON
↓
Optional Quarantine Rows CSV
↓
Optional Accepted Rows CSV
```

---

## Current Scope

Supported now:

```text
CSV input
CSV output
optional JSON diagnostic report
optional HTML diagnostic report
optional quarantine candidate JSON export
optional quarantine rows CSV export
optional accepted rows CSV export
optional constraint validation
optional strict status mode
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
quarantine candidate reporting
pipeline status reporting
```

---

## Safety Policy

```text
normal cleaned CSV includes all rows
quarantine exports are optional and explicit
quarantine export does not mutate the original table
strict mode behavior is unchanged
```

---

## Future Improvements

Possible future additions:

- report path auto-generation
- selectable strict policy modes
- source file metadata in diagnostic bundle
- output file metadata in diagnostic bundle
- execution duration
- pipeline version
- cleaning profile support
- batch CSV processing
- richer quarantine export metadata
- richer HTML report sections
