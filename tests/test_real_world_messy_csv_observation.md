# test_real_world_messy_csv_observation.py

## Purpose

Runs the heavy real-world messy customer CSV fixture through the current pipeline as a baseline observation test.

Fixture:

```text
tests/fixtures/csv/real_world_messy_customers_heavy.csv
```

Constraints:

```text
tests/fixtures/csv/real_world_messy_customers_constraints.json
```

---

## Test Style

This is intentionally a broad observation test.

It avoids exact row counts and exact failure counts because the fixture includes:

```text
malformed rows
ambiguous values
mixed formats
broken quote area
summary/footer rows
```

---

## Covered Behavior

The test verifies:

```text
pipeline completes
cleaned CSV is written
JSON diagnostic report is written
HTML diagnostic report is written
quarantine candidate JSON is written
quarantine rows CSV is written
accepted rows CSV is written
diagnostic bundle contains expected sections
parse diagnostics include detection information
semicolon delimiter is detected
UTF-8 BOM encoding is detected
metadata-before-header is detected
validation failures exist
quarantine candidates exist
```

---

## Intentionally Not Covered Yet

This test does not assert:

```text
exact row count
exact validation failure count
exact quarantine candidate count
exact malformed quote behavior
exact extra/missing field counts
```

Those should be added only after baseline behavior is observed and documented.

---

## Run Test

```bash
python -m pytest tests/test_real_world_messy_csv_observation.py
```

---

## Design Rule

This test should reveal whether the current pipeline can survive a realistic messy CSV.

It should not pretend that all dirty cases are already solved.
