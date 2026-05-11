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

---

### `test_run_csv_pipeline_quality_report`

Verifies the pipeline returns correct quality report values.

---

### `test_run_csv_pipeline_exports_cleaned_values`

Verifies cleaned values are written to the output file.

Examples:

```text
" Alice " → "Alice"
"YES" → "true"
"25.50" → "25.5"
```

---

### `test_run_csv_pipeline_exports_european_decimal_values`

Verifies European decimal values are inferred, cast, and exported correctly.

Examples:

```text
"1.000,50" → 1000.5
"250,75" → 250.75
"5.500,00" → 5500.0
```

---

### `test_run_csv_pipeline_reports_mixed_type_diagnostics`

Verifies mostly numeric mixed-type columns are reported in the diagnostic bundle.

Example:

```text
amount values: 100, 250.75, unknown, 300, 400
```

Expected diagnostic:

```text
dominant_type = float
invalid value = row 2, unknown
```

---

### `test_run_csv_pipeline_converts_whitespace_only_cells_to_null`

Verifies whitespace-only CSV cells become `None` during normal pipeline execution.

---

### `test_run_csv_pipeline_returns_diagnostic_bundle`

Verifies the pipeline returns a diagnostic bundle including type diagnostics.

---

### `test_run_csv_pipeline_exports_diagnostic_report`

Verifies the pipeline exports a JSON diagnostic report including type diagnostics when `report_path` is provided.

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
