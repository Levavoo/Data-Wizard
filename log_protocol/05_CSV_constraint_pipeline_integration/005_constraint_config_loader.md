# Protocol — Stage E Constraint Config Loader

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/05_CSV_constraint_pipeline_integration.md` |
| Stage | Stage E — Constraint Config Loader |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Config loader, tests, documentation |

---

## Purpose

Convert machine-readable constraint configuration dictionaries into `Constraint` objects.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `data_processor/validators/constraint_config.py` | Created | Implements config-to-constraint conversion. |
| `data_processor/validators/constraint_config.md` | Created | Documents config loader. |
| `tests/test_constraint_config.py` | Created | Tests config loader behavior. |
| `tests/test_constraint_config.md` | Created | Documents config loader tests. |
| `log_protocol/05_CSV_constraint_pipeline_integration/005_constraint_config_loader.md` | Created | Records Stage E completion. |

---

## Supported Types

```text
required
unique
min_value
max_value
allowed_values
regex_pattern
regex
```

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_constraint_config.py
```

Status:

```text
Not executed by assistant in this environment.
```
