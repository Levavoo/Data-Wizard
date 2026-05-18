# Protocol — Stage F Parse Diagnostics Integration

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/14_CSV_encoding_and_delimiter_detection.md` |
| Stage | Stage F — Parse Diagnostics Integration |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Diagnostics model and adapter integration |

---

## Purpose

Expose encoding and delimiter detection in parse diagnostics.

---

## Diagnostic Section Added

```text
parse_diagnostics.detection
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `data_processor/adapters/parse_diagnostics.py` | Modified | Adds `detection` diagnostics field. |
| `data_processor/adapters/csv_adapter.py` | Modified | Populates detection diagnostics. |
| `log_protocol/14_CSV_encoding_and_delimiter_detection/006_parse_diagnostics_integration.md` | Created | Records Stage F completion. |

---

## Behavior Added

```text
encoding detection diagnostics visible in parse diagnostics
delimiter detection diagnostics visible in parse diagnostics
override/default confidence values visible
```

---

## Tests / Checks

Covered through:

```bash
python -m pytest tests/test_csv_detection_integration.py
python -m pytest tests/test_cli_csv_detection_options.py
```

Status:

```text
Not executed by assistant in this environment.
```
