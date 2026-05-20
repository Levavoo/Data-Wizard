# Protocol — Stage G Example Config File

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/13_CSV_config_file_pipeline.md` |
| Stage | Stage G — Example Config File |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Example config and documentation |

---

## Purpose

Add a small example config file for the customer migration example.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `examples/csv/customer_migration_config.json` | Created | Provides runnable example pipeline config. |
| `examples/csv/customer_migration_config.md` | Created | Documents example config fields. |
| `log_protocol/13_CSV_config_file_pipeline/007_example_config_file.md` | Created | Records Stage G completion. |

---

## Behavior Added

```text
example config references existing example CSV
example config references existing constraints
example config writes outputs to data/processed
```
