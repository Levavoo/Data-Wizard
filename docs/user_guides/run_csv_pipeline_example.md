# Run the CSV Pipeline Example

## Purpose

This guide shows how to run the CSV pipeline with the example customer migration files.

You can produce:

```text
cleaned CSV output
JSON diagnostic report
HTML diagnostic report
quarantine candidate JSON
quarantine rows CSV
accepted rows CSV
optional strict-mode exit code
```

---

## Example Files

Input CSV:

```text
examples/csv/customer_migration_sample.csv
```

Constraint file:

```text
examples/csv/customer_constraints.json
```

---

## Output Files

Recommended output paths:

```text
data/processed/customer_migration_clean.csv
data/processed/customer_migration_report.json
data/processed/customer_migration_report.html
data/processed/quarantine_candidates.json
data/processed/quarantine_rows.csv
data/processed/accepted_rows.csv
```

The `data/processed/` folder is ignored by Git except for `.gitkeep`.

---

## Run With a Profile

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    examples\csv\customer_migration_sample.csv `
    data\processed\customer_migration_clean.csv `
    --profile migration_audit
```

Profiles select reusable workflow defaults.

Important:

```text
profiles do not generate output paths automatically yet
```

---

## Run With Profile, Reports, and Quarantine Exports

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    examples\csv\customer_migration_sample.csv `
    data\processed\customer_migration_clean.csv `
    --profile migration_audit `
    --constraints-path examples\csv\customer_constraints.json `
    --report-path data\processed\customer_migration_report.json `
    --html-report-path data\processed\customer_migration_report.html `
    --quarantine-candidates-path data\processed\quarantine_candidates.json `
    --quarantine-rows-path data\processed\quarantine_rows.csv `
    --accepted-rows-path data\processed\accepted_rows.csv
```

This runs:

```text
CSV parsing
cleaning
type inference
type-aware casting
quality reporting
row classification
mixed-type diagnostics
constraint validation
quarantine candidate reporting
pipeline status reporting
CSV export
JSON report export
HTML report export
quarantine candidate JSON export
quarantine rows CSV export
accepted rows CSV export
```

Because `migration_audit` is non-strict, the command exits with code `0` when execution succeeds, even if diagnostics report issues.

---

## Run With Strict Profile

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    examples\csv\customer_migration_sample.csv `
    data\processed\customer_migration_clean.csv `
    --profile strict_crm `
    --constraints-path examples\csv\customer_constraints.json `
    --report-path data\processed\customer_migration_report.json `
    --html-report-path data\processed\customer_migration_report.html `
    --quarantine-candidates-path data\processed\quarantine_candidates.json `
    --quarantine-rows-path data\processed\quarantine_rows.csv `
    --accepted-rows-path data\processed\accepted_rows.csv
```

`strict_crm` enables strict mode by default.

If serious policy failures are found, the command exits with:

```text
2
```

This means:

```text
processing completed, but strict policy failed
```

---

## Override Strict Profile

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    examples\csv\customer_migration_sample.csv `
    data\processed\customer_migration_clean.csv `
    --profile strict_crm `
    --constraints-path examples\csv\customer_constraints.json `
    --no-strict
```

This uses the `strict_crm` profile metadata but disables strict mode.

---

## Output Meaning

### Cleaned CSV

```text
data/processed/customer_migration_clean.csv
```

The normal cleaned CSV includes all processed rows.

This file is not changed by quarantine exports.

---

### Quarantine Candidate JSON

```text
data/processed/quarantine_candidates.json
```

Machine-readable list of candidate rows and reasons.

---

### Quarantine Rows CSV

```text
data/processed/quarantine_rows.csv
```

CSV containing only rows listed as quarantine candidates.

Use this for manual review.

---

### Accepted Rows CSV

```text
data/processed/accepted_rows.csv
```

CSV containing rows not listed as quarantine candidates.

This is an explicit split output.

---

## Expected Console Output

The CLI prints:

```text
CSV pipeline completed.
Input file: ...
Output file: ...
Profile: ...
Profile description: ...
Diagnostic JSON report: ...
Diagnostic HTML report: ...
Quarantine candidates JSON: ...
Quarantine rows CSV: ...
Accepted rows CSV: ...
Constraints file: ...
Strict mode: ...
Pipeline status:
...
Quality report:
...
Validation report:
...
```

---

## Exit Codes

```text
0 = successful execution
1 = execution error
2 = strict policy failure
```

---

## Inspect the Cleaned CSV

PowerShell:

```powershell
Get-Content data\processed\customer_migration_clean.csv
```

Expected behavior includes:

```text
null-like values normalized
US/EU numbers converted
booleans normalized
text trimmed
```

---

## Inspect the JSON Report

PowerShell:

```powershell
code data\processed\customer_migration_report.json
```

---

## Inspect the HTML Report

PowerShell:

```powershell
Start-Process data\processed\customer_migration_report.html
```

The HTML report is intended for human review in a browser.

---

## Inspect Quarantine Files

PowerShell:

```powershell
code data\processed\quarantine_candidates.json
Get-Content data\processed\quarantine_rows.csv
Get-Content data\processed\accepted_rows.csv
```

---

## Important Report Sections

Review these sections first:

```text
summary
pipeline status
quarantine candidates
validation report
row classification
type diagnostics
quality report
```

---

## What To Do After Reviewing

Typical next actions:

```text
fix invalid emails
review duplicate IDs
review unsupported countries
review summary/footer rows
review negative amounts
review null-like values
review quarantine candidates
```

---

## Important Safety Rule

The pipeline reports issues but does not automatically remove suspicious rows or quarantine candidates.

Quarantine exports are explicit additional files.

Strict mode reports policy failure through status and exit code only.
