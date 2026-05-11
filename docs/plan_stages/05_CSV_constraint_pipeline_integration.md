# CSV Constraint Pipeline Integration Plan

## Status

```text
Draft — not active until user confirmation.
```

This plan focuses on integrating the existing constraint validation layer into the normal CSV pipeline.

It must not be started automatically.

---

## Purpose

Connect reusable validation constraints to the CSV processing workflow so users can run structured rule checks as part of an end-to-end CSV cleaning process.

Goal:

```text
CSV input
→ canonical Table
→ cleaning
→ type inference/casting
→ constraint validation
→ validation report
→ diagnostic bundle
→ exported clean CSV + report
```

---

## Problem

The project already has validation-related modules, but CSV pipeline usage still needs stronger integration.

Current risk:

```text
constraints exist as standalone logic
pipeline users may not easily pass validation rules
validation results may not be consistently included in reports
CLI may not support constraints
```

Expected future behavior:

```text
user provides constraints
pipeline validates table after cleaning/casting
validation report appears in diagnostic bundle
CLI can run constrained CSV validation
```

---

## Architectural Layer

This plan belongs mainly to:

```text
10_Constraint_Validation_Layer
11_Semantic_Layer, future only
17_Report_Export
```

Main module areas:

```text
data_processor/validators/
data_processor/core/pipeline.py
scripts/run_csv_pipeline.py
data_processor/reports/
```

Rules:

```text
Validators validate only.
Validators must not mutate table rows.
Pipeline orchestrates validation.
Constraint definitions should be data/config objects.
Reports aggregate validation results.
Exporters only serialize.
```

---

# Stage A — Current Constraint Capability Review

## Goal

Review and document current constraint support.

Expected files to inspect:

```text
data_processor/validators/constraints.py
data_processor/validators/validation_report.py
data_processor/core/pipeline.py
tests/test_constraints.py
tests/test_validation_report.py
```

## Expected Files

```text
docs/design/current_constraint_capabilities.md
log_protocol/05_CSV_constraint_pipeline_integration/001_current_capability_review.md
```

## Acceptance Criteria

- Existing constraint types are documented.
- Existing report behavior is documented.
- Missing integration points are listed.
- No production code change is required in this stage.

---

# Stage B — Pipeline Constraint Input Design

## Goal

Define how constraints should be passed into `run_csv_pipeline()`.

Possible function shape:

```python
run_csv_pipeline(
    input_path=input_path,
    output_path=output_path,
    constraints=[...],
)
```

or:

```python
run_csv_pipeline(
    input_path=input_path,
    output_path=output_path,
    constraint_config=constraint_config,
)
```

## Expected Files

```text
docs/design/pipeline_constraint_input.md
log_protocol/05_CSV_constraint_pipeline_integration/002_pipeline_constraint_input_design.md
```

## Acceptance Criteria

- Function interface is proposed.
- Backward compatibility is considered.
- Constraints remain optional.
- Existing pipeline calls should continue to work.

---

# Stage C — Constraint Configuration Format

## Goal

Define a simple machine-readable constraint configuration format.

Example draft:

```python
[
    {
        "column": "customer_id",
        "type": "required"
    },
    {
        "column": "email",
        "type": "regex",
        "pattern": "^[^@]+@[^@]+\\.[^@]+$"
    },
    {
        "column": "country",
        "type": "allowed_values",
        "values": ["Germany", "France", "Spain"]
    }
]
```

## Expected Files

```text
docs/design/constraint_config_format.md
log_protocol/05_CSV_constraint_pipeline_integration/003_constraint_config_format.md
```

## Acceptance Criteria

- Supported constraint config fields are documented.
- Required fields are defined.
- Invalid config behavior is documented.
- No CLI parsing implementation is required yet.

---

# Stage D — Pipeline Validation Integration

## Goal

Allow `run_csv_pipeline()` to accept optional constraints and include validation results in the diagnostic bundle.

Expected files:

```text
data_processor/core/pipeline.py
data_processor/core/pipeline.md
tests/test_pipeline.py
tests/test_pipeline.md
log_protocol/05_CSV_constraint_pipeline_integration/004_pipeline_validation_integration.md
```

## Acceptance Criteria

- Existing pipeline calls still work without constraints.
- Pipeline accepts optional constraints.
- Validation runs after cleaning and type-aware casting.
- Validation results are passed to `build_diagnostic_bundle()`.
- Validation report appears in returned result and diagnostic bundle.
- Validators do not mutate data.

---

# Stage E — Constraint Config Loader

## Goal

Add a small config conversion layer that converts dictionaries into constraint objects/functions.

Possible future file:

```text
data_processor/validators/constraint_config.py
data_processor/validators/constraint_config.md
```

Possible function:

```python
load_constraints_from_config(config)
```

## Expected Files

```text
data_processor/validators/constraint_config.py
data_processor/validators/constraint_config.md
tests/test_constraint_config.py
tests/test_constraint_config.md
log_protocol/05_CSV_constraint_pipeline_integration/005_constraint_config_loader.md
```

## Acceptance Criteria

- Constraint config dictionaries can be converted to executable constraints.
- Unsupported constraint types produce clear errors.
- Missing required fields produce clear errors.
- Tests cover each supported constraint type.

---

# Stage F — CLI Constraint File Support

## Goal

Allow the CSV pipeline CLI to receive a constraints file.

Possible CLI option:

```bash
python scripts/run_csv_pipeline.py input.csv output.csv --constraints constraints.json --report report.json
```

Expected files:

```text
scripts/run_csv_pipeline.py
scripts/run_csv_pipeline.md
tests/test_cli_constraints.py
tests/test_cli_constraints.md
log_protocol/05_CSV_constraint_pipeline_integration/006_cli_constraint_file_support.md
```

## Acceptance Criteria

- CLI accepts optional constraint JSON file.
- CLI still works without constraints.
- Invalid constraint file produces clear error.
- Report includes validation results.

---

# Stage G — End-to-End Constraint Pipeline Test

## Goal

Verify full CSV constraint validation behavior end to end.

Target fixture:

```text
tests/fixtures/csv/messy_customers.csv
```

Possible test:

```text
required customer_id
unique customer_id
allowed country values
regex email pattern
min/max amount
```

Expected files:

```text
tests/test_pipeline.py
tests/test_pipeline.md
log_protocol/05_CSV_constraint_pipeline_integration/007_end_to_end_constraint_pipeline_test.md
```

## Acceptance Criteria

- Pipeline validates constraints after cleaning/casting.
- Validation failures include row indexes and values.
- Diagnostic bundle includes validation report failures.
- Cleaned table remains available.
- CSV export still works.

---

# Stage H — Validation Report Export Check

## Goal

Verify exported JSON report includes validation report details.

Expected files:

```text
tests/test_json_report_exporter.py
tests/test_json_report_exporter.md
tests/test_pipeline.py
tests/test_pipeline.md
log_protocol/05_CSV_constraint_pipeline_integration/008_validation_report_export_check.md
```

## Acceptance Criteria

- JSON diagnostic report includes validation report.
- Failed constraints are machine-readable.
- Existing report sections remain unchanged.

---

# Stage I — Constraint Integration Policy

## Goal

Document what constraint validation should and should not do.

Policy:

```text
constraints report violations only
constraints do not clean values
constraints do not cast values
constraints do not quarantine rows yet
constraints do not block export by default
```

Expected files:

```text
docs/design/constraint_validation_policy.md
log_protocol/05_CSV_constraint_pipeline_integration/009_constraint_integration_policy.md
```

## Acceptance Criteria

- Validation behavior is explicitly documented.
- Export-blocking behavior is deferred.
- Quarantine relationship is documented as future work.

---

## Out Of Scope

This plan does not include:

```text
automatic row quarantine
blocking CSV export on validation failure
semantic cross-field rules
foreign key validation
SQL/database validation
Excel adapter
JSON adapter
HTML report generation
interactive validation UI
```

---

## Recommended Implementation Order

```text
Stage A — Current Constraint Capability Review
Stage B — Pipeline Constraint Input Design
Stage C — Constraint Configuration Format
Stage D — Pipeline Validation Integration
Stage E — Constraint Config Loader
Stage F — CLI Constraint File Support
Stage G — End-to-End Constraint Pipeline Test
Stage H — Validation Report Export Check
Stage I — Constraint Integration Policy
```

---

## Required Protocol Folder

When active, use:

```text
log_protocol/05_CSV_constraint_pipeline_integration/
```

Protocol files:

```text
001_current_capability_review.md
002_pipeline_constraint_input_design.md
003_constraint_config_format.md
004_pipeline_validation_integration.md
005_constraint_config_loader.md
006_cli_constraint_file_support.md
007_end_to_end_constraint_pipeline_test.md
008_validation_report_export_check.md
009_constraint_integration_policy.md
999_plan_completion.md
```

---

## Activation Rule

This plan is not active until the user explicitly confirms:

```text
Start 05_CSV_constraint_pipeline_integration
```

Until then, continue only with the currently active confirmed plan.
