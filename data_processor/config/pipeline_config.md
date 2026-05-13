# pipeline_config.py

## Purpose

`pipeline_config.py` loads and validates JSON config files for CSV pipeline execution.

It belongs to the configuration layer.

Architecture:

```text
JSON config file
→ config loader
→ validated config dictionary
```

---

## Main Functions

### `load_pipeline_config(path)`

Loads a UTF-8 JSON config file and validates it.

---

### `validate_pipeline_config(config)`

Validates a config dictionary.

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
encoding
delimiter
auto_detect_csv
```

---

## Detection Fields

| Field | Meaning |
|---|---|
| `encoding` | Optional explicit CSV text encoding |
| `delimiter` | Optional explicit CSV delimiter |
| `auto_detect_csv` | Whether missing CSV encoding/delimiter settings should be detected |

---

## Validation Rules

The loader validates:

```text
config is a JSON object
required fields are present
unknown fields are rejected
strict_mode is boolean when provided
auto_detect_csv is boolean when provided
encoding is string when provided
delimiter is string when provided
```

---

## Design Rules

This module must not:

- run the pipeline
- load constraints
- resolve profiles
- write output files
- mutate data

Those responsibilities belong to separate modules.
