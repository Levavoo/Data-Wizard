# Protocol — Stage B Detection Policy Design

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/14_CSV_encoding_and_delimiter_detection.md` |
| Stage | Stage B — Detection Policy Design |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Design documentation |

---

## Purpose

Define conservative detection policy.

---

## Policy

```text
explicit encoding overrides detection
explicit delimiter overrides detection
UTF-8 compatible encodings are preferred
ambiguous delimiter detection falls back to comma
fallbacks and overrides are reported
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/design/csv_detection_policy.md` | Created | Documents encoding/delimiter detection policy and override precedence. |
| `log_protocol/14_CSV_encoding_and_delimiter_detection/002_detection_policy.md` | Created | Records Stage B completion. |

---

## Production Code Decision

Implementation followed in later stages.
