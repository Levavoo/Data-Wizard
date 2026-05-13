# CSV Report Usability and Examples Plan

## Status

```text
Draft — not active until user confirmation.
```

This plan focuses on making the current CSV workflow easier to understand, run, and review from a user perspective.

It must not be started automatically.

---

## Purpose

The CSV engine now produces many diagnostics:

```text
parse diagnostics
quality report
column profiles
row profiles
row classification
type diagnostics
validation report
```

The next step is to make those outputs usable for a real user.

Goal:

```text
clean CSV pipeline
→ clear examples
→ readable diagnostic reports
→ documented user workflow
→ reusable sample configs
```

---

## Problem

The engine is becoming capable, but users still need clear guidance.

Current risks:

```text
users do not know which command to run
users do not know how to write constraints.json
users do not know how to interpret report.json
users do not know which diagnostics are warnings vs serious issues
examples are not packaged as a clear workflow
```

Expected result:

```text
a user can run a sample CSV through the pipeline
review clean CSV output
review diagnostic JSON output
understand each report section
understand what to fix next
```

---

## Architectural Layer

This plan belongs mainly to:

```text
17_Report_Export
14_Output_Serialization_Layer
Developer/User Documentation Layer
```

Main module areas:

```text
docs/
examples/
scripts/
tests/
```

Rules:

```text
Do not change core cleaning behavior unless needed.
Examples must be reproducible.
Generated outputs should not be committed unless intentionally stored as golden fixtures.
Documentation must match current CLI behavior.
```

---

# Stage A — Current Report Structure Review

## Goal

Document the current diagnostic bundle structure.

Current top-level sections:

```text
table_name
row_count
column_count
metadata
parse_diagnostics
quality_report
column_profiles
row_profiles
row_classification
type_diagnostics
validation_report
```

## Expected Files

```text
docs/user_guides/csv_diagnostic_report.md
log_protocol/06_CSV_report_usability_and_examples/001_current_report_structure_review.md
```

## Acceptance Criteria

- Each diagnostic section is explained in user-facing language.
- Examples are included for key sections.
- The difference between quality issues, type issues, suspicious rows, and validation failures is clear.

---

# Stage B — Example Input Dataset

## Goal

Create a small realistic sample CSV for user demonstrations.

Suggested file:

```text
examples/csv/customer_migration_sample.csv
```

Should include:

```text
normal rows
missing values
weird null tokens
EU/US number formats
invalid email
duplicate customer ID
unsupported country
summary/footer row
```

## Expected Files

```text
examples/csv/customer_migration_sample.csv
examples/csv/customer_migration_sample.md
log_protocol/06_CSV_report_usability_and_examples/002_example_input_dataset.md
```

## Acceptance Criteria

- Example is small and readable.
- Example triggers multiple diagnostics.
- Matching `.md` documentation explains why each row exists.

---

# Stage C — Example Constraint File

## Goal

Create a reusable example constraints JSON file.

Suggested file:

```text
examples/csv/customer_constraints.json
```

Example rules:

```text
customer_id required
customer_id unique
email regex
country allowed values
amount min_value 0
```

## Expected Files

```text
examples/csv/customer_constraints.json
examples/csv/customer_constraints.md
log_protocol/06_CSV_report_usability_and_examples/003_example_constraint_file.md
```

## Acceptance Criteria

- Constraint JSON works with current CLI.
- Documentation explains each constraint.
- Uses supported constraint config format only.

---

# Stage D — Example Run Guide

## Goal

Create a user-facing guide for running the CSV pipeline.

Suggested file:

```text
docs/user_guides/run_csv_pipeline_example.md
```

Guide should include:

```text
where to place input files
how to run without constraints
how to run with constraints
where outputs are written
how to inspect report JSON
how to interpret major diagnostic sections
```

## Expected Files

```text
docs/user_guides/run_csv_pipeline_example.md
log_protocol/06_CSV_report_usability_and_examples/004_example_run_guide.md
```

## Acceptance Criteria

- Commands are PowerShell-friendly.
- Commands match current CLI arguments.
- User can copy/paste commands.
- Output expectations are documented.

---

# Stage E — Report Interpretation Guide

## Goal

Explain what users should do after receiving diagnostics.

Suggested file:

```text
docs/user_guides/csv_report_interpretation.md
```

Guide should explain:

```text
parse diagnostics
missing values
duplicate rows
mixed-type columns
suspicious rows
validation failures
```

## Expected Files

```text
docs/user_guides/csv_report_interpretation.md
log_protocol/06_CSV_report_usability_and_examples/005_report_interpretation_guide.md
```

## Acceptance Criteria

- Each report area has an action recommendation.
- User can distinguish warnings from hard problems.
- No misleading promise of automatic correction.

---

# Stage F — Optional Pretty Summary Design

## Goal

Design a future concise report summary for CLI output.

Example future summary:

```text
CSV Pipeline Summary
Rows: 25
Columns: 8
Missing values: 4
Mixed-type columns: 1
Suspicious rows: 2
Validation failures: 5
Report: data/processed/report.json
```

## Expected Files

```text
docs/design/cli_report_summary.md
log_protocol/06_CSV_report_usability_and_examples/006_cli_report_summary_design.md
```

## Acceptance Criteria

- Summary fields are proposed.
- Implementation is deferred unless separately confirmed.
- Summary does not replace full diagnostic JSON.

---

# Stage G — Example Workflow Test

## Goal

Add a light test that verifies the example constraint file can be loaded and used with the example CSV.

Expected files:

```text
tests/test_example_csv_workflow.py
tests/test_example_csv_workflow.md
log_protocol/06_CSV_report_usability_and_examples/007_example_workflow_test.md
```

## Acceptance Criteria

- Example CSV exists.
- Example constraints JSON exists.
- Pipeline can run on example files.
- Diagnostic bundle includes expected report sections.
- Validation failures are detected.

---

## Out Of Scope

This plan does not include:

```text
HTML report generation
new validation rule types
row quarantine implementation
automatic data correction
strict/fail mode
GitHub Actions
large file performance work
Excel adapter
JSON adapter
```

---

## Recommended Implementation Order

```text
Stage A — Current Report Structure Review
Stage B — Example Input Dataset
Stage C — Example Constraint File
Stage D — Example Run Guide
Stage E — Report Interpretation Guide
Stage F — Optional Pretty Summary Design
Stage G — Example Workflow Test
```

---

## Required Protocol Folder

When active, use:

```text
log_protocol/06_CSV_report_usability_and_examples/
```

Protocol files:

```text
001_current_report_structure_review.md
002_example_input_dataset.md
003_example_constraint_file.md
004_example_run_guide.md
005_report_interpretation_guide.md
006_cli_report_summary_design.md
007_example_workflow_test.md
999_plan_completion.md
```

---

## Activation Rule

This plan is not active until the user explicitly confirms:

```text
Start 06_CSV_report_usability_and_examples
```

Until then, continue only with the currently active confirmed plan.
