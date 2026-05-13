# CSV Cleaning Profiles Guide

## Purpose

CSV cleaning profiles provide reusable workflow defaults.

They help users choose an intended workflow without remembering every policy option.

---

## Current Built-In Profiles

```text
default
light_touch
migration_audit
strict_crm
```

---

## `default`

Matches the current no-profile behavior.

```text
strict mode: false
recommended outputs: none
```

Use when you want the normal explicit CLI workflow.

---

## `light_touch`

Minimal review workflow.

```text
strict mode: false
recommended outputs: JSON report
```

Use when you want basic diagnostics without strict policy failure.

---

## `migration_audit`

Audit-oriented migration workflow.

```text
strict mode: false
recommended outputs:
- JSON report
- HTML report
- quarantine candidates
- quarantine rows
- accepted rows
```

Use when you want to review issues before deciding whether the dataset should fail a strict policy.

---

## `strict_crm`

Strict CRM migration workflow.

```text
strict mode: true
recommended outputs:
- JSON report
- HTML report
- quarantine candidates
- quarantine rows
- accepted rows
```

Use when validation failures or error-level quarantine candidates should fail the command with exit code `2`.

---

## Basic Usage

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    data\raw\customers.csv `
    data\processed\customers_clean.csv `
    --profile migration_audit
```

---

## Profile With Explicit Outputs

Profiles currently do not generate output paths automatically.

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    data\raw\customers.csv `
    data\processed\customers_clean.csv `
    --profile migration_audit `
    --report-path data\processed\customers_report.json `
    --html-report-path data\processed\customers_report.html `
    --quarantine-candidates-path data\processed\quarantine_candidates.json `
    --quarantine-rows-path data\processed\quarantine_rows.csv `
    --accepted-rows-path data\processed\accepted_rows.csv
```

---

## Strict Profile

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    data\raw\customers.csv `
    data\processed\customers_clean.csv `
    --profile strict_crm `
    --constraints-path data\raw\customer_constraints.json
```

`strict_crm` enables strict mode by default.

---

## Override Strict Profile

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    data\raw\customers.csv `
    data\processed\customers_clean.csv `
    --profile strict_crm `
    --constraints-path data\raw\customer_constraints.json `
    --no-strict
```

This uses the profile metadata but disables strict mode.

---

## Explicit CLI Options Win

Explicit CLI options override profile defaults.

Examples:

```text
--profile strict_crm --no-strict
```

Result:

```text
strict mode disabled
```

```text
--profile default --strict
```

Result:

```text
strict mode enabled
```

---

## Current Limitation

Profiles do not yet load from external files.

Profiles do not yet generate output paths automatically.

These features are deferred to:

```text
13_CSV_config_file_pipeline
```
