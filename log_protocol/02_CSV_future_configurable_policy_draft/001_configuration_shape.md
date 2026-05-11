# Protocol — Stage A Configuration Shape Draft

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/02_CSV_future_configurable_policy_draft.md` |
| Stage | Stage A — Configuration Shape Draft |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Design documentation |

---

## Purpose

Define a future configuration shape for profile-driven null-token handling.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/design/null_token_profiles.md` | Created | Documents proposed null-token profile configuration. |
| `log_protocol/02_CSV_future_configurable_policy_draft/001_configuration_shape.md` | Created | Records Stage A completion. |

---

## Summary

The proposed shape includes:

```text
name
global_null_tokens
extra_null_tokens
preserve_tokens
columns
```

Column-specific behavior is designed to support overrides for future configurable cleaning profiles.

---

## Production Code Decision

No production code change was made.
