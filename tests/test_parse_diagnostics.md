# test_parse_diagnostics.py

## Purpose

Tests for structured parse diagnostics.

These tests verify that parser diagnostics can be serialized, count row width problems, integrate with the CSV adapter, and appear in diagnostic bundles.

---

## Covered Behavior

- default `ParseDiagnostics` serialization
- extra field counting
- missing field counting
- CSV adapter metadata integration
- duplicate header diagnostics
- empty header diagnostics
- shifted header diagnostics
- diagnostic bundle top-level `parse_diagnostics` section

---

## Test Command

```bash
python -m pytest tests/test_parse_diagnostics.py
```

---

## Architecture Notes

These tests confirm that parse diagnostics stay structural only.

They do not test cleaning, validation, transformation, or quarantine behavior.
