# Protocol — Stage D Delimiter Detection Utility

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/14_CSV_encoding_and_delimiter_detection.md` |
| Stage | Stage D — Delimiter Detection Utility |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Adapter utility, tests, documentation |

---

## Purpose

Add a delimiter detection utility that samples text and chooses a likely delimiter conservatively.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `data_processor/adapters/delimiter_detection.py` | Created | Detects likely delimiter and returns diagnostics. |
| `data_processor/adapters/delimiter_detection.md` | Created | Documents delimiter detection utility. |
| `tests/test_delimiter_detection.py` | Created | Tests comma, semicolon, tab, pipe, fallback, and ambiguity. |
| `tests/test_delimiter_detection.md` | Created | Documents delimiter detection tests. |
| `log_protocol/14_CSV_encoding_and_delimiter_detection/004_delimiter_detection_utility.md` | Created | Records Stage D completion. |

---

## Behavior Added

```text
candidate score diagnostics
consistent-row scoring
fallback to comma when no viable candidate exists
fallback to comma when detection is ambiguous
```

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_delimiter_detection.py
```

Status:

```text
Not executed by assistant in this environment.
```
