# run_csv_pipeline.py

## Purpose

`run_csv_pipeline.py` is the command-line runner for the CSV cleaning pipeline.

It allows the project to be used from PowerShell without writing Python code manually.

Architecture:

```text
PowerShell Command
→ run_csv_pipeline.py
→ data_processor.core.pipeline.run_csv_pipeline()
→ cleaned CSV output
→ optional diagnostic JSON report
```

---

## Main Responsibilities

This script handles:

- reading command-line arguments
- loading optional constraint JSON files
- calling the CSV pipeline
- printing the input path
- printing the output path
- printing the diagnostic report path if provided
- printing the quality report summary
- printing the validation report summary

It does not handle:

- CSV parsing directly
- cleaning directly
- validation directly
- report construction directly
- exporting directly

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
--report-path
--constraints-path
```

---

### `load_constraints_from_path(path)`

Loads an optional JSON constraint file and converts it into `Constraint` objects.

---

### `main()`

Main script entry point.

Flow:

```text
parse arguments
→ load optional constraints
→ run pipeline
→ print summary
→ print quality report
→ print validation report
```

---

## Example Usage Without Report Export

```powershell
python scripts\run_csv_pipeline.py `
    data\raw\customers.csv `
    data\processed\customers_clean.csv
```

---

## Example Usage With Report Export

```powershell
python scripts\run_csv_pipeline.py `
    data\raw\customers.csv `
    data\processed\customers_clean.csv `
    --report-path data\processed\customers_report.json
```

---

## Example Usage With Constraints

```powershell
python scripts\run_csv_pipeline.py `
    data\raw\customers.csv `
    data\processed\customers_clean.csv `
    --constraints-path data\raw\customer_constraints.json `
    --report-path data\processed\customers_report.json
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
Diagnostic report: data\processed\customers_report.json
Constraints file: data\raw\customer_constraints.json

Quality report:
...

Validation report:
...
```

---

## Import Path Handling

This script adds the project root to `sys.path`.

Reason:

When Python runs a script from the `scripts/` folder, Python may treat `scripts/` as the import root.

The project package lives here:

```text
data_processor/
```

---

## Important Design Rule

CLI scripts should be thin.

They should only:

```text
receive input
load simple config files
call project modules
show output
```

They should not contain business logic.

---

## Current Workflow

```text
CSV File
→ CLI Runner
→ Optional Constraint Config Loader
→ Pipeline
→ Cleaned CSV
→ Optional Diagnostic JSON Report
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
    --constraints-path data\raw\customer_constraints.json `
    --report-path data\processed\customers_report.json
```

---

## Developer Notes

This script intentionally uses:

```python
argparse
```

because it is part of the Python standard library.

No external CLI framework is needed yet.

---

## Future Improvements

Possible future additions:

- verbose mode
- dry-run mode
- strict/tolerant mode
- selectable cleaning profile
- batch folder processing
- logging
- exit codes
