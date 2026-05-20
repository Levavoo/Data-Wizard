# Protocol — Stage F Profile-Driven Output Path Policy

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/12_CSV_cleaning_profiles.md` |
| Stage | Stage F — Profile-Driven Output Path Policy |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Design documentation |

---

## Purpose

Define how profiles should handle generated output paths.

---

## Policy

```text
profiles can recommend output types
profiles do not generate output paths automatically in this stage
users must provide explicit output paths
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/design/profile_output_path_policy.md` | Created | Documents output path policy. |
| `log_protocol/12_CSV_cleaning_profiles/006_profile_output_path_policy.md` | Created | Records Stage F completion. |

---

## Production Code Decision

Automatic output path generation was not implemented.
