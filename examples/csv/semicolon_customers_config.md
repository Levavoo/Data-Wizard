# semicolon_customers_config.json

## Purpose

Example config showing explicit semicolon delimiter handling.

---

## Run Command

```powershell
python scripts\run_csv_pipeline.py --config examples\csv\semicolon_customers_config.json
```

---

## Detection Fields

```json
{
  "delimiter": ";",
  "auto_detect_csv": true
}
```

The explicit delimiter value wins over detection.

---

## Output Paths

Outputs are written to:

```text
data/processed/
```

That folder is ignored by Git except for `.gitkeep`.
