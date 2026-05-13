# Protocol — Stage B Quarantine Candidate Model Design

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/08_CSV_quarantine_candidates.md` |
| Stage | Stage B — Quarantine Candidate Model Design |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Design documentation |

---

## Purpose

Define the structured report model for quarantine candidates.

---

## Model Fields

```text
candidate_count
summary
candidates
row_index
severity
reason_count
reasons
row
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/design/quarantine_candidate_model.md` | Created | Documents candidate report model. |
| `log_protocol/08_CSV_quarantine_candidates/002_candidate_model_design.md` | Created | Records Stage B completion. |

---

## Production Code Decision

Implementation followed in Stage C.
