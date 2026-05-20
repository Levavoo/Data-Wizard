# test_real_world_quarantine_and_diagnostics.py

## Purpose

Tests diagnostic and quarantine behavior for the heavy real-world messy customer CSV fixture.

Fixture:

```text
tests/fixtures/csv/real_world_messy_customers_heavy.csv
```

Constraints:

```text
tests/fixtures/csv/real_world_messy_customers_constraints.json
```

---

## Covered Behavior

The tests verify:

```text
validation report has failures
type diagnostics are present
representative mixed/problem columns are diagnosed
row classification finds suspicious rows
summary/footer-like rows are surfaced somewhere in suspicious diagnostics
quarantine candidates exist
quarantine candidate JSON export is written
quarantine rows CSV export is written
accepted rows CSV export is written
JSON report includes expected diagnostic sections
HTML report includes expected diagnostic sections
```

---

## Assertion Policy

These tests use representative assertions.

They intentionally avoid exact counts for:

```text
validation failures
quarantine candidates
suspicious rows
type diagnostic items
```

Reason:

```text
the heavy fixture contains malformed and ambiguous data, and exact counts may change when diagnostics improve
```

---

## Run Tests

```bash
python -m pytest tests/test_real_world_quarantine_and_diagnostics.py
```

---

## Design Rule

These tests should confirm that dirty real-world data is surfaced for review.

They should not require automatic deletion, automatic repair, or perfect cleaning.
