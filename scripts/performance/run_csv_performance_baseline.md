# run_csv_performance_baseline.py

## Purpose

Runs the CSV pipeline against a generated fixture and records baseline performance metrics.

This script is opt-in and should not run as part of normal correctness tests.

---

## Basic Usage

PowerShell:

```powershell
python scripts\performance\run_csv_performance_baseline.py
```

Default behavior:

```text
generates 1,000 rows
runs clean CSV output only
writes metrics to data/performance/csv_performance_baseline.json
```

---

## Generate and Measure 10,000 Rows

```powershell
python scripts\performance\run_csv_performance_baseline.py `
    --rows 10000 `
    --fixture-path data\performance\csv_performance_10000.csv `
    --output-path data\performance\csv_performance_10000_clean.csv `
    --metrics-path data\performance\csv_performance_10000_baseline.json
```

---

## Measure With Reports

```powershell
python scripts\performance\run_csv_performance_baseline.py `
    --rows 10000 `
    --json-report `
    --html-report
```

---

## Measure With Quarantine Exports

```powershell
python scripts\performance\run_csv_performance_baseline.py `
    --rows 10000 `
    --quarantine-exports
```

---

## Arguments

| Argument | Purpose | Default |
|---|---|---|
| `--rows` | Number of generated fixture rows | `1000` |
| `--fixture-path` | Generated fixture path | `data/performance/csv_performance_fixture.csv` |
| `--output-path` | Clean CSV output path | `data/performance/csv_performance_clean.csv` |
| `--metrics-path` | Metrics JSON output path | `data/performance/csv_performance_baseline.json` |
| `--delimiter` | Fixture delimiter | `,` |
| `--bom` | Generate UTF-8 BOM fixture | disabled |
| `--dirty-every` | Inject dirty values every N rows | `25` |
| `--json-report` | Generate JSON diagnostic report | disabled |
| `--html-report` | Generate HTML diagnostic report | disabled |
| `--quarantine-exports` | Generate quarantine/accepted split outputs | disabled |

---

## Metrics

The runner records:

```text
scenario
row_count
column_count
input_file_size_bytes
output_file_size_bytes
runtime_seconds
rows_per_second
pipeline_status
outputs
artifact_sizes
fixture
```

---

## Artifact Policy

Generated files are performance artifacts and should not be committed by default.

Typical generated files:

```text
data/performance/*.csv
data/performance/*.json
data/performance/*.html
```

---

## Design Rule

The baseline runner measures current behavior.

It should not optimize, skip diagnostics, or change pipeline correctness behavior.
