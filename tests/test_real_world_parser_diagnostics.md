# test_real_world_parser_diagnostics.py

## Purpose

Tests stable parser-level expectations for the heavy real-world messy customer CSV fixture.

Fixture:

```text
tests/fixtures/csv/real_world_messy_customers_heavy.csv
```

---

## Covered Behavior

The tests verify:

```text
UTF-8 BOM is detected as utf-8-sig
semicolon delimiter is detected
real header row is detected after metadata rows
preamble row count is recorded
duplicate Email header is detected
schema normalizes duplicate headers into email and email_2
extra field diagnostics exist
missing field diagnostics exist
metadata rows are preserved as preamble metadata
```

---

## Assertion Policy

These tests assert stable parser-level facts.

They intentionally avoid brittle assertions for:

```text
exact malformed quote recovery behavior
exact extra field row list
exact missing field row list
exact total row count
```

---

## Run Tests

```bash
python -m pytest tests/test_real_world_parser_diagnostics.py
```

---

## Design Rule

Parser diagnostics tests should focus on structural CSV parsing behavior only.

Cleaning, validation, quarantine, and preservation behavior belong to later Stage 15 tests.
