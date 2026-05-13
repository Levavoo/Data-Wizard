# run_csv_pipeline.py

## Purpose

`run_csv_pipeline.py` is the command-line runner for the CSV cleaning pipeline.

It allows the project to be used from PowerShell without writing Python code manually.

Architecture:

```text
PowerShell Command
→ run_csv_pipeline.py
→ optional cleaning profile resolution
→ data_processor.core.pipeline.run_csv_pipeline()
→ cleaned CSV output
→ optional diagnostic JSON report
→ optional diagnostic HTML report
→ optional quarantine exports
→ process exit code
```

---

## Main Responsibilities

This script handles:

- reading command-line arguments
- resolving optional built-in cleaning profiles
- loading optional constraint JSON files
- calling the CSV pipeline
- printing the input path
- printing the output path
- printing selected profile information
- printing diagnostic report paths if provided
- printing quarantine export paths if provided
- printing the pipeline status
- printing the quality report summary
- printing the validation report summary
- returning CLI exit codes

It does not handle:

- CSV parsing directly
- cleaning directly
- validation directly
- report construction directly
- exporting directly
- HTML rendering directly
- quarantine row selection directly
- external config files

Those responsibilities belong to the core project modules.

---

## Main Functions

### `parse_arguments()`

Reads command-line arguments.

Required arguments:

```text
input_path
output_path
```

Optional arguments:

```text
--profile
--report-path
--html-report-path
--quarantine-candidates-path
--quarantine-rows-path
--accepted-rows-path
--constraints-path
--strict
--no-strict
```

---

### `load_constraints_from_path(path)`

Loads an optional JSON constraint file and converts it into `Constraint` objects.

---

### `resolve_cli_strict_override(args)`

Converts explicit CLI strict flags into an override value:

```text
--strict → True
--no-strict → False
no strict flag → None
```

---

### `main()`

Main script entry point.

Flow:

```text
parse arguments
→ resolve optional profile
→ load optional constraints
→ run pipeline
→ print summary
→ print pipeline status
→ print quality report
→ print validation report
→ return exit code
```

---

## Built-In Profiles

Available profiles:

```text
default
light_touch
migration_audit
strict_crm
```

Profiles currently define:

```text
strict mode default
recommended output types
profile description
profile notes
```

Profiles do not generate output paths automatically in this stage.

---

## Profile Override Rules

Explicit CLI options override profile defaults.

Examples:

```text
--profile strict_crm --no-strict
```

means:

```text
use strict_crm profile metadata but disable strict mode
```

```text
--profile default --strict
```

means:

```text
use default profile metadata but enable strict mode
```

---

## Exit Codes

```text
0 = successful execution, including non-strict runs with warnings/errors reported
1 = execution error
2 = strict policy failure
```

Important:

```text
Exit code 2 means processing completed but strict policy failed.
Exit code 1 means the command itself failed to execute successfully.
```

---

## Example Usage Without Profile

```powershell
python scripts\run_csv_pipeline.py `
    data\raw\customers.csv `
    data\processed\customers_clean.csv
```

No profile is required. This keeps existing behavior.

---

## Example Usage With Profile

```powershell
python scripts\run_csv_pipeline.py `
    data\raw\customers.csv `
    data\processed\customers_clean.csv `
    --profile migration_audit
```

---

## Example Usage With JSON and HTML Reports

```powershell
python scripts\run_csv_pipeline.py `
    data\raw\customers.csv `
    data\processed\customers_clean.csv `
    --profile migration_audit `
    --report-path data\processed\customers_report.json `
    --html-report-path data\processed\customers_report.html
```

---

## Example Usage With Quarantine Exports

```powershell
python scripts\run_csv_pipeline.py `
    data\raw\customers.csv `
    data\processed\customers_clean.csv `
    --profile migration_audit `
    --quarantine-candidates-path data\processed\quarantine_candidates.json `
    --quarantine-rows-path data\processed\quarantine_rows.csv `
    --accepted-rows-path data\processed\accepted_rows.csv
```

---

## Example Usage With Constraints, Reports, and Quarantine Exports

```powershell
python scripts\run_csv_pipeline.py `
    data\raw\customers.csv `
    data\processed\customers_clean.csv `
    --profile migration_audit `
    --constraints-path data\raw\customer_constraints.json `
    --report-path data\processed\customers_report.json `
    --html-report-path data\processed\customers_report.html `
    --quarantine-candidates-path data\processed\quarantine_candidates.json `
    --quarantine-rows-path data\processed\quarantine_rows.csv `
    --accepted-rows-path data\processed\accepted_rows.csv
```

---

## Example Usage With Strict Profile

```powershell
python scripts\run_csv_pipeline.py `
    data\raw\customers.csv `
    data\processed\customers_clean.csv `
    --profile strict_crm `
    --constraints-path data\raw\customer_constraints.json
```

`strict_crm` enables strict mode by default.

---

## Disable Strict Mode From a Strict Profile

```powershell
python scripts\run_csv_pipeline.py `
    data\raw\customers.csv `
    data\processed\customers_clean.csv `
    --profile strict_crm `
    --constraints-path data\raw\customer_constraints.json `
    --no-strict
```

---

## Constraint File Example

```json
[
    {
        "column": "customer_id",
        "type": "required"
    },
    {
        "column": "customer_id",
        "type": "unique"
    },
    {
        "column": "country",
        "type": "allowed_values",
        "values": ["Germany", "France", "Spain"]
    },
    {
        "column": "email",
        "type": "regex",
        "pattern": "^[^@]+@[^@]+\\.[^@]+$"
    }
]
```

---

## Expected Output

Example terminal output:

```text
CSV pipeline completed.

Input file: data\raw\customers.csv
Output file: data\processed\customers_clean.csv
Profile: strict_crm
Profile description: Strict CRM migration workflow for constraint-sensitive imports.
Diagnostic JSON report: data\processed\customers_report.json
Diagnostic HTML report: data\processed\customers_report.html
Quarantine candidates JSON: data\processed\quarantine_candidates.json
Quarantine rows CSV: data\processed\quarantine_rows.csv
Accepted rows CSV: data\processed\accepted_rows.csv
Constraints file: data\raw\customer_constraints.json
Strict mode: True

Pipeline status:
...

Quality report:
...

Validation report:
...
```

---

## Quarantine Export Safety

```text
normal cleaned CSV still includes all rows
quarantine rows CSV is an additional explicit review file
accepted rows CSV is an additional explicit split file
rows are not deleted automatically
```

---

## Important Design Rule

CLI scripts should be thin.

They should only:

```text
receive input
resolve simple built-in profile defaults
load simple config files
call project modules
show output
return process exit codes
```

They should not contain business logic.

---

## Current Workflow

```text
CSV File
→ CLI Runner
→ Optional Built-In Profile Resolver
→ Optional Constraint Config Loader
→ Pipeline
→ Pipeline Status
→ Cleaned CSV
→ Optional Diagnostic JSON Report
→ Optional Diagnostic HTML Report
→ Optional Quarantine Candidate JSON
→ Optional Quarantine Rows CSV
→ Optional Accepted Rows CSV
→ Exit Code
```

---

## Validation Command

```powershell
ruff check scripts\run_csv_pipeline.py
black scripts\run_csv_pipeline.py
```

---

## Manual Test Command

```powershell
python scripts\run_csv_pipeline.py `
    data\raw\customers.csv `
    data\processed\customers_clean.csv `
    --profile strict_crm `
    --constraints-path data\raw\customer_constraints.json `
    --report-path data\processed\customers_report.json `
    --html-report-path data\processed\customers_report.html `
    --quarantine-candidates-path data\processed\quarantine_candidates.json `
    --quarantine-rows-path data\processed\quarantine_rows.csv `
    --accepted-rows-path data\processed\accepted_rows.csv
```

---

## Future Improvements

Possible future additions:

- verbose mode
- dry-run mode
- selectable strict policy modes
- external profile config files
- config-file pipeline execution
- automatic output path generation
- batch folder processing
- logging
- more granular exit codes
- richer HTML report rendering
- quarantine export summaries in CLI output
