# test_example_csv_workflow.py

## Purpose

Tests the documented customer migration CSV example workflow.

This verifies that the example CSV and example constraint file are usable with the current pipeline.

---

## Tested Files

```text
examples/csv/customer_migration_sample.csv
examples/csv/customer_constraints.json
data_processor/core/pipeline.py
data_processor/validators/constraint_config.py
```

---

## Covered Behavior

- example CSV file exists
- example constraints JSON exists
- constraints JSON can be loaded
- pipeline can process the example CSV
- cleaned CSV output is written
- JSON diagnostic report is written
- diagnostic bundle contains expected report sections
- validation failures are detected
- suspicious rows are detected

---

## Run Test

```bash
python -m pytest tests/test_example_csv_workflow.py
```

---

## Design Rule

This is a workflow smoke test.

It should not duplicate every unit test for parsing, cleaning, validation, or reporting.
