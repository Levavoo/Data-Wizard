# CSV Real-World Test Suite Guide

## Purpose

The real-world CSV test suite verifies how the current pipeline behaves with messy, realistic CSV data.

It is designed to reveal weaknesses.

It is not proof that the pipeline perfectly cleans every dirty CSV.

---

## Main Fixture

Heavy messy CSV fixture:

```text
tests/fixtures/csv/real_world_messy_customers_heavy.csv
```

Constraint config:

```text
tests/fixtures/csv/real_world_messy_customers_constraints.json
```

Constraint documentation:

```text
tests/fixtures/csv/real_world_messy_customers_constraints.md
```

---

## Expected and Observed Reports

Expected behavior report:

```text
docs/testing/real_world_messy_customers_expected_report.md
```

Observed weakness report:

```text
docs/testing/real_world_messy_customers_observed_weaknesses.md
```

Use the expected report to understand what the suite is trying to verify.

Use the observed weakness report to understand what the current pipeline still cannot do or should not claim to solve.

---

## What The Fixture Contains

The fixture includes:

```text
metadata before header
UTF-8 BOM
semicolon delimiter
duplicate headers
extra fields
missing fields
multiline quoted fields
escaped quotes
broken quote area
mixed number formats
mixed date formats
mixed boolean formats
ambiguous null tokens
invalid emails
duplicate IDs
duplicate emails
missing required values
leading-zero values
whitespace problems
formula-like text
HTML-like text
Unicode and emoji
summary/footer rows
range issues
```

---

## Test Files

Stage 15 tests:

```text
tests/test_real_world_messy_csv_observation.py
tests/test_real_world_parser_diagnostics.py
tests/test_real_world_cleaning_preservation.py
tests/test_real_world_quarantine_and_diagnostics.py
```

---

## Run The Full Real-World Suite

PowerShell:

```powershell
python -m pytest tests/test_real_world_messy_csv_observation.py
python -m pytest tests/test_real_world_parser_diagnostics.py
python -m pytest tests/test_real_world_cleaning_preservation.py
python -m pytest tests/test_real_world_quarantine_and_diagnostics.py
```

Or as one command:

```powershell
python -m pytest `
    tests/test_real_world_messy_csv_observation.py `
    tests/test_real_world_parser_diagnostics.py `
    tests/test_real_world_cleaning_preservation.py `
    tests/test_real_world_quarantine_and_diagnostics.py
```

---

## Generate Processed Outputs Locally

The real messy CSV should be run through the pipeline to inspect processed outputs.

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

Generated outputs:

```text
data/processed/real_world_messy_customers_clean.csv
data/processed/real_world_messy_customers_report.json
data/processed/real_world_messy_customers_report.html
data/processed/real_world_messy_customers_quarantine_candidates.json
data/processed/real_world_messy_customers_quarantine_rows.csv
data/processed/real_world_messy_customers_accepted_rows.csv
```

---

## Generated Output Policy

Generated processed outputs should usually not be committed.

Reason:

```text
they are reproducible artifacts
they may change whenever diagnostics improve
they add repository noise
```

Commit only:

```text
source fixtures
constraint config
expected report
observed weakness report
tests
documentation
```

Do not commit by default:

```text
data/processed/*.csv
data/processed/*.json
data/processed/*.html
```

---

## How To Inspect Outputs

Open cleaned CSV:

```powershell
code data\processed\real_world_messy_customers_clean.csv
```

Open JSON report:

```powershell
code data\processed\real_world_messy_customers_report.json
```

Open HTML report:

```powershell
Start-Process data\processed\real_world_messy_customers_report.html
```

Open quarantine rows:

```powershell
code data\processed\real_world_messy_customers_quarantine_rows.csv
```

Open accepted rows:

```powershell
code data\processed\real_world_messy_customers_accepted_rows.csv
```

---

## How To Interpret Test Failures

A failure can mean one of three things:

```text
1. real bug in the pipeline
2. expected current limitation that should be documented
3. test assumption mismatch with current report shape or fixture behavior
```

When a failure happens:

```text
check docs/testing/real_world_messy_customers_expected_report.md
check docs/testing/real_world_messy_customers_observed_weaknesses.md
inspect the generated JSON report if needed
fix code only when the expected behavior is already intended and reasonable
otherwise document the limitation honestly
```

---

## What The Suite Should Prove

The suite should prove that the pipeline can:

```text
survive a messy real-world CSV
identify encoding and delimiter
skip metadata before header
detect duplicate headers
report row-shape problems
perform safe text cleanup
preserve risky text as text
produce validation diagnostics
produce type diagnostics
produce suspicious row diagnostics
produce quarantine exports
produce accepted row exports
produce JSON and HTML reports
```

---

## What The Suite Should Not Claim

The suite should not claim that the pipeline fully solves:

```text
malformed quote repair
semantic postal code handling
leading-zero preservation for every identifier
spreadsheet injection protection
HTML sanitization
all date formats
all currency formats
all locale-specific boolean tokens
all phone validation
all country normalization
large-file streaming performance
```

These belong to future improvement stages.

---

## Useful Follow-Up Test Commands

Run parser-level checks:

```powershell
python -m pytest tests/test_real_world_parser_diagnostics.py
```

Run cleaning/preservation checks:

```powershell
python -m pytest tests/test_real_world_cleaning_preservation.py
```

Run quarantine/diagnostics checks:

```powershell
python -m pytest tests/test_real_world_quarantine_and_diagnostics.py
```

Run full test suite:

```powershell
python -m pytest
```

---

## Maintenance Rule

When the fixture reveals a new weakness:

```text
update docs/testing/real_world_messy_customers_observed_weaknesses.md
only add exact-count assertions after behavior is stable
prefer representative assertions for messy diagnostic behavior
keep generated outputs reproducible, not committed
```

---

## Next Possible Improvement Stages

Possible future stages:

```text
16_CSV_golden_snapshot_policy
17_CSV_semantic_text_columns
18_CSV_malformed_quote_diagnostics
19_CSV_spreadsheet_injection_export_safety
20_CSV_locale_profiles_for_dates_booleans_numbers
21_CSV_auto_output_path_generation
22_CSV_large_file_stress_test
```
