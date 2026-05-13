# test_quarantine_row_selection.py

## Purpose

Tests row selection utilities for quarantine exports.

---

## Tested File

```text
data_processor/reports/quarantine_row_selection.py
```

---

## Covered Behavior

- extracts quarantine row indexes
- selects quarantine rows
- selects accepted rows
- handles empty candidates
- does not mutate the original table

---

## Run Tests

```bash
python -m pytest tests/test_quarantine_row_selection.py
```

---

## Design Rule

Row selection tests verify selection only.

CSV file writing is tested through pipeline and exporter tests.
