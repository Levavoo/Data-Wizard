# test_csv_detection_integration.py

## Purpose

Tests CSV adapter integration with encoding and delimiter detection.

---

## Tested File

```text
data_processor/adapters/csv_adapter.py
```

---

## Covered Behavior

- semicolon delimiter detection
- explicit delimiter override
- UTF-8 BOM header handling
- explicit encoding override
- disabled auto-detection defaults
- detection diagnostics stored in table metadata

---

## Run Tests

```bash
python -m pytest tests/test_csv_detection_integration.py
```

---

## Design Rule

Detection utility behavior is tested separately.

These tests verify adapter wiring and metadata visibility.
