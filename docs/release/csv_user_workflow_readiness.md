# CSV User Workflow Readiness Guide

## Purpose

This guide documents the current end-to-end CSV user workflows before release/merge readiness.

Plan:

```text
docs/plan_stages/17_CSV_core_stabilization_and_release_readiness.md
```

---

## Workflow 1 — Basic CSV Cleaning

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    tests\fixtures\csv\simple_customers.csv `
    data\processed\simple_customers_clean.csv
```

Expected output:

```text
cleaned CSV file
console summary
```

---

## Workflow 2 — Cleaning With Profile

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    tests\fixtures\csv\simple_customers.csv `
    data\processed\simple_customers_light_touch_clean.csv `
    --profile light_touch
```

Built-in profiles are documented in:

```text
docs/user_guides/csv_cleaning_profiles.md
```

---

## Workflow 3 — Config File Pipeline

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    --config examples\csv\customer_migration_config.json
```

Config file guide:

```text
docs/user_guides/csv_pipeline_config_files.md
```

---

## Workflow 4 — Constraint Validation

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    tests\fixtures\csv\real_world_messy_customers_heavy.csv `
    data\processed\real_world_clean.csv `
    --constraints-path tests\fixtures\csv\real_world_messy_customers_constraints.json
```

Expected output:

```text
clean CSV
validation report printed in console summary
```

---

## Workflow 5 — JSON Diagnostic Report

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    tests\fixtures\csv\real_world_messy_customers_heavy.csv `
    data\processed\real_world_clean.csv `
    --constraints-path tests\fixtures\csv\real_world_messy_customers_constraints.json `
    --report-path data\processed\real_world_report.json
```

Expected output:

```text
clean CSV
JSON diagnostic report
```

---

## Workflow 6 — HTML Diagnostic Report

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    tests\fixtures\csv\real_world_messy_customers_heavy.csv `
    data\processed\real_world_clean.csv `
    --constraints-path tests\fixtures\csv\real_world_messy_customers_constraints.json `
    --html-report-path data\processed\real_world_report.html
```

Open report:

```powershell
Start-Process data\processed\real_world_report.html
```

---

## Workflow 7 — Quarantine Exports

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    tests\fixtures\csv\real_world_messy_customers_heavy.csv `
    data\processed\real_world_clean.csv `
    --constraints-path tests\fixtures\csv\real_world_messy_customers_constraints.json `
    --quarantine-candidates-path data\processed\real_world_quarantine_candidates.json `
    --quarantine-rows-path data\processed\real_world_quarantine_rows.csv `
    --accepted-rows-path data\processed\real_world_accepted_rows.csv
```

Expected outputs:

```text
clean CSV
quarantine candidates JSON
quarantine rows CSV
accepted rows CSV
```

---

## Workflow 8 — Full Real-World Diagnostic Run

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    tests\fixtures\csv\real_world_messy_customers_heavy.csv `
    data\processed\real_world_messy_customers_clean.csv `
    --constraints-path tests\fixtures\csv\real_world_messy_customers_constraints.json `
    --report-path data\processed\real_world_messy_customers_report.json `
    --html-report-path data\processed\real_world_messy_customers_report.html `
    --quarantine-candidates-path data\processed\real_world_messy_customers_quarantine_candidates.json `
    --quarantine-rows-path data\processed\real_world_messy_customers_quarantine_rows.csv `
    --accepted-rows-path data\processed\real_world_messy_customers_accepted_rows.csv
```

Real-world guide:

```text
docs/testing/csv_real_world_test_suite.md
```

---

## Workflow 9 — Strict Mode

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    tests\fixtures\csv\real_world_messy_customers_heavy.csv `
    data\processed\real_world_strict_clean.csv `
    --constraints-path tests\fixtures\csv\real_world_messy_customers_constraints.json `
    --strict
```

Expected:

```text
strict policy failures affect process exit code
```

---

## Workflow 10 — Encoding and Delimiter Controls

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    tests\fixtures\csv\semicolon_customers.csv `
    data\processed\semicolon_customers_clean.csv `
    --delimiter ";" `
    --encoding utf-8
```

Detection guide:

```text
docs/user_guides/csv_encoding_and_delimiter_detection.md
```

---

## Workflow 11 — Performance Baseline

PowerShell:

```powershell
python scripts\performance\run_csv_performance_baseline.py `
    --rows 10000 `
    --json-report `
    --html-report
```

Performance guide:

```text
docs/performance/csv_performance_layer_guide.md
```

---

## Workflow 12 — Output Mode Performance Comparison

PowerShell:

```powershell
python scripts\performance\run_csv_output_mode_comparison.py `
    --rows 10000 `
    --output-dir data\performance\output_modes_10000
```

Expected output:

```text
comparison metrics JSON under data/performance/output_modes_10000/
```

---

## Output Policy

Generated outputs usually belong in:

```text
data/processed/
data/performance/
```

These files should not be committed by default.

See:

```text
docs/release/generated_artifact_policy.md
```

---

## Current Workflow Readiness

Ready for user-facing CLI workflows:

```text
basic cleaning
profiles
config files
constraint validation
JSON report
HTML report
quarantine exports
strict mode
encoding/delimiter control
real-world diagnostic run
performance baseline run
```

Not ready yet:

```text
GUI/web interface
JSON adapter
Excel adapter
streaming large-file processing
spreadsheet injection export hardening
semantic text column policy
```
