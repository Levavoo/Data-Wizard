# test_cli_csv_detection_options.py

## Purpose

Tests CLI CSV encoding and delimiter detection options.

---

## Tested File

```text
scripts/run_csv_pipeline.py
```

---

## Covered Behavior

- semicolon CSV can be read through auto-detection
- explicit delimiter override works
- explicit encoding override works
- auto-detection can be disabled
- CLI detection values override config detection values

---

## Run Tests

```bash
python -m pytest tests/test_cli_csv_detection_options.py
```

---

## Design Rule

CLI detection tests verify option wiring and report visibility.

Detection utility behavior is tested separately.
