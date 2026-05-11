# Protocol — Stage B Policy Precedence Rules

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/02_CSV_future_configurable_policy_draft.md` |
| Stage | Stage B — Policy Precedence Rules |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Design documentation |

---

## Purpose

Define deterministic conflict resolution for global and column-specific null-token rules.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/design/null_policy_precedence.md` | Created | Documents null policy precedence rules. |
| `log_protocol/02_CSV_future_configurable_policy_draft/002_policy_precedence.md` | Created | Records Stage B completion. |

---

## Decision

Recommended precedence:

```text
1. column preserve_tokens
2. column extra_null_tokens
3. global preserve_tokens
4. global extra_null_tokens
5. default NULL_VALUES
```

---

## Production Code Decision

No production code change was made.
