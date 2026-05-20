# Protocol — Stage E CSV Adapter Integration

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/14_CSV_encoding_and_delimiter_detection.md` |
| Stage | Stage E — CSV Adapter Integration |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Adapter integration, tests, documentation |

---

## Purpose

Integrate encoding and delimiter detection into `CsvAdapter` while keeping explicit values supported.

---

## Adapter Parameters Added

```python
encoding=None
delimiter=None
auto_detect=True
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `data_processor/adapters/csv_adapter.py` | Modified | Uses explicit/detected encoding and delimiter and stores detection diagnostics. |
| `tests/test_csv_detection_integration.py` | Created | Tests adapter detection behavior and metadata. |
| `tests/test_csv_detection_integration.md` | Created | Documents adapter integration tests. |
| `log_protocol/14_CSV_encoding_and_delimiter_detection/005_csv_adapter_detection_integration.md` | Created | Records Stage E completion. |

---

## Behavior Added

```text
explicit encoding override
explicit delimiter override
auto-detected encoding
auto-detected delimiter
disabled auto-detection defaults
detection diagnostics stored in parse diagnostics
```

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_csv_detection_integration.py
```

Status:

```text
Not executed by assistant in this environment.
```
