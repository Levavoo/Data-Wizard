# Current Project State and Future Plan

## Purpose

This document summarizes the current state of the Data Wizard project after the CSV core stabilization work.

It explains:

```text
what the project can do now
how the codebase is structured
how the CSV pipeline flows end-to-end
what is not supported yet
what should be implemented next
```

---

## Current Project Focus

Current project scope:

```text
Data cleaning and diagnostics system
Primary supported input format: CSV
Primary interface: CLI + config files
Primary outputs: cleaned CSV, JSON report, HTML report, quarantine outputs, performance metrics
```

The project is currently strongest as a backend/CLI data-cleaning engine.

It is not yet a GUI application and does not yet support JSON or Excel input adapters.

---

# Current Capabilities

## 1. CSV Input Processing

The project can currently process CSV files with support for:

```text
standard comma CSV
semicolon CSV
tab/pipe delimiter detection candidates
UTF-8 files
UTF-8 BOM files
cp1252 fallback
latin-1 fallback
metadata rows before header
duplicate headers
empty headers
extra fields
missing fields
quoted values
escaped quotes
multiline quoted fields
```

Important files:

```text
data_processor/adapters/csv_adapter.py
data_processor/adapters/encoding_detection.py
data_processor/adapters/delimiter_detection.py
data_processor/adapters/parse_diagnostics.py
```

---

## 2. Parse Diagnostics

The parser records structural diagnostics such as:

```text
selected encoding
selected delimiter
encoding/delimiter detection details
header row index
preamble row count
empty headers
duplicate headers
rows with extra fields
rows with missing fields
warnings
```

These diagnostics are included in the diagnostic bundle and exported reports.

---

## 3. Cleaning

The pipeline currently supports cleaning for:

```text
null-like values
whitespace-only values
text trimming
internal whitespace normalization
number normalization
basic boolean handling
basic date handling
```

Important files:

```text
data_processor/cleaners/nulls.py
data_processor/cleaners/text.py
data_processor/cleaners/numbers.py
data_processor/cleaners/booleans.py
data_processor/cleaners/dates.py
data_processor/cleaners/type_caster.py
```

---

## 4. Type Inference and Type Diagnostics

The project can infer and diagnose column types.

Current capabilities include:

```text
column type inference
schema metadata inference
mixed-type diagnostics
dominant type detection
invalid/outlier value reporting
```

Important files:

```text
data_processor/inference/type_inference.py
data_processor/inference/type_diagnostics.py
data_processor/inference/schema_inference.py
```

---

## 5. Validation Constraints

The project supports constraint validation through code and config files.

Current constraint examples:

```text
required
unique
regex
allowed_values
min_value
max_value
```

Important files:

```text
data_processor/validators/constraints.py
data_processor/validators/constraint_config.py
```

Current example:

```text
tests/fixtures/csv/real_world_messy_customers_constraints.json
```

---

## 6. Quality Reports and Diagnostic Bundle

The project creates structured reports containing:

```text
parse diagnostics
quality report
column profiles
row profiles
row classification
type diagnostics
validation report
quarantine candidates
pipeline status
```

Important files:

```text
data_processor/reports/diagnostic_bundle.py
data_processor/reports/pipeline_status.py
data_processor/reports/quarantine_candidates.py
data_processor/reports/html_report.py
```

---

## 7. Row Classification

Rows can be classified as suspicious when they look structurally or semantically problematic.

Examples:

```text
summary/footer rows
rows with many missing values
rows with structural anomalies
rows that look unlike normal data records
```

Important files:

```text
data_processor/analysis/row_classification.py
```

---

## 8. Quarantine Outputs

The project can produce quarantine-related outputs:

```text
quarantine candidates JSON
quarantine rows CSV
accepted rows CSV
```

Important files:

```text
data_processor/exporters/quarantine_json_exporter.py
data_processor/reports/quarantine_row_selection.py
```

CLI options:

```text
--quarantine-candidates-path
--quarantine-rows-path
--accepted-rows-path
```

---

## 9. Report Export

The project can export:

```text
cleaned CSV
JSON diagnostic report
HTML diagnostic report
```

Important files:

```text
data_processor/exporters/csv_exporter.py
data_processor/exporters/json_report_exporter.py
data_processor/exporters/html_report_exporter.py
```

CLI options:

```text
--report-path
--html-report-path
```

---

## 10. CLI Workflow

Main user entry point:

```text
scripts/run_csv_pipeline.py
```

Current CLI supports:

```text
input path
output path
config file
profile
constraints file
strict mode
JSON report path
HTML report path
quarantine exports
encoding override
delimiter override
disable auto CSV detection
```

---

## 11. Config File Pipeline

The project supports JSON config files for pipeline execution.

Config file capabilities:

```text
input_path
output_path
profile
constraints_path
report_path
html_report_path
quarantine_candidates_path
quarantine_rows_path
accepted_rows_path
strict_mode
encoding
delimiter
auto_detect_csv
```

Important files:

```text
data_processor/config/pipeline_config.py
data_processor/config/pipeline_config_resolver.py
```

---

## 12. Cleaning Profiles

The project supports configurable cleaning profiles.

Purpose:

```text
change cleaning behavior without changing code
allow safer future user workflows
```

Important files:

```text
data_processor/config/cleaning_profiles.py
data_processor/config/profile_resolver.py
```

---

## 13. Strict Mode and Exit Codes

The project supports strict mode for CLI workflows.

Purpose:

```text
turn quality/validation failures into process-level failure signals
make CI/data pipelines aware of dirty data
```

CLI option:

```text
--strict
```

---

## 14. Real-World Dirty CSV Test Suite

The project has a heavy dirty CSV fixture and tests that check realistic messy data behavior.

Important files:

```text
tests/fixtures/csv/real_world_messy_customers_heavy.csv
tests/fixtures/csv/real_world_messy_customers_constraints.json
docs/testing/real_world_messy_customers_expected_report.md
docs/testing/real_world_messy_customers_observed_weaknesses.md
docs/testing/csv_real_world_test_suite.md
```

Tests:

```text
tests/test_real_world_messy_csv_observation.py
tests/test_real_world_parser_diagnostics.py
tests/test_real_world_cleaning_preservation.py
tests/test_real_world_quarantine_and_diagnostics.py
```

---

## 15. Performance Layer

The project has performance measurement tooling.

Capabilities:

```text
generated performance CSV fixtures
baseline runtime measurement
metrics JSON output
output mode comparison
optional pipeline step timings
performance smoke tests
```

Important files:

```text
scripts/performance/generate_csv_performance_fixture.py
scripts/performance/run_csv_performance_baseline.py
scripts/performance/run_csv_output_mode_comparison.py
data_processor/reports/performance_metrics.py
docs/performance/csv_performance_layer_guide.md
```

---

# Current Codebase Structure

## High-Level Structure

```text
data_processor/
  adapters/
  analysis/
  cleaners/
  config/
  core/
  exporters/
  inference/
  reports/
  validators/

docs/
  design/
  performance/
  plan_stages/
  release/
  testing/
  user_guides/

examples/
  csv/

scripts/
  performance/
  run_csv_pipeline.py

tests/
  fixtures/
  performance/
  test_*.py

log_protocol/
```

---

## Core Model Layer

Purpose:

```text
store generic table/schema/row/column structures independent of input format
```

Important files:

```text
data_processor/core/table.py
data_processor/core/schema.py
data_processor/core/column.py
data_processor/core/row.py
data_processor/core/pipeline.py
```

---

## Adapter Layer

Purpose:

```text
read source files and convert them into the internal Table model
```

Current adapter:

```text
CSV adapter
```

Future adapters:

```text
JSON adapter
Excel adapter
```

Adapter rule:

```text
adapters should parse and attach source diagnostics, but should not clean, validate, or generate reports
```

---

## Cleaner Layer

Purpose:

```text
normalize values after parsing
```

Examples:

```text
nulls
text
numbers
dates
booleans
type casting
```

---

## Inference Layer

Purpose:

```text
infer column types and schema metadata
report type inconsistencies
```

---

## Validation Layer

Purpose:

```text
apply user-defined or config-defined constraints
produce validation results
```

---

## Report Layer

Purpose:

```text
build quality reports, diagnostic bundles, pipeline status, quarantine candidates, HTML report content, and performance metrics
```

---

## Exporter Layer

Purpose:

```text
write output artifacts
```

Current exporters:

```text
CSV exporter
JSON report exporter
HTML report exporter
quarantine JSON exporter
```

---

## CLI and Script Layer

Purpose:

```text
user-facing execution through command line
performance tooling
fixture generation
```

---

# Current End-To-End CSV Flow

## Standard Flow

```text
User runs CLI or calls run_csv_pipeline()
→ CSV adapter validates file
→ encoding/delimiter are detected or overridden
→ CSV rows are parsed
→ header row is detected
→ preamble metadata is preserved
→ headers are normalized
→ duplicate headers are made unique
→ parse diagnostics are attached
→ Table and Schema are created
→ null cleaning runs
→ text cleaning runs
→ first type inference runs
→ type casting runs
→ second type inference/schema metadata runs
→ constraints are validated
→ quality report is generated
→ diagnostic bundle is built
→ pipeline status is built
→ clean CSV is exported
→ optional JSON report is exported
→ optional HTML report is exported
→ optional quarantine outputs are exported
→ optional performance metrics are returned
```

---

## CLI Example

```powershell
python scripts\run_csv_pipeline.py `
    tests\fixtures\csv\real_world_messy_customers_heavy.csv `
    data\processed\real_world_messy_customers_clean.csv `
    --constraints-path tests\fixtures\csv\real_world_messy_customers_constraints.json `
    --report-path data\processed\real_world_messy_customers_report.json `
    --html-report-path data\processed\real_world_messy_customers_report.html `
    --quarantine-candidates-path data\processed\real_world_messy_customers_quarantine_candidates.json `
    --quarantine-rows-path data\processed\real_world_messy_customers_quarantine_rows.csv `
    --accepted-rows-path data\processed\real_world_messy_customers_accepted_rows.csv
```

---

# Current Output Types

## Main Outputs

```text
clean CSV
JSON diagnostic report
HTML diagnostic report
quarantine candidates JSON
quarantine rows CSV
accepted rows CSV
performance metrics JSON
```

---

## Generated Artifact Policy

Generated outputs usually belong under:

```text
data/processed/
data/performance/
```

They should not be committed by default.

Source fixtures, tests, config examples, and documentation should be committed.

---

# What The Project Cannot Do Yet

## Unsupported Input Formats

Not yet supported:

```text
JSON input
Excel input
Parquet input
database input
API input
```

---

## Unsupported Interface Layer

Not yet supported:

```text
GUI
local web interface
drag-and-drop upload
interactive data review
interactive quarantine approval
```

---

## Known CSV Limitations

Current known limitations:

```text
not a full malformed CSV repair engine
unbalanced quote source locations may not be precise
multiline text newlines are currently collapsed by text cleaning
leading-zero semantic preservation is not guaranteed for all ID/postal-like columns
currency/percent/text-number normalization is limited
Excel serial dates are not fully supported
locale-specific boolean tokens such as ja/nein may be unsupported
spreadsheet injection export hardening is not implemented
HTML-like text is preserved, not sanitized as data
extra fields are diagnosed but not preserved as normal data
summary/footer rows are flagged but not automatically removed
pipeline is not streaming/chunked yet
diagnostics can grow large on big files
```

Detailed limitation document:

```text
docs/release/csv_core_known_limitations.md
```

---

# Current Readiness Level

## Backend / CLI Readiness

Current readiness:

```text
strong for CSV backend and CLI workflows
ready for local verification and merge/release checkpoint
```

Required before merge/release:

```powershell
python -m pytest
python -m pytest tests/test_real_world_messy_csv_observation.py
python -m pytest tests/test_real_world_parser_diagnostics.py
python -m pytest tests/test_real_world_cleaning_preservation.py
python -m pytest tests/test_real_world_quarantine_and_diagnostics.py
python -m pytest tests/performance/test_csv_performance_smoke.py
python -m pytest tests/test_pipeline_performance_metrics.py
```

---

## Adapter Expansion Readiness

The project is close to ready for additional adapters, but the CSV core should be merged/released first.

Recommended next adapter order:

```text
JSON adapter first
Excel adapter second
```

Reason:

```text
JSON is structurally simpler than Excel
JSON will test whether the internal Table model generalizes beyond CSV
Excel has more complex concerns: sheets, formulas, date serials, merged cells, hidden rows, formatting
```

---

## GUI Readiness

A GUI should come after adapter expansion or after at least one more backend stabilization pass.

Reason:

```text
GUI should wrap stable CLI/config/report behavior
building GUI too early risks hiding backend limitations behind interface complexity
```

Recommended first GUI form:

```text
local web interface
file upload/select
profile/config selection
run pipeline
view HTML report
download clean/quarantine/accepted outputs
```

---

# Recommended Future Implementation Plan

## Phase 1 — CSV Core Release Checkpoint

Goal:

```text
make current CSV work merge/release ready
```

Actions:

```text
run full tests
fix failures
run real-world suite
run performance smoke tests
verify CLI/config/report commands
check generated artifacts are not committed
create PR/merge codex into master
```

Relevant docs:

```text
docs/release/csv_core_verification_checklist.md
docs/release/csv_core_merge_readiness_report.md
```

---

## Phase 2 — JSON Adapter

Suggested stage:

```text
18_JSON_adapter
```

Recommended first scope:

```text
list of flat objects
single JSON file input
schema from object keys
missing keys become null
extra keys become columns
basic nested object policy documented before implementation
parse diagnostics for root shape and record count
```

Avoid initially:

```text
deep arbitrary flattening
multiple incompatible root shapes
JSON streaming parser
business-specific transformations
```

Expected files:

```text
data_processor/adapters/json_adapter.py
data_processor/adapters/json_adapter.md
tests/test_json_adapter.py
tests/test_json_adapter.md
docs/plan_stages/18_JSON_adapter.md
```

---

## Phase 3 — Excel Adapter

Suggested stage:

```text
19_Excel_adapter
```

Recommended first scope:

```text
.xlsx files only
single sheet or selected sheet
first detected/explicit header row
cell values only
no formula execution
basic date serial handling documented
parse diagnostics for sheet name, row count, header row, empty rows
```

Avoid initially:

```text
merged-cell repair
multi-sheet merge
formatting-based inference
formula execution
hidden row/column policy without design
```

Expected files:

```text
data_processor/adapters/excel_adapter.py
data_processor/adapters/excel_adapter.md
tests/test_excel_adapter.py
tests/test_excel_adapter.md
docs/plan_stages/19_Excel_adapter.md
```

---

## Phase 4 — CSV Safety Improvements

Possible stages:

```text
CSV_semantic_text_columns
CSV_malformed_quote_diagnostics
CSV_spreadsheet_injection_export_safety
CSV_locale_profiles_for_dates_booleans_numbers
CSV_diagnostic_depth_controls
CSV_streaming_export_layer
CSV_type_inference_cache
```

Recommended priority:

```text
1. semantic text columns
2. spreadsheet injection export safety
3. locale profiles
4. malformed quote diagnostics
5. diagnostic depth controls
6. streaming/export performance improvements
```

---

## Phase 5 — GUI / Local Web Interface

Suggested stage:

```text
20_GUI_or_local_web_interface
```

Recommended first scope:

```text
local-only web app
upload/select CSV
choose profile
optional config file
run pipeline
show HTML report
download clean CSV
download quarantine/accepted outputs
```

Technology decision should be documented before implementation.

Possible backend-first approach:

```text
FastAPI backend
simple HTML frontend
or Streamlit-style internal tool if dependency policy allows
```

---

# Recommended Immediate Next Step

Before creating new adapter plans, run local verification:

```powershell
git checkout codex
git pull Levavoo codex
python -m pytest
python -m pytest tests/performance/test_csv_performance_smoke.py
python -m pytest tests/test_pipeline_performance_metrics.py
```

If tests pass:

```text
create PR / merge CSV core checkpoint
then start 18_JSON_adapter
```

If tests fail:

```text
fix failures first
update known limitations only if failure reflects expected current limitation
rerun tests
```

---

## Summary

Current project state:

```text
CSV backend is feature-rich and close to release checkpoint
CLI/config/report/quarantine workflows are established
real-world messy CSV diagnostics exist
performance measurement exists
project is not yet multi-format or GUI-based
```

Recommended direction:

```text
1. verify and merge CSV core
2. add JSON adapter
3. add Excel adapter
4. add targeted CSV safety improvements
5. add GUI/local web interface
```
