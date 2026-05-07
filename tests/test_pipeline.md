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
→ Inference
→ Quality Report
→ CSV Exporter
→ CSV Output
```

---

# Tested File

```text
data_processor/core/pipeline.py
```

---

# Current Test Coverage

## `test_run_csv_pipeline_creates_output_file`

Verifies:

- pipeline runs successfully
- output CSV file is created
- result contains table
- result contains quality report

---

## `test_run_csv_pipeline_quality_report`

Verifies the pipeline returns correct quality report values.

Checks:

- table name
- row count
- column count
- missing values by column

---

## `test_run_csv_pipeline_exports_cleaned_values`

Verifies cleaned values are written to the output file.

Examples:

```text
" Alice "
→ "Alice"

"YES"
→ "true"

"25.50"
→ "25.5"
```

---

# Important Design Rule

Pipeline tests verify orchestration.

They should not deeply test individual cleaners.

Individual modules already have their own dedicated tests.

---

# Run Tests

```powershell
pytest tests\test_pipeline.py
```

Expected result:

```text
3 passed
```

---

# Recommended Validation Workflow

```powershell
ruff check `
    data_processor\core\pipeline.py `
    tests\test_pipeline.py

black `
    data_processor\core\pipeline.py `
    tests\test_pipeline.py

pytest tests\test_pipeline.py
```

---

# Run Full Test Suite

```powershell
pytest
```

Expected result:

```text
80 passed
```

---

# Developer Notes

Pipeline tests should focus on:

- flow correctness
- file input/output
- module integration
- returned result structure

Avoid duplicating every cleaner test here.

---

# Future Improvements

Possible future additions:

- pipeline error handling tests
- invalid input file tests
- malformed CSV tests
- report export tests
- configurable pipeline tests
- dry-run mode tests