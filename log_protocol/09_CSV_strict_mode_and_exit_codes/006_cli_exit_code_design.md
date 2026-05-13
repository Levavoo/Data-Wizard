# Protocol — Stage F CLI Exit Code Design

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/09_CSV_strict_mode_and_exit_codes.md` |
| Stage | Stage F — CLI Exit Code Design |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Design documentation |

---

## Purpose

Define CLI exit codes for CSV pipeline execution.

---

## Exit Codes

```text
0 = successful execution
1 = execution error
2 = strict policy failure
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/design/cli_exit_codes.md` | Created | Documents CLI exit codes. |
| `log_protocol/09_CSV_strict_mode_and_exit_codes/006_cli_exit_code_design.md` | Created | Records Stage F completion. |

---

## Production Code Decision

Implementation followed in Stage G.
