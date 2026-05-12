# Protocol — Stage C Example Constraint File

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/06_CSV_report_usability_and_examples.md` |
| Stage | Stage C — Example Constraint File |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Example constraint config and documentation |

---

## Purpose

Create a reusable example constraint JSON file for the customer migration sample.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `examples/csv/customer_constraints.json` | Created | Provides example validation rules. |
| `examples/csv/customer_constraints.md` | Created | Documents each example constraint. |
| `log_protocol/06_CSV_report_usability_and_examples/003_example_constraint_file.md` | Created | Records Stage C completion. |

---

## Constraints Included

```text
customer_id required
customer_id unique
country allowed values
email regex
amount min_value
```

---

## Production Code Decision

No production code change was made.
