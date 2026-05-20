# CSV Initial Bottleneck Review

## Purpose

This document records the initial bottleneck review for the CSV performance layer.

Plan:

```text
docs/plan_stages/16_CSV_performance_layer.md
```

---

## Current Status

Performance tooling now exists for:

```text
generating deterministic CSV fixtures
running baseline performance measurements
recording metrics JSON
collecting optional pipeline step timings
comparing output modes
```

No local benchmark results are committed in this stage.

Reason:

```text
performance metrics depend on machine, Python version, disk speed, and output mode
```

---

## How To Produce Evidence

Run baseline:

```powershell
python scripts\performance\run_csv_performance_baseline.py `
    --rows 10000 `
    --json-report `
    --html-report
```

Run output mode comparison:

```powershell
python scripts\performance\run_csv_output_mode_comparison.py `
    --rows 10000 `
    --output-dir data\performance\output_modes_10000
```

Generated metrics should be inspected locally and not committed by default.

---

## Likely Bottleneck Candidates To Confirm

These are candidates, not proven bottlenecks until measured.

### CSV Adapter Read

Potential issue:

```text
all rows are loaded into memory
CSV parsing is not streamed through later stages
```

Evidence to inspect:

```text
adapter_read_seconds
input_file_size_bytes
row_count
```

---

### Cleaning Passes

Potential issue:

```text
null cleaning and text cleaning scan table values
```

Evidence to inspect:

```text
cleaning_seconds
row_count
column_count
```

---

### Type Inference and Casting

Potential issue:

```text
type inference runs before and after casting
type casting scans values again
number/date/boolean parsing may be repeated
```

Evidence to inspect:

```text
type_inference_first_pass_seconds
type_casting_seconds
type_inference_second_pass_seconds
```

Future improvement candidate:

```text
cache parse evidence
combine compatible passes
avoid repeated parsing where safe
```

---

### Diagnostic Bundle

Potential issue:

```text
column profiles, row profiles, row classification, mixed-type diagnostics, and quarantine candidates can grow with row count
```

Evidence to inspect:

```text
diagnostic_bundle_seconds
quarantine candidate count
report sizes
```

Future improvement candidate:

```text
configurable diagnostic depth
summary-first diagnostics
sampled row previews
```

---

### HTML Report Rendering

Potential issue:

```text
HTML report is built as a full string
large diagnostic sections may increase render time and memory
```

Evidence to inspect:

```text
html_report_export_seconds
html_report_bytes
```

Future improvement candidate:

```text
limit row previews
stream HTML rendering
separate detailed machine report from compact human report
```

---

### Quarantine Row Splits

Potential issue:

```text
quarantine and accepted row exports may build additional table objects
large quarantine candidate lists can increase runtime and memory
```

Evidence to inspect:

```text
quarantine_json_export_seconds
quarantine_rows_export_seconds
accepted_rows_export_seconds
quarantine_rows_bytes
accepted_rows_bytes
```

Future improvement candidate:

```text
single-pass row split export
avoid constructing duplicate tables for large files
```

---

## Review Method

For each benchmark run, record:

```text
machine
Python version
row count
output mode
runtime seconds
rows per second
largest timing fields
artifact sizes
```

Then decide:

```text
is the bottleneck real?
is it caused by core processing or report/export mode?
can it be optimized without reducing correctness?
should it be configurable instead of removed?
```

---

## No Optimization Yet

This stage intentionally does not apply performance optimizations.

Reason:

```text
first establish measurement tooling and review method
then optimize based on evidence
```

---

## Future Optimization Candidates

Possible future stages:

```text
17_CSV_semantic_text_columns
18_CSV_malformed_quote_diagnostics
19_CSV_spreadsheet_injection_export_safety
20_CSV_locale_profiles_for_dates_booleans_numbers
21_CSV_auto_output_path_generation
22_CSV_large_file_stress_test
23_CSV_diagnostic_depth_controls
24_CSV_streaming_export_layer
25_CSV_type_inference_cache
```
