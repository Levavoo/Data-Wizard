# test_pipeline_status.py

## Purpose

Tests pipeline status building and exit-code conversion.

---

## Tested File

```text
data_processor/reports/pipeline_status.py
```

---

## Covered Behavior

- success status
- completed-with-warnings status
- non-strict validation failures
- strict-mode validation failure
- strict-mode quarantine error failure
- exit code `0` for successful execution
- exit code `2` for strict policy failure

---

## Run Tests

```bash
python -m pytest tests/test_pipeline_status.py
```

---

## Design Rule

Pipeline status is report/policy data.

It must not mutate data, remove rows, or raise policy failures as execution errors.
