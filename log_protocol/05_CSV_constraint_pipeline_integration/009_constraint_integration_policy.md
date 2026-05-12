# Protocol — Stage I Constraint Integration Policy

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/05_CSV_constraint_pipeline_integration.md` |
| Stage | Stage I — Constraint Integration Policy |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Design documentation |

---

## Purpose

Document what constraint validation should and should not do inside the CSV pipeline.

---

## Decision

Constraint validation is report-only for now.

Current policy:

```text
constraints report violations only
constraints do not clean values
constraints do not cast values
constraints do not quarantine rows
constraints do not block export by default
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/design/constraint_validation_policy.md` | Created | Documents validation policy. |
| `log_protocol/05_CSV_constraint_pipeline_integration/009_constraint_integration_policy.md` | Created | Records Stage I completion. |

---

## Production Code Decision

CSV export still runs even when validation failures exist.

Export-blocking or quarantine modes are deferred.
