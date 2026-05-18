# Protocol — Stage L Example Workflow Detection Test

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/14_CSV_encoding_and_delimiter_detection.md` |
| Stage | Stage L — Example Workflow Detection Test |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Integration tests |

---

## Purpose

Add workflow-level coverage for detection behavior.

---

## Behavior Verified

```text
semicolon CSV can be read through auto-detection
explicit delimiter override works
explicit encoding override works
auto-detection can be disabled
CLI detection values override config values
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `tests/test_cli_csv_detection_options.py` | Created | Provides workflow-level detection coverage through CLI. |
| `tests/test_cli_csv_detection_options.md` | Created | Documents detection workflow tests. |
| `log_protocol/14_CSV_encoding_and_delimiter_detection/012_example_workflow_detection_test.md` | Created | Records Stage L completion. |

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
