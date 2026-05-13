# Protocol — Stage C Strict Mode Policy Design

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/09_CSV_strict_mode_and_exit_codes.md` |
| Stage | Stage C — Strict Mode Policy Design |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Design documentation |

---

## Purpose

Define opt-in strict-mode policy behavior.

---

## Policy

Strict mode fails when either condition is true:

```text
validation_report.failed_count > 0
quarantine_candidates.summary.error > 0
```

---

## Default Behavior

```text
strict_mode=False
```

Default mode remains report-only and backward-compatible.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/design/strict_mode_policy.md` | Created | Documents strict-mode behavior. |
| `log_protocol/09_CSV_strict_mode_and_exit_codes/003_strict_mode_policy.md` | Created | Records Stage C completion. |
