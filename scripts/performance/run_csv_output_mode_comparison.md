# run_csv_output_mode_comparison.py

## Purpose

Runs the CSV pipeline across multiple output modes and compares runtime metrics.

This script is opt-in and generates performance artifacts.

---

## Basic Usage

PowerShell:

```powershell
python scripts\performance\run_csv_output_mode_comparison.py
```

Default behavior:

```text
generates 1,000 rows per scenario
runs five output scenarios
writes comparison to data/performance/output_modes/output_mode_comparison.json
```

---

## Generate 10,000-Row Comparison

```powershell
python scripts\performance\run_csv_output_mode_comparison.py `
    --rows 10000 `
    --output-dir data\performance\output_modes_10000
```

---

## Scenarios

```text
clean_only
json_report
html_report
quarantine_exports
full_outputs
```

---

## Generated Artifacts

Example output folder:

```text
data/performance/output_modes/
```

Each scenario writes:

```text
fixture.csv
clean.csv
metrics.json
optional report/quarantine artifacts
```

The comparison root writes:

```text
output_mode_comparison.json
```

---

## Artifact Policy

Generated output mode files should not be committed by default.

---

## Design Rule

This script compares output mode costs.

It should not change pipeline correctness behavior or apply optimizations.
