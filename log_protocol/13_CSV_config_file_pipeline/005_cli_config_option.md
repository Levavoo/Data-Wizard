# Protocol — Stage E CLI `--config` Support

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/13_CSV_config_file_pipeline.md` |
| Stage | Stage E — CLI `--config` Support |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | CLI integration, tests, documentation |

---

## Purpose

Allow the CLI to run from a JSON config file.

---

## CLI Option Added

```text
--config
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `scripts/run_csv_pipeline.py` | Modified | Adds config loading, optional positional paths, runtime option building. |
| `tests/test_cli_pipeline_config.py` | Created | Tests config-driven CLI execution. |
| `tests/test_cli_pipeline_config.md` | Created | Documents CLI config tests. |
| `log_protocol/13_CSV_config_file_pipeline/005_cli_config_option.md` | Created | Records Stage E completion. |

---

## Behavior Added

```text
CLI can run with --config without positional paths
existing positional CLI usage remains supported
config values are passed to pipeline
```

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_cli_pipeline_config.py
```

Status:

```text
Not executed by assistant in this environment.
```
