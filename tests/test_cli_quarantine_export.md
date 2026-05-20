# test_cli_quarantine_export.py

## Purpose

Tests CLI quarantine export options.

---

## Tested File

```text
scripts/run_csv_pipeline.py
```

---

## Covered Behavior

- CLI accepts `--quarantine-candidates-path`
- CLI accepts `--quarantine-rows-path`
- CLI accepts `--accepted-rows-path`
- CLI writes quarantine candidate JSON
- CLI writes quarantine rows CSV
- CLI writes accepted rows CSV
- strict policy failure can still write quarantine exports

---

## Run Tests

```bash
python -m pytest tests/test_cli_quarantine_export.py
```

---

## Design Rule

CLI tests verify argument wiring and output file creation.

Quarantine candidate building and row selection are tested separately.
