# CSV Performance Layer Guide

## Purpose

This guide explains how to use the CSV performance layer.

The performance layer is designed to measure current behavior before optimization.

It does not replace correctness tests.

---

## Main Files

Performance plan:

```text
docs/plan_stages/16_CSV_performance_layer.md
```

Performance policy:

```text
docs/performance/csv_performance_measurement_policy.md
```

Current performance surface:

```text
docs/performance/current_csv_pipeline_performance_surface.md
```

Metrics format:

```text
docs/performance/csv_performance_metrics_format.md
```

Bottleneck review:

```text
docs/performance/csv_initial_bottleneck_review.md
```

Output mode scenarios:

```text
docs/performance/csv_output_mode_performance_scenarios.md
```

---

## Fixture Generator

Script:

```text
scripts/performance/generate_csv_performance_fixture.py
```

Documentation:

```text
scripts/performance/generate_csv_performance_fixture.md
```

Generate default 1,000-row fixture:

```powershell
python scripts\performance\generate_csv_performance_fixture.py
```

Generate 10,000-row fixture:

```powershell
python scripts\performance\generate_csv_performance_fixture.py `
    --rows 10000 `
    --output-path data\performance\csv_performance_10000.csv
```

Generate semicolon-delimited fixture:

```powershell
python scripts\performance\generate_csv_performance_fixture.py `
    --rows 10000 `
    --delimiter ";" `
    --output-path data\performance\csv_performance_10000_semicolon.csv
```

---

## Baseline Runner

Script:

```text
scripts/performance/run_csv_performance_baseline.py
```

Documentation:

```text
scripts/performance/run_csv_performance_baseline.md
```

Run default baseline:

```powershell
python scripts\performance\run_csv_performance_baseline.py
```

Run 10,000-row baseline:

```powershell
python scripts\performance\run_csv_performance_baseline.py `
    --rows 10000 `
    --fixture-path data\performance\csv_performance_10000.csv `
    --output-path data\performance\csv_performance_10000_clean.csv `
    --metrics-path data\performance\csv_performance_10000_baseline.json
```

Run with JSON and HTML report generation:

```powershell
python scripts\performance\run_csv_performance_baseline.py `
    --rows 10000 `
    --json-report `
    --html-report
```

Run with quarantine exports:

```powershell
python scripts\performance\run_csv_performance_baseline.py `
    --rows 10000 `
    --quarantine-exports
```

---

## Output Mode Comparison

Script:

```text
scripts/performance/run_csv_output_mode_comparison.py
```

Documentation:

```text
scripts/performance/run_csv_output_mode_comparison.md
```

Run default comparison:

```powershell
python scripts\performance\run_csv_output_mode_comparison.py
```

Run 10,000-row comparison:

```powershell
python scripts\performance\run_csv_output_mode_comparison.py `
    --rows 10000 `
    --output-dir data\performance\output_modes_10000
```

Scenarios:

```text
clean_only
json_report
html_report
quarantine_exports
full_outputs
```

---

## Optional Pipeline Step Timings

The pipeline supports optional timing metrics:

```python
result = run_csv_pipeline(
    input_path=input_path,
    output_path=output_path,
    collect_step_timings=True,
)

performance_metrics = result["performance_metrics"]
```

Timing metrics are disabled by default.

Current timing fields include:

```text
adapter_read_seconds
cleaning_seconds
type_inference_first_pass_seconds
type_casting_seconds
type_inference_second_pass_seconds
validation_seconds
quality_report_seconds
diagnostic_bundle_seconds
pipeline_status_seconds
clean_csv_export_seconds
json_report_export_seconds
html_report_export_seconds
quarantine_json_export_seconds
quarantine_rows_export_seconds
accepted_rows_export_seconds
```

---

## Performance Smoke Test

Smoke test:

```text
tests/performance/test_csv_performance_smoke.py
```

Run:

```powershell
python -m pytest tests\performance\test_csv_performance_smoke.py
```

Purpose:

```text
verify fixture generator works
verify baseline runner writes metrics
verify metrics structure
```

It does not enforce runtime thresholds.

---

## Generated Artifact Locations

Default generated locations:

```text
data/performance/
data/generated/
```

Typical generated artifacts:

```text
*.csv
*.json
*.html
```

These files should usually not be committed.

---

## Artifact Policy

Commit:

```text
scripts
documentation
tests
small source fixtures when explicitly needed
```

Do not commit by default:

```text
generated performance CSVs
generated metrics JSON files
generated HTML reports
generated output comparisons
```

Reason:

```text
metrics are machine-dependent
large generated files bloat the repository
artifacts are reproducible from scripts
```

---

## How To Interpret Results

Compare performance results only when these are similar:

```text
same machine
same Python version
same row count
same delimiter/BOM settings
same dirty value frequency
same output mode
same branch or commit range
```

Important metrics:

```text
runtime_seconds
rows_per_second
input_file_size_bytes
output_file_size_bytes
artifact_sizes
step timings when enabled
```

---

## How To Decide Future Optimizations

Do not optimize after one isolated slow run.

Look for:

```text
consistent bottlenecks
large differences between output modes
bad scaling as row count grows
specific pipeline phases dominating total runtime
large report artifacts
large quarantine artifacts
```

Then decide whether to:

```text
optimize code
make diagnostics configurable
add semantic config options
split reports into summary/detail modes
introduce streaming export
cache repeated parse evidence
```

---

## What This Layer Does Not Do

This layer does not implement:

```text
streaming processing
parallel processing
external dataframe engine
runtime CI gates
memory-gated benchmark checks
automatic optimization
```

Those require separate future plans.

---

## Recommended Local Workflow

1. Run correctness tests:

```powershell
python -m pytest
```

2. Run performance smoke test:

```powershell
python -m pytest tests\performance\test_csv_performance_smoke.py
```

3. Run 10,000-row baseline:

```powershell
python scripts\performance\run_csv_performance_baseline.py `
    --rows 10000 `
    --json-report `
    --html-report
```

4. Run output-mode comparison:

```powershell
python scripts\performance\run_csv_output_mode_comparison.py `
    --rows 10000 `
    --output-dir data\performance\output_modes_10000
```

5. Inspect generated metrics:

```powershell
code data\performance\csv_performance_baseline.json
code data\performance\output_modes_10000\output_mode_comparison.json
```

---

## Future Improvement Candidates

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
