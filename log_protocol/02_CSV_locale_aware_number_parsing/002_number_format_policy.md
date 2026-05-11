# Protocol — Stage B Number Format Policy

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/02_CSV_locale_aware_number_parsing.md` |
| Stage | Stage B — Number Format Policy Design |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Design documentation |

---

## Purpose

Document supported numeric format policies.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/design/number_format_policy.md` | Created | Documents `auto`, `us`, and `eu` policies. |
| `log_protocol/02_CSV_locale_aware_number_parsing/002_number_format_policy.md` | Created | Records Stage B completion. |

---

## Policy Decision

Supported policies:

```text
auto
us
eu
```

Strict modes are deferred until parsing diagnostics and column-level policies exist.

---

## Production Code Decision

Implementation followed in Stage C.
