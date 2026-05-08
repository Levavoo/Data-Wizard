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

# Main Responsibilities

This script handles:

- reading command-line arguments
- calling the CSV pipeline
- printing the input path
- printing the output path
- printing the diagnostic report path if provided
- printing the quality report summary

It does not handle:

- CSV parsing directly
- cleaning directly
- validation directly
- report construction directly
- exporting directly

Those responsibilities belong to the core project modules.

---

# Main Functions

## `parse_arguments()`

Reads command-line arguments.

Required arguments:

```text
input_path
output_path
```

Optional arguments:

```text
--report-path
```

---

## `main()`

Main script entry point.

Flow:

```text
parse arguments
→ run pipeline
→ print summary
→ print quality report
```

---

# Example Usage Without Report Export

From the project root:

```powershell
python scripts\run_csv_pipeline.py `
    data\raw\customers.csv `
    data\processed\customers_clean.csv
```

---

# Example Usage With Report Export

```powershell
python scripts\run_csv_pipeline.py `
    data\raw\customers.csv `
    data\processed\customers_clean.csv `
    --report-path data\processed\customers_report.json
```

---

# Expected Output

Example terminal output:

```text
CSV pipeline completed.

Input file: data\raw\customers.csv
Output file: data\processed\customers_clean.csv
Diagnostic report: data\processed\customers_report.json

Quality report:
{
    "table_name": "customers",
    "row_count": 100,
    "column_count": 5,
    ...
}
```

---

# Import Path Handling

This script adds the project root to `sys.path`.

Reason:

When Python runs a script from the `scripts/` folder, Python may treat `scripts/` as the import root.

The project package lives here:

```text
data_processor/
```

So this block makes imports reliable:

```python
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
```

---

# Important Design Rule

CLI scripts should be thin.

They should only:

```text
receive input
call project modules
show output
```

They should not contain business logic.

---

# Project Position

This script makes the project usable as a local command-line tool.

Current workflow:

```text
CSV File
→ CLI Runner
→ Pipeline
→ Cleaned CSV
→ Optional Diagnostic JSON Report
```

---

# Validation Command

Run formatting and linting:

```powershell
ruff check scripts\run_csv_pipeline.py

black scripts\run_csv_pipeline.py
```

---

# Manual Test Command

Use an existing sample file:

```powershell
python scripts\run_csv_pipeline.py `
    examples\sample_dirty.csv `
    data\processed\sample_clean.csv `
    --report-path data\processed\sample_clean_report.json
```

Then check:

```powershell
Get-Content data\processed\sample_clean.csv

Get-Content data\processed\sample_clean_report.json
```

---

# Developer Notes

This script intentionally uses:

```python
argparse
```

because it is part of the Python standard library.

No external CLI framework is needed yet.

---

# Future Improvements

Possible future additions:

- verbose mode
- dry-run mode
- strict/tolerant mode
- selectable cleaning profile
- constraint file input
- batch folder processing
- logging
- exit codes