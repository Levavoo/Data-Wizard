# CSV Quarantine Candidates Plan

## Status

```text
Draft — not active until user confirmation.
```

This plan focuses on identifying rows that should be reviewed as quarantine candidates.

It must not be started automatically.

---

## Purpose

The CSV pipeline already reports multiple issue sources:

```text
parse diagnostics
row classification
type diagnostics
validation report
quality report
```

This plan combines those signals into a structured quarantine-candidate report.

Goal:

```text
CSV diagnostics
→ quarantine candidate detection
→ row-level candidate reasons
→ diagnostic bundle section
→ future quarantine export support
```

---

## Important Policy

Initial policy:

```text
quarantine candidates only
```

Meaning:

```text
rows are flagged for review
rows are not removed
rows are not excluded from CSV export
rows are not written to a separate quarantine file yet
```

Reason:

```text
automatic quarantine or removal can cause silent data loss
```

---

## Problem

The pipeline currently reports issues separately.

Example:

```text
row_classification reports footer rows
validation_report reports invalid emails
type_diagnostics reports incompatible numeric values
quality_report reports missing values
```

Current risk:

```text
users must manually connect row-level issues across report sections
problematic rows are hard to review as a single list
future quarantine export has no shared candidate model
```

Expected future behavior:

```text
one report section lists rows that should be reviewed
candidate reasons are grouped per row
candidate severity is visible
source diagnostic area is preserved
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
data_processor/reports/
data_processor/validators/
data_processor/analysis/
docs/
tests/
```

Rules:

```text
Quarantine candidate detection must not mutate rows.
Quarantine candidates must not remove rows.
Diagnostic source should be preserved.
Export behavior should remain unchanged.
Candidate export is future work unless separately confirmed.
```

---

# Stage A — Current Diagnostic Sources Review

## Goal

Document which existing diagnostics can produce quarantine candidate signals.

Candidate sources:

```text
row_classification.suspicious_rows
validation_report.failed_results
type_diagnostics.mixed_type_columns.invalid_values
quality_report missing values, future optional
parse_diagnostics malformed rows, future optional
```

## Expected Files

```text
docs/design/quarantine_candidate_sources.md
log_protocol/08_CSV_quarantine_candidates/001_candidate_source_review.md
```

## Acceptance Criteria

- Candidate signal sources are documented.
- Initial included sources are chosen.
- Deferred sources are documented.
- No production code change is required in this stage.

---

# Stage B — Quarantine Candidate Model Design

## Goal

Define a structured candidate model.

Possible shape:

```python
{
    "row_index": 2,
    "severity": "error",
    "reason_count": 3,
    "reasons": [
        {
            "source": "validation_report",
            "code": "regex_pattern_failed",
            "column": "email",
            "message": "Value does not match pattern.",
            "value": "invalid-email"
        },
        {
            "source": "row_classification",
            "code": "summary_row",
            "message": "First non-empty value starts with a summary marker."
        }
    ]
}
```

## Expected Files

```text
docs/design/quarantine_candidate_model.md
log_protocol/08_CSV_quarantine_candidates/002_candidate_model_design.md
```

## Acceptance Criteria

- Candidate fields are documented.
- Severity levels are documented.
- Source diagnostic fields are documented.
- Row index semantics are documented.

---

# Stage C — Quarantine Candidate Builder

## Goal

Add a non-mutating report module that builds quarantine candidates from existing diagnostics.

Possible file:

```text
data_processor/reports/quarantine_candidates.py
```

Matching documentation:

```text
data_processor/reports/quarantine_candidates.md
```

Possible functions:

```python
build_quarantine_candidates(
    table,
    row_classification,
    type_diagnostics,
    validation_report,
)
```

## Expected Files

```text
data_processor/reports/quarantine_candidates.py
data_processor/reports/quarantine_candidates.md
tests/test_quarantine_candidates.py
tests/test_quarantine_candidates.md
log_protocol/08_CSV_quarantine_candidates/003_candidate_builder.md
```

## Acceptance Criteria

- Builds candidates without mutating table rows.
- Groups reasons by row index.
- Preserves diagnostic source names.
- Supports validation failures.
- Supports suspicious row classifications.
- Supports mixed-type invalid values.

---

# Stage D — Severity Policy

## Goal

Define conservative severity levels for quarantine candidates.

Suggested levels:

```text
info
warning
error
```

Initial mapping:

```text
validation failure → error
mixed-type invalid value → warning
summary/footer/comment/garbage row → warning
empty row → warning
parse malformed row → future error
```

## Expected Files

```text
docs/design/quarantine_candidate_severity_policy.md
log_protocol/08_CSV_quarantine_candidates/004_severity_policy.md
```

## Acceptance Criteria

- Severity policy is documented.
- Severity is deterministic.
- No candidate blocks export by default.

---

# Stage E — Diagnostic Bundle Integration

## Goal

Expose quarantine candidates in the diagnostic bundle.

Possible section:

```python
{
    "quarantine_candidates": {
        "candidate_count": 3,
        "candidates": [...],
        "summary": {
            "error": 1,
            "warning": 2,
            "info": 0
        }
    }
}
```

## Expected Files

```text
data_processor/reports/diagnostic_bundle.py
data_processor/reports/diagnostic_bundle.md
tests/test_diagnostic_bundle.py
tests/test_diagnostic_bundle.md
log_protocol/08_CSV_quarantine_candidates/005_diagnostic_bundle_integration.md
```

## Acceptance Criteria

- Diagnostic bundle includes `quarantine_candidates`.
- Existing report sections remain unchanged.
- Tests verify candidate summary and candidate reasons.

---

# Stage F — Pipeline Integration Check

## Goal

Verify quarantine candidates work through the normal CSV pipeline.

Expected files:

```text
tests/test_pipeline.py
tests/test_pipeline.md
log_protocol/08_CSV_quarantine_candidates/006_pipeline_integration_check.md
```

## Acceptance Criteria

- Pipeline diagnostic bundle includes quarantine candidates.
- Rows remain in the cleaned table.
- CSV export still includes all rows.
- Validation and suspicious-row issues produce candidates.

---

# Stage G — Example Workflow Update

## Goal

Update the existing example workflow so users can see quarantine candidates in the report.

Expected files:

```text
docs/user_guides/csv_diagnostic_report.md
docs/user_guides/csv_report_interpretation.md
docs/user_guides/run_csv_pipeline_example.md
tests/test_example_csv_workflow.py
tests/test_example_csv_workflow.md
log_protocol/08_CSV_quarantine_candidates/007_example_workflow_update.md
```

## Acceptance Criteria

- User guides mention quarantine candidates.
- Example workflow test confirms the section exists.
- Documentation clearly says candidates are not removed automatically.

---

# Stage H — Quarantine Export Policy Design Only

## Goal

Document future quarantine export behavior without implementing it yet.

Suggested future outputs:

```text
cleaned CSV with all rows
quarantine_candidates.json
quarantine_rows.csv
```

Expected files:

```text
docs/design/quarantine_export_policy.md
log_protocol/08_CSV_quarantine_candidates/008_quarantine_export_policy_design.md
```

## Acceptance Criteria

- Future quarantine export behavior is documented.
- Current plan remains candidate/report-only.
- No row removal or separate quarantine export is implemented.

---

## Out Of Scope

This plan does not include:

```text
automatic row removal
separate quarantine CSV export
blocking export on candidates
strict/fail mode
HTML reports
new validation constraint types
semantic cross-field rules
manual review UI
```

---

## Recommended Implementation Order

```text
Stage A — Current Diagnostic Sources Review
Stage B — Quarantine Candidate Model Design
Stage C — Quarantine Candidate Builder
Stage D — Severity Policy
Stage E — Diagnostic Bundle Integration
Stage F — Pipeline Integration Check
Stage G — Example Workflow Update
Stage H — Quarantine Export Policy Design Only
```

---

## Required Protocol Folder

When active, use:

```text
log_protocol/08_CSV_quarantine_candidates/
```

Protocol files:

```text
001_candidate_source_review.md
002_candidate_model_design.md
003_candidate_builder.md
004_severity_policy.md
005_diagnostic_bundle_integration.md
006_pipeline_integration_check.md
007_example_workflow_update.md
008_quarantine_export_policy_design.md
999_plan_completion.md
```

---

## Activation Rule

This plan is not active until the user explicitly confirms:

```text
Start 08_CSV_quarantine_candidates
```

Until then, continue only with the currently active confirmed plan.
