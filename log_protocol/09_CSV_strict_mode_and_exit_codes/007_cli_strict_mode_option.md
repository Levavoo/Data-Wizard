# Protocol — Stage G CLI Strict Mode Option

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/09_CSV_strict_mode_and_exit_codes.md` |
| Stage | Stage G — CLI Strict Mode Option |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | CLI integration, tests, documentation |

---

## Purpose

Add CLI support for strict mode and predictable exit codes.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `scripts/run_csv_pipeline.py` | Modified | Adds `--strict`, pipeline status output, and exit codes. |
| `scripts/run_csv_pipeline.md` | Modified | Documents strict mode and exit codes. |
| `tests/test_cli_strict_mode.py` | Created | Tests CLI exit-code behavior. |
| `tests/test_cli_strict_mode.md` | Created | Documents CLI strict-mode tests. |
| `log_protocol/09_CSV_strict_mode_and_exit_codes/007_cli_strict_mode_option.md` | Created | Records Stage G completion. |

---

## Behavior Added

```text
--strict option
exit code 0 for successful non-strict execution
exit code 1 for execution error
exit code 2 for strict policy failure
```

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_cli_strict_mode.py
```

Status:

```text
Not executed by assistant in this environment.
```
