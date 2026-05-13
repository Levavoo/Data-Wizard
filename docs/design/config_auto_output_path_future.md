# Config Auto Output Path Future

## Purpose

This document records limitations of current config-file execution and future automatic output path generation ideas.

---

## Current Behavior

Config files require explicit output paths.

Current output path fields:

```text
output_path
report_path
html_report_path
quarantine_candidates_path
quarantine_rows_path
accepted_rows_path
```

---

## Current Limitation

The config file does not support:

```text
output_dir
auto_generate_report_paths
auto-generated report names
auto-generated quarantine export names
```

---

## Reason

Automatic path generation should be designed carefully to avoid unexpected file creation or overwriting.

---

## Future Option

Possible future config shape:

```json
{
  "input_path": "data/raw/customers.csv",
  "output_dir": "data/processed",
  "auto_generate_report_paths": true,
  "profile": "migration_audit"
}
```

Possible generated outputs:

```text
data/processed/customers_clean.csv
data/processed/customers_report.json
data/processed/customers_report.html
data/processed/customers_quarantine_candidates.json
data/processed/customers_quarantine_rows.csv
data/processed/customers_accepted_rows.csv
```

---

## Design Rule

Automatic path generation is deferred.

Current config files remain explicit-path only.
