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

Verifies:

- pipeline runs successfully
- output CSV file is created
- result contains table
- result contains quality report
- result contains diagnostic bundle

---

### `test_run_csv_pipeline_quality_report`

Verifies the pipeline returns correct quality report values.

Checks:

- table name
- row count
- column count
- missing values by column

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

### `test_run_csv_pipeline_converts_whitespace_only_cells_to_null`

Verifies whitespace-only CSV cells become `None` during normal pipeline execution.

Examples:

```text
"   " → None
"\t" → None
```

This protects the expected interaction between CSV parsing, null cleaning, and text cleaning.

---

### `test_run_csv_pipeline_returns_diagnostic_bundle`

Verifies the pipeline returns a diagnostic bundle.

Checks:

- table name
- row count
- column count
- quality report section
- column profile section
- row profile section
- validation report section

---

### `test_run_csv_pipeline_exports_diagnostic_report`

Verifies the pipeline exports a JSON diagnostic report when `report_path` is provided.

Checks:

- cleaned CSV output exists
- JSON report exists
- JSON report can be read
- report contains expected diagnostic sections

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

Expected result:

```text
all tests pass
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

---

## Future Improvements

Possible future additions:

- optional constraints tests
- invalid input file tests
- malformed CSV tests
- strict/tolerant mode tests
- report metadata tests
- auto-generated report path tests
