# Protocol — Stage F CLI Constraint File Support

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/05_CSV_constraint_pipeline_integration.md` |
| Stage | Stage F — CLI Constraint File Support |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | CLI support and documentation |

---

## Purpose

Allow the CSV pipeline CLI to load constraints from a JSON file.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `scripts/run_csv_pipeline.py` | Modified | Adds `--constraints-path` support. |
| `scripts/run_csv_pipeline.md` | Modified | Documents CLI constraint file usage. |
| `log_protocol/05_CSV_constraint_pipeline_integration/006_cli_constraint_file_support.md` | Created | Records Stage F completion. |

---

## CLI Option Added

```text
--constraints-path
```

---

## Example

```bash
python scripts/run_csv_pipeline.py input.csv output.csv --constraints-path constraints.json --report-path report.json
```

---

## Tests / Checks

Recommended local/manual command:

```bash
python scripts/run_csv_pipeline.py data/raw/customers.csv data/processed/customers_clean.csv --constraints-path data/raw/customer_constraints.json --report-path data/processed/customers_report.json
```

Status:

```text
Not executed by assistant in this environment.
```
