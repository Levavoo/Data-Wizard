# Protocol — Stage C Encoding Detection Utility

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/14_CSV_encoding_and_delimiter_detection.md` |
| Stage | Stage C — Encoding Detection Utility |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Adapter utility, tests, documentation |

---

## Purpose

Add a dependency-free encoding detection utility.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `data_processor/adapters/encoding_detection.py` | Created | Detects readable text encoding and returns diagnostics. |
| `data_processor/adapters/encoding_detection.md` | Created | Documents encoding detection utility. |
| `tests/test_encoding_detection.py` | Created | Tests UTF-8, UTF-8 BOM, cp1252, and custom candidates. |
| `tests/test_encoding_detection.md` | Created | Documents encoding detection tests. |
| `log_protocol/14_CSV_encoding_and_delimiter_detection/003_encoding_detection_utility.md` | Created | Records Stage C completion. |

---

## Behavior Added

```text
utf-8-sig / utf-8 / cp1252 / latin-1 candidate order
selected_encoding diagnostics
candidate_results diagnostics
confidence and reason fields
```

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_encoding_detection.py
```

Status:

```text
Not executed by assistant in this environment.
```
