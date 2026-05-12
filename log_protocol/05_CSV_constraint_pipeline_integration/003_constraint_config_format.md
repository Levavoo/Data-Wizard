# Protocol — Stage C Constraint Configuration Format

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/05_CSV_constraint_pipeline_integration.md` |
| Stage | Stage C — Constraint Configuration Format |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Design documentation |

---

## Purpose

Define the machine-readable JSON constraint config format.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/design/constraint_config_format.md` | Created | Documents constraint config format. |
| `log_protocol/05_CSV_constraint_pipeline_integration/003_constraint_config_format.md` | Created | Records Stage C completion. |

---

## Supported Types

```text
required
unique
min_value
max_value
allowed_values
regex_pattern
regex
```
