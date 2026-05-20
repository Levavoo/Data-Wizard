# test_delimiter_detection.py

## Purpose

Tests conservative CSV delimiter detection.

---

## Tested File

```text
data_processor/adapters/delimiter_detection.py
```

---

## Covered Behavior

- detects comma delimiter
- detects semicolon delimiter
- detects tab delimiter
- detects pipe delimiter
- falls back to comma when no viable delimiter exists
- falls back to comma when detection is ambiguous

---

## Run Tests

```bash
python -m pytest tests/test_delimiter_detection.py
```

---

## Design Rule

Delimiter detection tests verify detection diagnostics only.

CSV adapter integration is tested separately.
