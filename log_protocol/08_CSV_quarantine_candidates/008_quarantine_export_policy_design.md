# Protocol — Stage H Quarantine Export Policy Design Only

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/08_CSV_quarantine_candidates.md` |
| Stage | Stage H — Quarantine Export Policy Design Only |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Design documentation |

---

## Purpose

Document future quarantine export behavior without implementing separate quarantine exports.

---

## Current Policy

```text
candidate report only
```

Current behavior:

```text
rows remain in cleaned CSV
rows remain in table
quarantine candidates are included in report JSON
no separate quarantine export is written
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/design/quarantine_export_policy.md` | Created | Documents future quarantine export behavior. |
| `log_protocol/08_CSV_quarantine_candidates/008_quarantine_export_policy_design.md` | Created | Records Stage H completion. |

---

## Production Code Decision

No quarantine export was implemented.

No row removal was implemented.
