# test_diagnostic_bundle.py

## Purpose

Tests the diagnostic bundle module.

This verifies that quality reports, column profiles, row profiles, and validation reports are combined into one structured report.

Architecture:

```text
Table + Validation Results
→ Diagnostic Bundle
→ Complete Report Dictionary
```

---

# Tested File

```text
data_processor/reports/diagnostic_bundle.py
```

---

# Current Test Coverage

## `test_build_diagnostic_bundle_contains_top_level_fields`

Verifies the bundle contains:

- table name
- row count
- column count
- quality report
- column profiles
- row profiles
- validation report

---

## `test_build_diagnostic_bundle_quality_report`

Verifies the quality report section is included and correctly generated.

---

## `test_build_diagnostic_bundle_column_profiles`

Verifies column profiles are included.

Checks:

- expected column keys
- missing count values

---

## `test_build_diagnostic_bundle_row_profiles`

Verifies row profiles are included.

Checks:

- row profile count
- missing values
- duplicate candidate detection

---

## `test_build_diagnostic_bundle_validation_report`

Verifies validation results are summarized into the bundle.

---

## `test_build_diagnostic_bundle_empty_validation_report`

Verifies the validation report section exists even when no validation results are provided.

---

# Important Design Rule

Diagnostic bundles aggregate reports only.

They must never:

- clean data
- cast values
- modify tables
- export files
- validate constraints directly

---

# Run Tests

```powershell
pytest tests\test_diagnostic_bundle.py
```

Expected:

```text
6 passed
```

---

# Recommended Validation Workflow

```powershell
ruff check `
    data_processor\reports\diagnostic_bundle.py `
    tests\test_diagnostic_bundle.py

black `
    data_processor\reports\diagnostic_bundle.py `
    tests\test_diagnostic_bundle.py

pytest tests\test_diagnostic_bundle.py
pytest
```

---

# Developer Notes

The diagnostic bundle will later be exported as JSON beside every cleaned dataset.

This becomes the central report object for:

- CLI summaries
- audit reports
- future UI dashboards
- migration diagnostics
- quarantine workflows

## `test_build_diagnostic_bundle_includes_table_metadata`

Verifies table metadata is included in the diagnostic bundle.

Useful for CSV diagnostics such as:

```text
source_format
encoding
delimiter
```