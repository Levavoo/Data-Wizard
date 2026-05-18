# Protocol — Stage I CLI Detection Options

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/14_CSV_encoding_and_delimiter_detection.md` |
| Stage | Stage I — CLI Detection Options |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | CLI integration, tests, documentation |

---

## Purpose

Expose encoding and delimiter controls through CLI.

---

## CLI Options Added

```text
--encoding
--delimiter
--no-auto-detect-csv
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `scripts/run_csv_pipeline.py` | Modified | Adds CSV detection CLI options and passes them to the pipeline. |
| `tests/test_cli_csv_detection_options.py` | Created | Tests CLI detection behavior and config override behavior. |
| `tests/test_cli_csv_detection_options.md` | Created | Documents CLI detection tests. |
| `log_protocol/14_CSV_encoding_and_delimiter_detection/009_cli_detection_options.md` | Created | Records Stage I completion. |

---

## Behavior Added

```text
CLI accepts explicit encoding
CLI accepts explicit delimiter
CLI can disable auto-detection
CLI detection values override config values
```

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_cli_csv_detection_options.py
```

Status:

```text
Not executed by assistant in this environment.
```
