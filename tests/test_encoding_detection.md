# test_encoding_detection.py

## Purpose

Tests conservative CSV text encoding detection.

---

## Tested File

```text
data_processor/adapters/encoding_detection.py
```

---

## Covered Behavior

- detects UTF-8 compatible files
- detects UTF-8 BOM files
- falls back to cp1252 when UTF-8 fails
- supports custom candidate list

---

## Run Tests

```bash
python -m pytest tests/test_encoding_detection.py
```

---

## Design Rule

Encoding detection tests verify detection diagnostics only.

CSV parsing is tested through the adapter and pipeline tests.
