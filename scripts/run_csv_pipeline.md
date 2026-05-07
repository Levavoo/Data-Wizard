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
```

---

# Main Responsibilities

This script handles:

- reading command-line arguments
- calling the CSV pipeline
- printing the output path
- printing the quality report

It does not handle:

- CSV parsing directly
- cleaning directly
- validation directly
- exporting directly

Those responsibilities belong to the core project modules.

---

# Main Functions

## `parse_arguments()`

Reads command-line arguments.

Expected arguments:

```text
input_path
output_path
```

Example:

```powershell
python scripts\run_csv_pipeline.py data\raw\input.csv data\processed\output.csv
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

# Example Usage

From the project root:

```powershell
python scripts\run_csv_pipeline.py `
    data\raw\customers.csv `
    data\processed\customers_clean.csv
```

---

# Expected Output

Example terminal output:

```text
CSV pipeline completed.

Input file: data\raw\customers.csv
Output file: data\processed\customers_clean.csv

Quality report:
{
    "table_name": "customers",
    "row_count": 100,
    "column_count": 5,
    ...
}
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
→ Quality Report
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
    data\processed\sample_clean.csv
```

Then check:

```powershell
Get-Content data\processed\sample_clean.csv
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

- optional report output path
- JSON report export
- verbose mode
- dry-run mode
- strict/tolerant mode
- selectable cleaning profile
- batch folder processing
- logging
- exit codes