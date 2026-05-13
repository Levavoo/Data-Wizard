# Strict Mode CI Usage

## Purpose

This guide explains how strict mode can be used in automated workflows.

Strict mode allows data-policy failures to produce a non-zero exit code.

---

## Command

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    examples\csv\customer_migration_sample.csv `
    data\processed\customer_migration_clean.csv `
    --constraints-path examples\csv\customer_constraints.json `
    --report-path data\processed\customer_migration_report.json `
    --strict
```

---

## Exit Codes

```text
0 = successful execution
1 = execution error
2 = strict policy failure
```

---

## Exit Code 2 Meaning

Exit code `2` means:

```text
CSV processing completed
cleaned CSV was written
report JSON was written if requested
serious diagnostics were found
strict policy failed
```

---

## Difference From Execution Error

```text
exit code 1 = the command failed to run successfully
exit code 2 = the command ran successfully but data failed strict policy
```

---

## CI Usage

A CI job can fail when strict policy fails because exit code `2` is non-zero.

Example:

```yaml
- name: Run strict CSV validation
  run: |
    python scripts/run_csv_pipeline.py examples/csv/customer_migration_sample.csv data/processed/customer_migration_clean.csv --constraints-path examples/csv/customer_constraints.json --report-path data/processed/customer_migration_report.json --strict
```

---

## Current Recommendation

Do not add strict data validation to the default GitHub Actions workflow yet.

Reason:

```text
strict data checks should be added only when target data files and policies are stable
```

---

## Future Work

Possible future additions:

```text
separate CI workflow for sample data validation
strict mode policy configuration
artifact upload for diagnostic reports
```
