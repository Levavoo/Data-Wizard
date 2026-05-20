# Protocol — Stage H JSON Config Support

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/18_JSON_adapter.md` |
| Stage | Stage H — JSON Config Support |
| Branch | `codex` |
| Status | Implemented |

---

## Files Added / Modified

```text
data_processor/config/pipeline_config.py
data_processor/config/pipeline_config.md
data_processor/config/pipeline_config_resolver.py
data_processor/config/pipeline_config_resolver.md
scripts/run_json_pipeline.py
examples/json/json_customer_config.json
examples/json/README.md
tests/test_json_config_pipeline.py
tests/test_json_config_pipeline.md
```

---

## Behavior Added

```text
pipeline config supports optional input_format
allowed input_format values are csv and json
JSON CLI accepts --config
JSON CLI requires config input_format=json
CSV config default remains csv-compatible
```

---

## Next Stage

```text
Stage I — JSON User Guide
```
