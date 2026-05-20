# JSON Config Pipeline Tests

Tests for running the JSON pipeline through config files.

Covered behavior:

```text
JSON CLI accepts config with input_format=json
JSON CLI writes clean CSV and report from config
JSON CLI rejects config with input_format=csv
```

Run:

```bash
python -m pytest tests/test_json_config_pipeline.py
```
