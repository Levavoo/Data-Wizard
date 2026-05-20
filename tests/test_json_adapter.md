# JSON Adapter Tests

Tests for reading supported JSON files into the internal Table model.

Covered behavior:

```text
simple flat records
missing keys
nested object stringification
array stringification
unsupported root object
unsupported mixed list
wrong extension
```

Run:

```bash
python -m pytest tests/test_json_adapter.py
```
