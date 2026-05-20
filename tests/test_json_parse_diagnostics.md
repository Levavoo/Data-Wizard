# JSON Parse Diagnostics Tests

Tests for the JSON parse diagnostics helper.

Covered behavior:

```text
default serialization
warning recording
nested value column recording
array value column recording
invalid record index recording
```

Run:

```bash
python -m pytest tests/test_json_parse_diagnostics.py
```
