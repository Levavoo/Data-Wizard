# test_cli_pipeline_config.py

## Purpose

Tests CLI execution from a CSV pipeline config file.

---

## Tested File

```text
scripts/run_csv_pipeline.py
```

---

## Covered Behavior

- CLI can run from `--config` without positional input/output paths
- config-driven CLI can write report outputs
- config-driven CLI can write quarantine exports
- config `strict_mode` can trigger exit code `2`

---

## Run Tests

```bash
python -m pytest tests/test_cli_pipeline_config.py
```

---

## Design Rule

CLI config tests verify config wiring and execution behavior.

Config loading and validation are tested separately.
