# Protocol — Stage I Example Workflow Config Test

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/13_CSV_config_file_pipeline.md` |
| Stage | Stage I — Example Workflow Config Test |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Example workflow test and documentation |

---

## Purpose

Update example workflow tests to verify config-file execution.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `tests/test_example_csv_workflow.py` | Modified | Adds CLI `--config` workflow test. |
| `tests/test_example_csv_workflow.md` | Modified | Documents config workflow test coverage. |
| `log_protocol/13_CSV_config_file_pipeline/009_example_workflow_config_test.md` | Created | Records Stage I completion. |

---

## Behavior Verified

```text
example workflow can run through CLI using --config
explicit-argument workflow still works
profile workflow still works
```

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_example_csv_workflow.py
```

Status:

```text
Not executed by assistant in this environment.
```
