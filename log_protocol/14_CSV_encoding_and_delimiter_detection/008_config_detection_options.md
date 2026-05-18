# Protocol — Stage H Config File Support

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/14_CSV_encoding_and_delimiter_detection.md` |
| Stage | Stage H — Config File Support |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Config validation, resolver, tests, documentation |

---

## Purpose

Add config-file support for encoding and delimiter options.

---

## Config Fields Added

```text
encoding
delimiter
auto_detect_csv
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `data_processor/config/pipeline_config.py` | Modified | Accepts and validates detection fields. |
| `data_processor/config/pipeline_config.md` | Modified | Documents detection fields. |
| `data_processor/config/pipeline_config_resolver.py` | Modified | Resolves detection fields into runtime options. |
| `tests/test_pipeline_config.py` | Modified | Tests detection field validation. |
| `tests/test_pipeline_config_resolver.py` | Modified | Tests detection option resolution. |
| `log_protocol/14_CSV_encoding_and_delimiter_detection/008_config_detection_options.md` | Created | Records Stage H completion. |

---

## Behavior Added

```text
config accepts encoding
config accepts delimiter
config accepts auto_detect_csv
unknown field rejection remains intact
resolver passes values forward
```

---

## Tests / Checks

Recommended local commands:

```bash
python -m pytest tests/test_pipeline_config.py
python -m pytest tests/test_pipeline_config_resolver.py
```

Status:

```text
Not executed by assistant in this environment.
```
