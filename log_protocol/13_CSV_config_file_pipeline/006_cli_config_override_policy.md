# Protocol — Stage F CLI Override Policy

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/13_CSV_config_file_pipeline.md` |
| Stage | Stage F — CLI Override Policy |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | CLI behavior, tests, documentation |

---

## Purpose

Define and implement how explicit CLI values interact with config file values.

---

## Policy

```text
--config provides defaults
explicit CLI arguments override config values when provided
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/design/pipeline_config_override_policy.md` | Created | Documents config override behavior. |
| `scripts/run_csv_pipeline.py` | Modified | Applies explicit CLI values over config values. |
| `tests/test_cli_pipeline_config_overrides.py` | Created | Tests CLI override behavior. |
| `tests/test_cli_pipeline_config_overrides.md` | Created | Documents override tests. |
| `log_protocol/13_CSV_config_file_pipeline/006_cli_config_override_policy.md` | Created | Records Stage F completion. |

---

## Behavior Added

```text
positional paths override config paths
explicit report path overrides config report path
--no-strict overrides config strict mode
--profile overrides config profile
```

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_cli_pipeline_config_overrides.py
```

Status:

```text
Not executed by assistant in this environment.
```
