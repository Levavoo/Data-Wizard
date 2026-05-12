# Run the CSV Pipeline Example

## Purpose

This guide shows how to run the CSV pipeline with the example customer migration files.

You will produce:

```text
cleaned CSV output
JSON diagnostic report
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
```

The `data/processed/` folder is ignored by Git except for `.gitkeep`.

---

## Run Without Constraints

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    examples\csv\customer_migration_sample.csv `
    data\processed\customer_migration_clean.csv `
    --report-path data\processed\customer_migration_report.json
```

This runs cleaning and diagnostics but does not apply user-defined validation rules.

---

## Run With Constraints

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    examples\csv\customer_migration_sample.csv `
    data\processed\customer_migration_clean.csv `
    --constraints-path examples\csv\customer_constraints.json `
    --report-path data\processed\customer_migration_report.json
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
CSV export
JSON report export
```

---

## Expected Console Output

The CLI prints:

```text
CSV pipeline completed.
Input file: ...
Output file: ...
Diagnostic report: ...
Constraints file: ...
Quality report:
...
Validation report:
...
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
Get-Content data\processed\customer_migration_report.json
```

For easier reading, open it in VS Code:

```powershell
code data\processed\customer_migration_report.json
```

---

## Important Report Sections

Review these sections first:

```text
parse_diagnostics
row_classification
validation_report
type_diagnostics
quality_report
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
```

---

## Important Limitation

The pipeline reports issues but does not automatically remove suspicious rows or block export on validation failures.

This is intentional for now.
