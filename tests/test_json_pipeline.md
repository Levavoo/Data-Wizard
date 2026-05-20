# JSON Pipeline Tests

Tests for running supported JSON input through the pipeline.

Covered behavior:

```text
clean CSV export
parse diagnostics in diagnostic bundle
constraint validation
JSON report export
optional performance timings
```

Run:

```bash
python -m pytest tests/test_json_pipeline.py
```
