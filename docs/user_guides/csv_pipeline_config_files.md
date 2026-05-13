# CSV Pipeline Config Files Guide

## Purpose

CSV pipeline config files make repeated workflows easier to run.

Instead of passing many CLI options every time, save them in one JSON file.

---

## Basic Command

PowerShell:

```powershell
python scripts\run_csv_pipeline.py --config examples\csv\customer_migration_config.json
```

---

## Example Config

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

## Profiles in Config Files

A config can reference a built-in profile:

```json
{
  "profile": "migration_audit"
}
```

Available profiles:

```text
default
light_touch
migration_audit
strict_crm
```

---

## CLI Overrides

Config files provide defaults.

Explicit CLI values override config values.

Example:

```powershell
python scripts\run_csv_pipeline.py `
    other_input.csv `
    other_output.csv `
    --config examples\csv\customer_migration_config.json
```

This uses the positional paths instead of the config paths.

---

## Strict Override

Config file has strict mode enabled:

```json
{
  "strict_mode": true
}
```

Disable it from CLI:

```powershell
python scripts\run_csv_pipeline.py `
    --config examples\csv\customer_migration_config.json `
    --no-strict
```

---

## Current Limitation

Config files do not generate output paths automatically.

Every output path must be explicit.

Future path generation may be added through:

```text
output_dir
auto_generate_report_paths
```

These are not implemented yet.
