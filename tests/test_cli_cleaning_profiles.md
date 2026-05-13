# test_cli_cleaning_profiles.py

## Purpose

Tests CLI cleaning profile behavior.

---

## Tested File

```text
scripts/run_csv_pipeline.py
```

---

## Covered Behavior

- `--profile strict_crm` enables strict mode by default
- `--no-strict` overrides strict profile behavior
- no-profile behavior remains non-strict by default
- explicit `--strict` overrides default profile behavior

---

## Run Tests

```bash
python -m pytest tests/test_cli_cleaning_profiles.py
```

---

## Design Rule

CLI profile tests verify argument behavior and profile override behavior.

Profile definitions and resolver behavior are tested separately.
