# Protocol — Stage G Quarantine Policy Decision

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/04_CSV_suspicious_row_classification.md` |
| Stage | Stage G — Quarantine Policy Decision |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Design documentation |

---

## Purpose

Decide whether suspicious row classification should affect quarantine or export behavior.

---

## Decision

Suspicious row classification is diagnostics-only for now.

Current policy:

```text
diagnostics only, no row removal
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/design/suspicious_row_quarantine_policy.md` | Created | Documents quarantine policy decision. |
| `log_protocol/04_CSV_suspicious_row_classification/007_quarantine_policy_decision.md` | Created | Records Stage G completion. |

---

## Reason

Automatic row removal can cause silent data loss.

Quarantine requires a dedicated row quarantine model, explicit policy, and report/export support.

---

## Production Code Decision

No quarantine or export behavior was changed.
