# CSV Pipeline Config Schema

## Purpose

This document defines the initial JSON config file shape for CSV pipeline execution.

---

## Required Fields

```text
input_path
output_path
```

---

## Optional Fields

```text
profile
constraints_path
report_path
html_report_path
quarantine_candidates_path
quarantine_rows_path
accepted_rows_path
strict_mode
```

---

## Example

```json
{
  "input_path": "examples/csv/customer_migration_sample.csv",
  "output_path": "data/processed/customer_migration_clean.csv",
  "profile": "migration_audit",
  "constraints_path": "examples/csv/customer_constraints.json",
  "report_path": "data/processed/customer_migration_report.json",
  "html_report_path": "data/processed/customer_migration_report.html",
  "quarantine_candidates_path": "data/processed/quarantine_candidates.json",
  "quarantine_rows_path": "data/processed/quarantine_rows.csv",
  "accepted_rows_path": "data/processed/accepted_rows.csv",
  "strict_mode": false
}
```

---

## Field Meanings

| Field | Meaning |
|---|---|
| `input_path` | Source CSV path |
| `output_path` | Cleaned CSV output path |
| `profile` | Optional built-in cleaning profile |
| `constraints_path` | Optional validation constraint JSON path |
| `report_path` | Optional diagnostic JSON report path |
| `html_report_path` | Optional diagnostic HTML report path |
| `quarantine_candidates_path` | Optional quarantine candidate JSON path |
| `quarantine_rows_path` | Optional quarantine rows CSV path |
| `accepted_rows_path` | Optional accepted rows CSV path |
| `strict_mode` | Optional strict-mode override |

---

## Future Fields

Deferred fields:

```text
output_dir
auto_generate_report_paths
null_policy
number_policy
encoding_policy
delimiter_policy
```

---

## Design Rule

Unknown fields should be rejected with a clear error.

Config files should be explicit and inspectable.
