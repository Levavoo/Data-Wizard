# customer_migration_config.json

## Purpose

Example CSV pipeline config for the customer migration sample.

---

## Run Command

```powershell
python scripts\run_csv_pipeline.py --config examples\csv\customer_migration_config.json
```

---

## Fields

| Field | Purpose |
|---|---|
| `input_path` | Source example CSV |
| `output_path` | Cleaned CSV output path |
| `profile` | Built-in cleaning profile |
| `constraints_path` | Example validation constraints |
| `report_path` | JSON diagnostic report path |
| `html_report_path` | HTML diagnostic report path |
| `quarantine_candidates_path` | Dedicated quarantine candidate JSON path |
| `quarantine_rows_path` | Dedicated quarantine rows CSV path |
| `accepted_rows_path` | Dedicated accepted rows CSV path |
| `strict_mode` | Explicit strict-mode setting |

---

## Output Paths

All output paths point to:

```text
data/processed/
```

That folder is ignored by Git except for `.gitkeep`.

---

## Design Rule

This config is explicit.

It does not rely on automatic output path generation.
