# test_real_world_cleaning_preservation.py

## Purpose

Tests safe cleaning and preservation behavior for the heavy real-world messy customer CSV fixture.

Fixture:

```text
tests/fixtures/csv/real_world_messy_customers_heavy.csv
```

---

## Covered Behavior

The tests verify:

```text
leading/trailing whitespace is trimmed
repeated internal whitespace is collapsed where text cleaning applies
multiline quoted notes are preserved
escaped quote text is preserved
quoted delimiter characters inside notes are preserved
Unicode text is preserved
emoji text is preserved
formula-like text remains text
HTML-like text remains text
phone values remain text-like values
```

---

## Assertion Policy

These tests focus on safe cleaning and preservation.

They do not assert:

```text
validation failure counts
quarantine candidate counts
all numeric normalization behavior
all date normalization behavior
malformed quote recovery behavior
spreadsheet injection escaping
HTML sanitization
```

Those belong to later stages or future improvement plans.

---

## Important Safety Note

The risky text test does not claim spreadsheet injection hardening is solved.

It only checks that formula-like strings remain text and are not executed or reinterpreted by the pipeline.

---

## Run Tests

```bash
python -m pytest tests/test_real_world_cleaning_preservation.py
```

---

## Design Rule

Cleaning preservation tests should prove safe transformations and non-destructive text handling.

They should not pretend all messy data cases are cleaned perfectly.
