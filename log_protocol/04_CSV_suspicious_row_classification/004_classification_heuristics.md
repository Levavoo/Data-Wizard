# Protocol — Stage D Classification Heuristics

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/04_CSV_suspicious_row_classification.md` |
| Stage | Stage D — Classification Heuristics |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Classification heuristics and tests |

---

## Purpose

Implement conservative heuristics for suspicious row categories.

---

## Classifications Implemented

```text
empty_row
comment_row
summary_row
footer_row
garbage_row
normal_row
```

---

## Behavior

Rows are classified with:

```text
row_index
classification
reason
confidence
row
```

---

## Production Code Decision

Classification is diagnostic-only. Rows are not removed, repaired, or quarantined.
