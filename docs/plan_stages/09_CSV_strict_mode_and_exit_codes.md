# CSV Strict Mode and Exit Codes Plan

## Status

```text
Draft — not active until user confirmation.
```

This plan focuses on adding configurable strict-mode behavior and predictable CLI exit codes.

It must not be started automatically.

---

## Purpose

The CSV pipeline currently reports issues but does not block export by default.

This is safe for diagnostics, but automated workflows need a way to fail when serious issues exist.

Goal:

```text
CSV diagnostics
→ configurable strict policy
→ predictable pipeline status
→ CLI exit codes
→ automation-friendly behavior
```

---

## Current Default Policy

Current behavior should remain the default:

```text
report-only
export still runs
exit code 0 if execution itself succeeds
```

Strict mode should be opt-in.

---

## Problem

The project now reports:

```text
parse diagnostics
validation failures
mixed-type diagnostics
suspicious rows
quarantine candidates
```

But the CLI currently has no formal machine-readable result status.

Current risks:

```text
CI/CD cannot fail on serious data problems
scripts cannot distinguish processing failure from validation failure
users cannot choose warn-only vs strict mode
exit codes are not documented
```

Expected future behavior:

```text
normal mode → report issues but exit successfully
strict mode → fail when configured serious issues are present
CLI exit code communicates result class
```

---

## Architectural Layer

This plan belongs mainly to:

```text
Pipeline Orchestration Layer
CLI Layer
Diagnostic Policy Layer
```

Main module areas:

```text
data_processor/core/
data_processor/reports/
scripts/
docs/
tests/
```

Rules:

```text
Strict mode must be explicit.
Default behavior must remain backward-compatible.
Exit codes belong to CLI behavior.
Pipeline should return structured status data.
Strict mode should not silently remove rows.
Strict mode should not mutate data.
```

---

# Stage A — Current CLI and Pipeline Behavior Review

## Goal

Document current CLI and pipeline behavior.

Expected files to inspect:

```text
data_processor/core/pipeline.py
scripts/run_csv_pipeline.py
data_processor/reports/diagnostic_bundle.py
```

## Expected Files

```text
docs/design/current_pipeline_status_behavior.md
log_protocol/09_CSV_strict_mode_and_exit_codes/001_current_behavior_review.md
```

## Acceptance Criteria

- Current report-only behavior is documented.
- Current CLI success behavior is documented.
- Missing status/exit-code behavior is documented.
- No production code change is required in this stage.

---

# Stage B — Pipeline Status Model Design

## Goal

Define a structured status model returned by the pipeline.

Possible shape:

```python
{
    "status": "success",
    "has_errors": False,
    "has_warnings": True,
    "error_count": 0,
    "warning_count": 3,
    "strict_mode": False,
    "strict_mode_failed": False,
    "reasons": [...]
}
```

Suggested statuses:

```text
success
completed_with_warnings
failed_policy
failed_execution
```

## Expected Files

```text
docs/design/pipeline_status_model.md
log_protocol/09_CSV_strict_mode_and_exit_codes/002_pipeline_status_model.md
```

## Acceptance Criteria

- Status fields are documented.
- Status names are documented.
- Difference between policy failure and execution failure is documented.
- Status model does not remove rows.

---

# Stage C — Strict Mode Policy Design

## Goal

Define what strict mode should consider a failure.

Initial policy options:

```text
none
validation_errors
quarantine_error_candidates
any_quarantine_candidate
any_warning_or_error
```

Recommended initial CLI option:

```text
--strict
```

Recommended default strict policy:

```text
validation_errors + quarantine_error_candidates
```

## Expected Files

```text
docs/design/strict_mode_policy.md
log_protocol/09_CSV_strict_mode_and_exit_codes/003_strict_mode_policy.md
```

## Acceptance Criteria

- Strict mode behavior is documented.
- Default remains non-strict.
- Initial failure conditions are documented.
- Future policy modes are documented but not necessarily implemented.

---

# Stage D — Pipeline Status Builder

## Goal

Add a small report/policy module that creates pipeline status from the diagnostic bundle.

Possible file:

```text
data_processor/reports/pipeline_status.py
```

Matching docs:

```text
data_processor/reports/pipeline_status.md
```

Possible function:

```python
build_pipeline_status(
    diagnostic_bundle,
    strict_mode=False,
)
```

## Expected Files

```text
data_processor/reports/pipeline_status.py
data_processor/reports/pipeline_status.md
tests/test_pipeline_status.py
tests/test_pipeline_status.md
log_protocol/09_CSV_strict_mode_and_exit_codes/004_pipeline_status_builder.md
```

## Acceptance Criteria

- Builds status from diagnostic bundle.
- Detects validation failures.
- Detects quarantine candidate errors and warnings.
- Non-strict mode never fails policy.
- Strict mode can produce `failed_policy`.
- Tests cover success, warnings, validation failure, and quarantine error failure.

---

# Stage E — Pipeline Integration

## Goal

Return pipeline status from `run_csv_pipeline()`.

Potential signature:

```python
run_csv_pipeline(
    input_path,
    output_path,
    report_path=None,
    constraints=None,
    strict_mode=False,
)
```

Expected files:

```text
data_processor/core/pipeline.py
data_processor/core/pipeline.md
tests/test_pipeline.py
tests/test_pipeline.md
log_protocol/09_CSV_strict_mode_and_exit_codes/005_pipeline_integration.md
```

## Acceptance Criteria

- Existing calls continue to work.
- `strict_mode` defaults to `False`.
- Pipeline result includes `pipeline_status`.
- CSV export still runs unless an execution error occurs.
- Strict policy failure is reported, not confused with execution failure.

---

# Stage F — CLI Exit Code Design

## Goal

Define CLI exit codes.

Recommended exit codes:

```text
0 = success or completed with warnings in non-strict mode
1 = execution error
2 = strict policy failure
```

Optional future codes:

```text
3 = invalid CLI/config input
4 = input file/access error
```

## Expected Files

```text
docs/design/cli_exit_codes.md
log_protocol/09_CSV_strict_mode_and_exit_codes/006_cli_exit_code_design.md
```

## Acceptance Criteria

- Exit codes are documented.
- Strict policy failure is separate from execution failure.
- Future codes are documented as deferred if not implemented.

---

# Stage G — CLI Strict Mode Option

## Goal

Add CLI support for strict mode.

Expected option:

```text
--strict
```

Expected behavior:

```text
without --strict → exit 0 when processing succeeds
with --strict and serious issues → exit 2
with execution failure → exit 1
```

Expected files:

```text
scripts/run_csv_pipeline.py
scripts/run_csv_pipeline.md
tests/test_cli_strict_mode.py
tests/test_cli_strict_mode.md
log_protocol/09_CSV_strict_mode_and_exit_codes/007_cli_strict_mode_option.md
```

## Acceptance Criteria

- CLI accepts `--strict`.
- CLI prints pipeline status.
- CLI exits `2` on strict policy failure.
- CLI preserves exit `0` for non-strict successful execution.
- CLI exits `1` for unexpected execution errors.

---

# Stage H — Example Workflow Update

## Goal

Update user examples to show strict and non-strict behavior.

Expected files:

```text
docs/user_guides/run_csv_pipeline_example.md
docs/user_guides/csv_report_interpretation.md
tests/test_example_csv_workflow.py
tests/test_example_csv_workflow.md
log_protocol/09_CSV_strict_mode_and_exit_codes/008_example_workflow_update.md
```

## Acceptance Criteria

- User guide shows normal mode.
- User guide shows strict mode.
- Documentation explains exit code `2`.
- Example workflow test checks pipeline status exists.

---

# Stage I — CI/Automation Usage Guide

## Goal

Document how strict mode can be used in automated workflows.

Expected file:

```text
docs/development/strict_mode_ci_usage.md
```

Example:

```powershell
python scripts\run_csv_pipeline.py input.csv output.csv --constraints-path constraints.json --report-path report.json --strict
```

## Expected Files

```text
docs/development/strict_mode_ci_usage.md
log_protocol/09_CSV_strict_mode_and_exit_codes/009_ci_usage_guide.md
```

## Acceptance Criteria

- Explains how exit code `2` can fail CI jobs.
- Explains difference between data-policy failure and execution failure.
- Does not enable GitHub Actions strict data checks automatically.

---

## Out Of Scope

This plan does not include:

```text
automatic row removal
separate quarantine export
blocking CSV export before report creation
hard GitHub branch protection
HTML reports
new validation rules
semantic cross-field validation
```

---

## Recommended Implementation Order

```text
Stage A — Current CLI and Pipeline Behavior Review
Stage B — Pipeline Status Model Design
Stage C — Strict Mode Policy Design
Stage D — Pipeline Status Builder
Stage E — Pipeline Integration
Stage F — CLI Exit Code Design
Stage G — CLI Strict Mode Option
Stage H — Example Workflow Update
Stage I — CI/Automation Usage Guide
```

---

## Required Protocol Folder

When active, use:

```text
log_protocol/09_CSV_strict_mode_and_exit_codes/
```

Protocol files:

```text
001_current_behavior_review.md
002_pipeline_status_model.md
003_strict_mode_policy.md
004_pipeline_status_builder.md
005_pipeline_integration.md
006_cli_exit_code_design.md
007_cli_strict_mode_option.md
008_example_workflow_update.md
009_ci_usage_guide.md
999_plan_completion.md
```

---

## Activation Rule

This plan is not active until the user explicitly confirms:

```text
Start 09_CSV_strict_mode_and_exit_codes
```

Until then, continue only with the currently active confirmed plan.
