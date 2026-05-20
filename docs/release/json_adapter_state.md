# JSON Adapter State

## Purpose

Summarizes the completed first JSON adapter implementation.

---

## Completed Capabilities

```text
JsonAdapter reads supported JSON files
supported root shape is list of objects
keys are unioned into columns
missing keys become None
primitive values are preserved
nested objects become compact JSON strings
arrays become compact JSON strings
JSON parse diagnostics are attached to table metadata
JSON pipeline reuses cleaning, inference, validation, reporting, and exports
JSON CLI is available
JSON config support is available with input_format=json
JSON reports include parse diagnostics
```

---

## Main Files

```text
data_processor/adapters/json_adapter.py
data_processor/adapters/json_parse_diagnostics.py
data_processor/core/json_pipeline.py
scripts/run_json_pipeline.py
docs/user_guides/json_pipeline.md
```

---

## Tests

```text
tests/test_json_parse_diagnostics.py
tests/test_json_adapter.py
tests/test_json_pipeline.py
tests/test_cli_json_pipeline.py
tests/test_json_report_integration.py
tests/test_json_config_pipeline.py
```

---

## Unsupported JSON Features

```text
single root object
JSON Lines / NDJSON
root_path extraction
arbitrary deep flattening
array explosion
multi-table extraction
streaming parser
```

---

## Verification Commands

```powershell
python -m pytest tests/test_json_parse_diagnostics.py
python -m pytest tests/test_json_adapter.py
python -m pytest tests/test_json_pipeline.py
python -m pytest tests/test_cli_json_pipeline.py
python -m pytest tests/test_json_report_integration.py
python -m pytest tests/test_json_config_pipeline.py
python -m pytest
```

---

## Recommended Next Stage

```text
19_Excel_adapter
```

Alternative before Excel:

```text
JSON Lines / NDJSON support
JSON root_path support
JSON flattening policy
```
