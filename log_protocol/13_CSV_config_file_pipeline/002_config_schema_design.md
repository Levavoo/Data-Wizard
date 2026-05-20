# Protocol — Stage B CSV Pipeline Config Schema Design

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/13_CSV_config_file_pipeline.md` |
| Stage | Stage B — CSV Pipeline Config Schema Design |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Design documentation |

---

## Purpose

Define the initial JSON config file shape.

---

## Required Fields

```text
input_path
output_path
```

---

## Optional Fields

```text
profile
constraints_path
report_path
html_report_path
quarantine_candidates_path
quarantine_rows_path
accepted_rows_path
strict_mode
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/design/csv_pipeline_config_schema.md` | Created | Documents config schema and field meanings. |
| `log_protocol/13_CSV_config_file_pipeline/002_config_schema_design.md` | Created | Records Stage B completion. |

---

## Production Code Decision

Implementation followed in Stage C.
