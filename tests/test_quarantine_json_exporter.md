# test_quarantine_json_exporter.py

## Purpose

Tests dedicated quarantine candidate JSON export.

---

## Tested File

```text
data_processor/exporters/quarantine_json_exporter.py
```

---

## Covered Behavior

- writes quarantine candidate JSON file
- creates parent directories
- preserves candidate report structure

---

## Run Tests

```bash
python -m pytest tests/test_quarantine_json_exporter.py
```

---

## Design Rule

Exporter tests verify JSON writing only.

Candidate building and row selection are tested separately.
