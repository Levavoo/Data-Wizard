# Protocol — Stage G Casting Policy Decision

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/03_CSV_mixed_type_diagnostics.md` |
| Stage | Stage G — Casting Policy Decision |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Design documentation |

---

## Purpose

Decide whether mixed-type diagnostics should influence casting behavior.

---

## Decision

Mixed-type diagnostics are report-only for now.

Current policy:

```text
diagnostics only, no casting change
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/design/mixed_type_casting_policy.md` | Created | Documents casting policy decision. |
| `log_protocol/03_CSV_mixed_type_diagnostics/007_casting_policy_decision.md` | Created | Records Stage G completion. |

---

## Reason

Automatic casting or quarantine behavior should wait until these systems exist:

```text
row quarantine
cleaning profiles
column-specific casting policies
issue report export
```

---

## Production Code Decision

No casting behavior was changed.
