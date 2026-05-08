# Refactored Development Stages — CSV First

## Principle

Do not add Excel or JSON yet.

First make CSV excellent.

Architecture goal:

```text
CSV
→ Table
→ Clean
→ Infer
→ Cast
→ Profile
→ Validate
→ Report
→ Export
```

Once this is stable, new formats become easier:

```text
Excel
→ Table
→ same engine

JSON
→ Table
→ same engine
```

---

# Stage 14 — CSV Pipeline Diagnostic Report Integration

Goal:

```text
CSV pipeline
→ cleaned CSV
→ diagnostic JSON report
```

Work:

```text
connect diagnostic_bundle.py
connect json_report_exporter.py
pipeline returns diagnostic_bundle
CLI can save report file
```

Files:

```text
data_processor/core/pipeline.py
data_processor/core/pipeline.md
scripts/run_csv_pipeline.py
scripts/run_csv_pipeline.md
tests/test_pipeline.py
tests/test_pipeline.md
```

---

# Stage 15 — CSV Manual End-to-End Test Pack

Goal:

Create realistic local CSV test files.

Work:

```text
simple clean CSV
messy but valid CSV
CSV with missing values
CSV with duplicate rows
CSV with quoted commas
CSV with semicolon delimiter
CSV with bad-but-detectable rows later
```

Files:

```text
examples/csv/simple_customers.csv
examples/csv/messy_customers.csv
examples/csv/quoted_values.csv
examples/csv/semicolon_customers.csv
examples/csv/duplicates_missing.csv
examples/csv/README.md
```

Purpose:

```text
manual testing
future regression checks
demo data
```

---

# Stage 16 — CSV Adapter Robustness

Goal:

Make CSV parsing safer before supporting other formats.

Work:

```text
duplicate header handling
empty header handling
extra field detection
missing field detection
row length diagnostics
strict/tolerant mode
CSV parsing metadata
```

Files:

```text
data_processor/adapters/csv_adapter.py
data_processor/adapters/csv_adapter.md
tests/test_csv_adapter.py
tests/test_csv_adapter.md
```

---

# Stage 17 — CSV Parsing Diagnostics

Goal:

Report parse-level issues instead of silently failing.

Work:

```text
parse warnings
malformed row counts
extra field counts
missing field counts
detected delimiter
detected encoding
source file metadata
```

Possible file:

```text
data_processor/adapters/parse_diagnostics.py
data_processor/adapters/parse_diagnostics.md
tests/test_parse_diagnostics.py
tests/test_parse_diagnostics.md
```

---

# Stage 18 — CSV Constraint Integration

Goal:

Apply validation constraints inside CSV pipeline.

Work:

```text
pipeline accepts optional constraints
runs validate_table_constraints()
includes validation_report in diagnostic bundle
```

Files:

```text
data_processor/core/pipeline.py
data_processor/core/pipeline.md
tests/test_pipeline.py
tests/test_pipeline.md
```

---

# Stage 19 — CSV Report Output Polish

Goal:

Make report output useful for real use.

Work:

```text
include source file path
include output file path
include generated timestamp
include pipeline version
include detected encoding/delimiter
include row/column counts
include quality report
include validation report
include column profiles
include row profiles
```

Files:

```text
data_processor/reports/diagnostic_bundle.py
data_processor/reports/diagnostic_bundle.md
data_processor/exporters/json_report_exporter.py
data_processor/exporters/json_report_exporter.md
```

---

# Stage 20 — CSV CLI Polish

Goal:

Make the tool comfortable from PowerShell.

Work:

```text
--report-path
--strict
--tolerant
--show-preview
--print-report
clear error messages
exit codes
```

Example:

```powershell
python scripts\run_csv_pipeline.py `
    examples\csv\messy_customers.csv `
    data\processed\messy_customers_clean.csv `
    --report-path data\processed\messy_customers_report.json `
    --tolerant
```

Files:

```text
scripts/run_csv_pipeline.py
scripts/run_csv_pipeline.md
```

---

# Stage 21 — CSV Output Polish

Goal:

Improve cleaned CSV writing.

Work:

```text
configurable delimiter
configurable encoding
stable column ordering
optional selected columns
optional report sidecar
safe overwrite behavior
```

Files:

```text
data_processor/exporters/csv_exporter.py
data_processor/exporters/csv_exporter.md
tests/test_csv_exporter.py
tests/test_csv_exporter.md
```

---

# Stage 22 — CSV Transformation Foundation

Goal:

Add useful transformations after cleaning.

Work:

```text
rename columns
select columns
drop columns
filter rows
sort rows
```

Files:

```text
data_processor/transformers/columns.py
data_processor/transformers/columns.md
data_processor/transformers/rows.py
data_processor/transformers/rows.md
tests/test_transformers_columns.py
tests/test_transformers_rows.py
```

---

# Stage 23 — CSV Cleaning Profiles

Goal:

Make repeatable cleaning configurations.

Work:

```text
profile object
enabled cleaning steps
constraints
output options
report options
```

Example profiles:

```text
general_csv
crm_migration
financial_import
```

Files:

```text
data_processor/config/profiles.py
data_processor/config/profiles.md
tests/test_profiles.py
tests/test_profiles.md
```

---

# Stage 24 — CSV Batch Processing

Goal:

Process folders of CSV files.

Work:

```text
input folder
output folder
process all .csv files
one cleaned output per file
one report per file
batch summary report
```

Possible files:

```text
data_processor/core/batch_pipeline.py
data_processor/core/batch_pipeline.md
scripts/run_csv_batch.py
scripts/run_csv_batch.md
```

---

# Stage 25 — CSV Acceptance Test

Goal:

Verify the whole CSV system as one complete product slice.

Acceptance workflow:

```text
run CLI on example CSV files
check cleaned outputs
check JSON reports
check test suite
check git status
```

Commands:

```powershell
ruff check .
black .
pytest

python scripts\run_csv_pipeline.py `
    examples\csv\messy_customers.csv `
    data\processed\messy_customers_clean.csv `
    --report-path data\processed\messy_customers_report.json
```

Definition of done:

```text
all tests pass
manual CSV files process correctly
reports are generated
bad rows are reported clearly
cleaned output is predictable
no sensitive data committed
```

---

# Only After CSV Is Stable

Then move to:

```text
Stage 26 — Excel Adapter
Stage 27 — JSON Adapter
Stage 28 — Excel/JSON exporter support
Stage 29 — Multi-format pipeline selection
```

Reason:

At that point Excel/JSON only need to implement:

```text
Excel → Table
JSON → Table
```

and reuse:

```text
cleaning
type inference
casting
profiling
validation
reporting
export logic
```

---

# Recommended Immediate Next Stage

Start with:

```text
Stage 14 — CSV Pipeline Diagnostic Report Integration
```

because the modules already exist:

```text
diagnostic_bundle.py
json_report_exporter.py
```

They just need to be connected to the real CSV pipeline and CLI.