# Protocol — Stage B Example Input Dataset

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/06_CSV_report_usability_and_examples.md` |
| Stage | Stage B — Example Input Dataset |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Example CSV and documentation |

---

## Purpose

Create a small realistic CSV sample that demonstrates the current diagnostics workflow.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `examples/csv/customer_migration_sample.csv` | Created | Provides a reproducible sample input file. |
| `examples/csv/customer_migration_sample.md` | Created | Explains the sample rows and intended diagnostics. |
| `log_protocol/06_CSV_report_usability_and_examples/002_example_input_dataset.md` | Created | Records Stage B completion. |

---

## Included Issues

```text
normal rows
missing values
weird null tokens
US/EU number formats
invalid email
duplicate customer ID
unsupported country
summary/footer rows
```

---

## Production Code Decision

No production code change was made.
