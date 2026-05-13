# Protocol — Stage I CI/Automation Usage Guide

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/09_CSV_strict_mode_and_exit_codes.md` |
| Stage | Stage I — CI/Automation Usage Guide |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Development documentation |

---

## Purpose

Document how strict mode can be used in automated workflows.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/development/strict_mode_ci_usage.md` | Created | Explains strict-mode use in CI and automation. |
| `log_protocol/09_CSV_strict_mode_and_exit_codes/009_ci_usage_guide.md` | Created | Records Stage I completion. |

---

## Policy

Strict mode is not added to the default GitHub Actions workflow yet.

Reason:

```text
strict data checks should be added only when target data files and policies are stable
```
