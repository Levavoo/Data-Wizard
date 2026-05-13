# Pipeline Config Override Policy

## Purpose

This document defines how explicit CLI values interact with values from a CSV pipeline config file.

---

## Policy

```text
--config provides defaults
explicit CLI arguments override config values when provided
```

---

## Override Fields

Explicit CLI values can override these config fields:

```text
input_path
output_path
profile
constraints_path
report_path
html_report_path
quarantine_candidates_path
quarantine_rows_path
accepted_rows_path
strict_mode via --strict or --no-strict
```

---

## Examples

Config contains:

```json
{
  "input_path": "input_a.csv",
  "output_path": "output_a.csv"
}
```

Command:

```powershell
python scripts\run_csv_pipeline.py input_b.csv output_b.csv --config config.json
```

Result:

```text
input_b.csv and output_b.csv are used
```

---

## Strict Override

Config contains:

```json
{
  "profile": "strict_crm",
  "strict_mode": true
}
```

Command:

```powershell
python scripts\run_csv_pipeline.py --config config.json --no-strict
```

Result:

```text
strict mode disabled
```

---

## Design Rule

Config files are inspectable defaults.

Explicit CLI values remain the final authority for command-line runs.
