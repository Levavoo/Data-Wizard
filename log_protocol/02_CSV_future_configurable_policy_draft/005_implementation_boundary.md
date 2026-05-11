# Protocol — Stage E Future Implementation Boundary

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/02_CSV_future_configurable_policy_draft.md` |
| Stage | Stage E — Future Implementation Boundary |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Design documentation |

---

## Purpose

Define where future configurable null-token policy implementation should live.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/design/null_policy_implementation_boundary.md` | Created | Documents future implementation boundary. |
| `log_protocol/02_CSV_future_configurable_policy_draft/005_implementation_boundary.md` | Created | Records Stage E completion. |

---

## Proposed Future Files

```text
data_processor/cleaners/null_policy.py
data_processor/cleaners/null_policy.md
data_processor/cleaners/cleaning_profile.py
data_processor/cleaners/cleaning_profile.md
```

---

## Boundary Decision

Do not implement null policy logic in adapters, validators, or profilers.

---

## Production Code Decision

No production code change was made.
