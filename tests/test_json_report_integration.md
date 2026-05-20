# JSON Report Integration Tests

Tests for JSON-origin diagnostics in exported reports.

Covered behavior:

```text
JSON report includes JSON parse diagnostics
HTML report includes parse diagnostics section
nested value columns appear in diagnostics
array value columns appear in diagnostics
```

Run:

```bash
python -m pytest tests/test_json_report_integration.py
```
