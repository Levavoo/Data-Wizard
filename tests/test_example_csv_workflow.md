# test_example_csv_workflow.py

## Purpose

Tests the documented customer migration CSV example workflow.

This verifies that the example CSV, example constraint file, and example config file are usable with the current pipeline.

---

## Tested Files

```text
examples/csv/customer_migration_sample.csv
examples/csv/customer_constraints.json
examples/csv/customer_migration_config.json
data_processor/core/pipeline.py
data_processor/validators/constraint_config.py
scripts/run_csv_pipeline.py
```

---

## Covered Behavior

- example CSV file exists
- example constraints JSON exists
- example config JSON exists
- constraints JSON can be loaded
- pipeline can process the example CSV
- cleaned CSV output is written
- JSON diagnostic report is written
- HTML diagnostic report is written
- quarantine candidate JSON is written
- quarantine rows CSV is written
- accepted rows CSV is written
- diagnostic bundle contains expected report sections
- validation failures are detected
- suspicious rows are detected
- quarantine candidates are detected
- exported JSON report includes quarantine candidates
- exported HTML report includes expected sections
- quarantine rows contain review candidates
- accepted rows contain non-candidate rows
- CLI can run the example workflow with a cleaning profile
- CLI can run the example workflow with `--config`

---

## Run Test

```bash
python -m pytest tests/test_example_csv_workflow.py
```

---

## Design Rule

This is a workflow smoke test.

It should not duplicate every unit test for parsing, cleaning, validation, quarantine candidate building, row selection, HTML rendering, profile resolution, config loading, config resolution, or reporting.
