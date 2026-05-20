# JSON Adapter Expected Report

## Purpose

Defines expected report behavior for JSON input.

---

## Expected Diagnostic Bundle Behavior

For supported JSON input, reports should include:

```text
metadata.source_format = json
parse_diagnostics.root_type
parse_diagnostics.record_count
parse_diagnostics.column_count
parse_diagnostics.missing_key_counts
parse_diagnostics.nested_value_columns
parse_diagnostics.array_value_columns
parse_diagnostics.warnings
```

---

## Nested Values

Nested objects and arrays should be visible in diagnostics.

They are currently converted to compact JSON strings instead of being flattened.

---

## Report Exports

JSON-origin parse diagnostics should appear in:

```text
diagnostic bundle
JSON report export
HTML report export
```
