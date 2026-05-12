# Protocol — Stage B Pipeline Constraint Input Design

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/05_CSV_constraint_pipeline_integration.md` |
| Stage | Stage B — Pipeline Constraint Input Design |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Design documentation and pipeline interface |

---

## Purpose

Define how optional constraints are passed into the CSV pipeline.

---

## Decision

`run_csv_pipeline()` accepts:

```python
constraints: list[Constraint] | None = None
```

Existing calls without constraints still work.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/design/pipeline_constraint_input.md` | Created | Documents pipeline constraint input design. |
| `data_processor/core/pipeline.py` | Modified | Adds optional constraints parameter. |
| `log_protocol/05_CSV_constraint_pipeline_integration/002_pipeline_constraint_input_design.md` | Created | Records Stage B completion. |
