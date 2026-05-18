# Protocol — Stage K User Guide and Examples

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/14_CSV_encoding_and_delimiter_detection.md` |
| Stage | Stage K — User Guide and Examples |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | User documentation and example config |

---

## Purpose

Document detection behavior and add example commands/config snippets.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/user_guides/csv_encoding_and_delimiter_detection.md` | Created | Explains auto-detection, overrides, config fields, and diagnostics. |
| `examples/csv/semicolon_customers_config.json` | Created | Demonstrates explicit delimiter config. |
| `examples/csv/semicolon_customers_config.md` | Created | Documents semicolon config example. |
| `log_protocol/14_CSV_encoding_and_delimiter_detection/011_user_guide_and_examples.md` | Created | Records Stage K completion. |

---

## Behavior Documented

```text
encoding detection
CSV delimiter detection
explicit CLI overrides
config-file detection fields
diagnostics visibility
ambiguous fallback behavior
```
