# test_type_diagnostics.py

## Purpose

Tests mixed-type diagnostic behavior.

These tests verify that type evidence can be collected without mutating values or changing schema inference.

---

## Tested File

```text
data_processor/inference/type_diagnostics.py
```

---

## Covered Behavior

- Current strict mixed-type inference fallback to `string`.
- Mostly numeric mixed columns report a dominant type.
- Invalid values are reported with row indexes.
- Null values do not count as invalid values.
- Threshold behavior prevents weak dominant-type detection.
- Mostly boolean mixed columns report invalid values.
- Table-level diagnostics collect mixed-type columns.

---

## Example

Input values:

```text
100
250.75
unknown
300
400
```

Expected diagnostics:

```text
dominant_type = float
invalid_values = row 2, value unknown
```

---

## Run Tests

```bash
python -m pytest tests/test_type_diagnostics.py
```

---

## Design Rule

Diagnostics are report-only.

They must not cast values, modify rows, set schema types, or quarantine records.
