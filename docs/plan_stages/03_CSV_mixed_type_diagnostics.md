# CSV Mixed-Type Diagnostics Plan

## Status

```text
Draft — not active until user confirmation.
```

This plan focuses on detecting and reporting mixed-type columns in CSV workflows.

It must not be started automatically.

---

## Purpose

Improve visibility into columns that mostly contain one type but include invalid or incompatible values.

Goal:

```text
raw CSV values
→ type inference
→ dominant type detection
→ invalid value diagnostics
→ safer casting and validation
```

---

## Problem

Current type inference is strict.

If one value does not match the rest of the column, the whole column can fall back to `string`.

Example:

```csv
amount
100
250.75
unknown
300
```

Current risk:

```text
amount may become string
invalid value is not clearly reported
numeric intent is hidden
```

Expected future behavior:

```text
dominant type: float
invalid values: row 3 = unknown
column should be reported as mixed-type
```

---

## Architectural Layer

This plan belongs mainly to:

```text
08_Type_Layer
10_Constraint_Validation_Layer, reporting only
17_Report_Export, future export only
```

Main module areas:

```text
data_processor/inference/
data_processor/reports/
```

Rules:

```text
Inference detects and reports type evidence.
Inference must not mutate values.
Type-aware casting should remain schema-driven.
Diagnostics should be machine-readable.
Validators should not perform inference.
Adapters should not classify semantic type errors.
```

---

# Stage A — Current Mixed-Type Behavior Verification

## Goal

Add tests that document current mixed-type behavior.

Example values:

```python
["100", "250.75", "unknown", "300"]
```

Expected current behavior may be:

```text
string
```

This stage should expose the limitation before changing behavior.

## Expected Files

```text
tests/test_type_inference.py
tests/test_type_inference.md
log_protocol/03_CSV_mixed_type_diagnostics/001_current_behavior_verification.md
```

## Acceptance Criteria

- Current behavior is covered by tests.
- Limitation is documented.
- No production behavior change is required in this stage unless needed by the test structure.

---

# Stage B — Mixed-Type Diagnostic Model Design

## Goal

Define a structured model for mixed-type diagnostics.

Possible future structure:

```python
{
    "column": "amount",
    "dominant_type": "float",
    "inferred_type": "string",
    "total_values": 4,
    "valid_count": 3,
    "invalid_count": 1,
    "invalid_values": [
        {
            "row_index": 2,
            "value": "unknown",
            "expected_type": "float"
        }
    ]
}
```

## Expected Files

```text
docs/design/mixed_type_diagnostics.md
log_protocol/03_CSV_mixed_type_diagnostics/002_diagnostic_model_design.md
```

## Acceptance Criteria

- Diagnostic fields are defined.
- Row index semantics are documented.
- Dominant type concept is documented.
- No production implementation is required yet.

---

# Stage C — Type Evidence Collection

## Goal

Add type evidence collection without mutating values.

Possible file:

```text
data_processor/inference/type_diagnostics.py
```

Required matching documentation:

```text
data_processor/inference/type_diagnostics.md
```

Possible functions:

```python
analyze_column_type_evidence(values)
analyze_table_type_evidence(table)
```

## Expected Files

```text
data_processor/inference/type_diagnostics.py
data_processor/inference/type_diagnostics.md
tests/test_type_diagnostics.py
tests/test_type_diagnostics.md
log_protocol/03_CSV_mixed_type_diagnostics/003_type_evidence_collection.md
```

## Acceptance Criteria

- Evidence collection does not mutate values.
- Counts compatible values per candidate type.
- Tracks invalid values for dominant candidate type.
- Handles null values separately.
- Tests cover integer, float, boolean, date, and mixed text values.

---

# Stage D — Dominant Type Detection

## Goal

Detect likely dominant type for mixed columns.

Example:

```text
values: 100, 250.75, unknown, 300
dominant_type: float
invalid_values: unknown
```

Possible rules:

```text
ignore null values
prefer numeric dominance if integer + float are both present
require configurable threshold, default 0.8
if no dominant type reaches threshold, classify as string
```

## Expected Files

```text
data_processor/inference/type_diagnostics.py
data_processor/inference/type_diagnostics.md
tests/test_type_diagnostics.py
tests/test_type_diagnostics.md
log_protocol/03_CSV_mixed_type_diagnostics/004_dominant_type_detection.md
```

## Acceptance Criteria

- Dominant type is detected for mostly numeric columns.
- Invalid values are reported with row indexes.
- Nulls do not count as invalid values.
- Ambiguous columns remain string or no-dominant-type.

---

# Stage E — Diagnostic Bundle Integration

## Goal

Expose mixed-type diagnostics in the diagnostic bundle.

Possible section:

```python
{
    "type_diagnostics": {
        "mixed_type_columns": [...]
    }
}
```

## Expected Files

```text
data_processor/reports/diagnostic_bundle.py
data_processor/reports/diagnostic_bundle.md
tests/test_diagnostic_bundle.py
tests/test_diagnostic_bundle.md
log_protocol/03_CSV_mixed_type_diagnostics/005_diagnostic_bundle_integration.md
```

## Acceptance Criteria

- Diagnostic bundle includes type diagnostics.
- Existing bundle sections remain unchanged.
- Tests confirm mixed-type diagnostics are present.

---

# Stage F — Pipeline Integration Check

## Goal

Verify mixed-type diagnostics work through the CSV pipeline.

Target fixture:

```text
tests/fixtures/csv/mixed_type_column.csv
```

Expected files:

```text
tests/test_pipeline.py
tests/test_pipeline.md
log_protocol/03_CSV_mixed_type_diagnostics/006_pipeline_integration_check.md
```

## Acceptance Criteria

- Pipeline reports mixed-type column diagnostics.
- Cleaned table remains available.
- Invalid values are not silently hidden.
- Existing CSV export still works.

---

# Stage G — Casting Policy Decision

## Goal

Decide whether dominant type diagnostics should influence actual casting.

Options:

```text
Option 1: diagnostics only, no casting change
Option 2: cast valid values and preserve invalid values
Option 3: cast valid values and quarantine invalid rows
```

Recommended for now:

```text
Option 1: diagnostics only, no casting change
```

Reason:

```text
Mutation policy should remain conservative until quarantine and cleaning profiles exist.
```

## Expected Files

```text
docs/design/mixed_type_casting_policy.md
log_protocol/03_CSV_mixed_type_diagnostics/007_casting_policy_decision.md
```

## Acceptance Criteria

- Casting policy is documented.
- No unexpected mutation behavior is introduced.
- Future quarantine/profile relationship is described.

---

## Out Of Scope

This plan does not include:

```text
row quarantine implementation
automatic invalid value correction
cleaning profile implementation
constraint engine expansion
Excel adapter
JSON adapter
large-file sampling
probabilistic inference
machine-learning anomaly detection
```

---

## Recommended Implementation Order

```text
Stage A — Current Mixed-Type Behavior Verification
Stage B — Mixed-Type Diagnostic Model Design
Stage C — Type Evidence Collection
Stage D — Dominant Type Detection
Stage E — Diagnostic Bundle Integration
Stage F — Pipeline Integration Check
Stage G — Casting Policy Decision
```

---

## Required Protocol Folder

When active, use:

```text
log_protocol/03_CSV_mixed_type_diagnostics/
```

Protocol files:

```text
001_current_behavior_verification.md
002_diagnostic_model_design.md
003_type_evidence_collection.md
004_dominant_type_detection.md
005_diagnostic_bundle_integration.md
006_pipeline_integration_check.md
007_casting_policy_decision.md
999_plan_completion.md
```

---

## Activation Rule

This plan is not active until the user explicitly confirms:

```text
Start 03_CSV_mixed_type_diagnostics
```

Until then, continue only with the currently active confirmed plan.
