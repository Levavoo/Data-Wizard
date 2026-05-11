# test_diagnostic_bundle.py

## Purpose

Tests the diagnostic bundle module.

This verifies that quality reports, profiles, parser diagnostics, row classification, type diagnostics, and validation reports are combined into one structured report.

Architecture:

```text
Table + Validation Results
→ Diagnostic Bundle
→ Complete Report Dictionary
```

---

## Tested File

```text
data_processor/reports/diagnostic_bundle.py
```

---

## Current Test Coverage

### `test_build_diagnostic_bundle_contains_top_level_fields`

Verifies the bundle contains:

- table name
- row count
- column count
- quality report
- column profiles
- row profiles
- row classification
- type diagnostics
- validation report

---

### `test_build_diagnostic_bundle_quality_report`

Verifies the quality report section is included and correctly generated.

---

### `test_build_diagnostic_bundle_column_profiles`

Verifies column profiles are included.

---

### `test_build_diagnostic_bundle_row_profiles`

Verifies row profiles are included.

---

### `test_build_diagnostic_bundle_row_classification`

Verifies suspicious row classification is included in the bundle.

Example:

```text
1,100
TOTAL,100
End of export,
```

Expected summary:

```text
normal_row: 1
summary_row: 1
footer_row: 1
```

---

### `test_build_diagnostic_bundle_type_diagnostics`

Verifies mixed-type diagnostics are included in the bundle.

---

### `test_build_diagnostic_bundle_validation_report`

Verifies validation results are summarized into the bundle.

---

### `test_build_diagnostic_bundle_empty_validation_report`

Verifies the validation report section exists even when no validation results are provided.

---

### `test_build_diagnostic_bundle_includes_table_metadata`

Verifies table metadata is included in the diagnostic bundle.

---

## Important Design Rule

Diagnostic bundles aggregate reports only.

They must never:

- clean data
- cast values
- modify tables
- remove rows
- export files
- validate constraints directly

---

## Run Tests

```bash
python -m pytest tests/test_diagnostic_bundle.py
```

---

## Developer Notes

The diagnostic bundle is the central report object for CLI summaries, audit reports, future UI dashboards, migration diagnostics, and quarantine workflows.
