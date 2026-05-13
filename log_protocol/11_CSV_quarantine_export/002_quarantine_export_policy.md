# Protocol — Stage B Quarantine Export Policy Design

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/11_CSV_quarantine_export.md` |
| Stage | Stage B — Quarantine Export Policy Design |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Design documentation |

---

## Purpose

Define explicit quarantine export modes and safety rules.

---

## Export Modes

```text
quarantine_candidates.json
quarantine_rows.csv
accepted_rows.csv
```

---

## Safety Policy

```text
normal cleaned CSV includes all rows
quarantine exports are explicit
row selection does not mutate the original table
strict mode behavior is unchanged
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/design/quarantine_export_modes.md` | Created | Documents quarantine export modes and safety policy. |
| `log_protocol/11_CSV_quarantine_export/002_quarantine_export_policy.md` | Created | Records Stage B completion. |

---

## Production Code Decision

Implementation followed in later stages.
