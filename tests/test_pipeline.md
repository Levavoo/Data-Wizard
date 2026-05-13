# test_pipeline.py

## Purpose

Tests the CSV pipeline orchestrator.

This verifies that the full CSV workflow works end-to-end.

Architecture:

```text
CSV Input
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
```

---

## Tested File

```text
data_processor/core/pipeline.py
```

---

## Current Test Coverage

### `test_run_csv_pipeline_creates_output_file`

Verifies pipeline execution and output file creation.

Also verifies the result contains `validation_results`.

---

### `test_run_csv_pipeline_quality_report`

Verifies the pipeline returns correct quality report values.

---

### `test_run_csv_pipeline_exports_cleaned_values`

Verifies cleaned values are written to the output file.

---

### `test_run_csv_pipeline_exports_european_decimal_values`

Verifies European decimal values are inferred, cast, and exported correctly.

---

### `test_run_csv_pipeline_reports_mixed_type_diagnostics`

Verifies mostly numeric mixed-type columns are reported in the diagnostic bundle.

---

### `test_run_csv_pipeline_reports_suspicious_rows`

Verifies suspicious rows are reported in the diagnostic bundle without removing rows.

---

### `test_run_csv_pipeline_validates_constraints`

Verifies optional constraints are applied after cleaning and casting.

Covered constraints:

```text
unique
allowed_values
regex_pattern
min_value
```

Expected behavior:

```text
validation failures appear in diagnostic_bundle["validation_report"]
validation_results are returned by run_csv_pipeline()
cleaned table and CSV export remain available
```

---

### `test_run_csv_pipeline_reports_quarantine_candidates`

Verifies quarantine candidates are reported without removing rows.

Expected behavior:

```text
validation failures produce error candidates
suspicious rows produce warning candidates
cleaned table still contains all rows
CSV export still runs
```

---

### `test_run_csv_pipeline_converts_whitespace_only_cells_to_null`

Verifies whitespace-only CSV cells become `None` during normal pipeline execution.

---

### `test_run_csv_pipeline_returns_diagnostic_bundle`

Verifies the pipeline returns a diagnostic bundle including row classification, type diagnostics, and quarantine candidates.

---

### `test_run_csv_pipeline_exports_diagnostic_report`

Verifies the pipeline exports a JSON diagnostic report including row classification, type diagnostics, and quarantine candidates when `report_path` is provided.

---

## Important Design Rule

Pipeline tests verify orchestration.

They should not deeply test individual cleaners, profilers, validators, or exporters.

Individual modules already have their own dedicated tests.

---

## Run Tests

```bash
python -m pytest tests/test_pipeline.py
```

---

## Recommended Validation Workflow

```bash
ruff check data_processor/core/pipeline.py scripts/run_csv_pipeline.py tests/test_pipeline.py
black data_processor/core/pipeline.py scripts/run_csv_pipeline.py tests/test_pipeline.py
python -m pytest tests/test_pipeline.py
python -m pytest
```

---

## Developer Notes

Pipeline tests should focus on:

- flow correctness
- file input/output
- module integration
- returned result structure
- report export integration

Avoid duplicating every module-level test here.
