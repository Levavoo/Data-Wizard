# Protocol — Stage G Pipeline Parameter Support

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/14_CSV_encoding_and_delimiter_detection.md` |
| Stage | Stage G — Pipeline Parameter Support |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Pipeline integration |

---

## Purpose

Allow the pipeline to pass encoding and delimiter options to the CSV adapter.

---

## Pipeline Parameters Added

```python
encoding=None
delimiter=None
auto_detect_csv=True
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `data_processor/core/pipeline.py` | Modified | Passes CSV detection options to `CsvAdapter`. |
| `log_protocol/14_CSV_encoding_and_delimiter_detection/007_pipeline_detection_options.md` | Created | Records Stage G completion. |

---

## Behavior Added

```text
pipeline can use explicit encoding
pipeline can use explicit delimiter
pipeline can disable adapter auto-detection
existing calls remain valid
```

---

## Tests / Checks

Covered through CLI and adapter tests.

Status:

```text
Not executed by assistant in this environment.
```
