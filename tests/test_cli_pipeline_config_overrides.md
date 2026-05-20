# test_cli_pipeline_config_overrides.py

## Purpose

Tests CLI override behavior when `--config` is used.

---

## Tested File

```text
scripts/run_csv_pipeline.py
```

---

## Covered Behavior

- positional input/output paths override config paths
- explicit report path overrides config report path
- `--no-strict` overrides config strict mode
- explicit `--profile` overrides config profile

---

## Run Tests

```bash
python -m pytest tests/test_cli_pipeline_config_overrides.py
```

---

## Design Rule

Config files provide defaults.

Explicit CLI values are the final authority for command-line runs.
