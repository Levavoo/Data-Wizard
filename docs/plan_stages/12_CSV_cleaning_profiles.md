# CSV Cleaning Profiles Plan

## Status

```text
Draft — not active until user confirmation.
```

This plan focuses on reusable CSV cleaning profiles.

It must not be started automatically.

---

## Purpose

The CSV pipeline now supports many useful options:

```text
cleaned CSV output
JSON diagnostic report
HTML diagnostic report
constraint validation
strict mode
quarantine candidate export
quarantine rows export
accepted rows export
```

The next problem is that users must remember many separate CLI options and policy decisions.

Goal:

```text
profile name or profile config
→ predefined cleaning/reporting/validation behavior
→ simpler repeatable CSV workflows
```

---

## Current Default Policy

Current behavior must remain unchanged:

```text
no profile is required
existing CLI arguments continue to work
existing pipeline calls continue to work
profile use is optional
explicit CLI options should override profile defaults where appropriate
```

---

## Problem

Current CLI workflows are powerful but becoming long.

Example:

```text
--constraints-path
--report-path
--html-report-path
--quarantine-candidates-path
--quarantine-rows-path
--accepted-rows-path
--strict
```

For repeated real-world workflows, users need named profiles such as:

```text
default
light_touch
migration_audit
strict_crm
financial_review
```

---

## Architectural Layer

This plan belongs mainly to:

```text
Configuration Layer
Pipeline Orchestration Layer
CLI Layer
Documentation Layer
```

Main module areas:

```text
data_processor/config/
data_processor/core/
scripts/
docs/
tests/
```

Rules:

```text
Profiles must not mutate data by themselves.
Profiles should only define pipeline options and policy defaults.
Profiles must not remove rows automatically.
Profiles must be explicit and inspectable.
Existing non-profile behavior must remain stable.
```

---

# Stage A — Current Option Surface Review

## Goal

Document current pipeline and CLI options that profiles may eventually configure.

Expected files to inspect:

```text
data_processor/core/pipeline.py
scripts/run_csv_pipeline.py
docs/user_guides/run_csv_pipeline_example.md
```

## Expected Files

```text
docs/design/current_csv_option_surface.md
log_protocol/12_CSV_cleaning_profiles/001_current_option_surface_review.md
```

## Acceptance Criteria

- Current pipeline options are documented.
- Current CLI options are documented.
- Profile candidates are identified.
- No production code change is required in this stage.

---

# Stage B — Cleaning Profile Policy Design

## Goal

Define what a cleaning profile is and what it can control.

Suggested profile fields:

```text
name
description
strict_mode
report_outputs
quarantine_exports
constraints_path
notes
```

Potential future fields:

```text
null_policy
number_policy
encoding_policy
delimiter_policy
row_classification_policy
strict_policy
```

## Expected Files

```text
docs/design/cleaning_profile_policy.md
log_protocol/12_CSV_cleaning_profiles/002_cleaning_profile_policy.md
```

## Acceptance Criteria

- Profile purpose is documented.
- Supported initial profile fields are documented.
- Explicit override behavior is documented.
- Future profile fields are documented separately from current scope.

---

# Stage C — Built-In Profile Definitions

## Goal

Define initial built-in profiles as plain data.

Suggested profiles:

```text
default
light_touch
migration_audit
strict_crm
```

Suggested behavior:

```text
default = current behavior
light_touch = minimal diagnostics, no strict mode
migration_audit = reports + quarantine exports, no strict mode
strict_crm = reports + quarantine exports + strict mode
```

Possible file:

```text
data_processor/config/cleaning_profiles.py
```

Matching docs:

```text
data_processor/config/cleaning_profiles.md
```

## Expected Files

```text
data_processor/config/cleaning_profiles.py
data_processor/config/cleaning_profiles.md
tests/test_cleaning_profiles.py
tests/test_cleaning_profiles.md
log_protocol/12_CSV_cleaning_profiles/003_builtin_profile_definitions.md
```

## Acceptance Criteria

- Built-in profile definitions exist.
- Profiles are plain dictionaries or dataclasses.
- Profiles do not execute pipeline logic.
- Tests verify available profile names and default values.

---

# Stage D — Profile Resolution Utility

## Goal

Add a utility that resolves a named profile plus explicit overrides into pipeline options.

Possible file:

```text
data_processor/config/profile_resolver.py
```

Matching docs:

```text
data_processor/config/profile_resolver.md
```

Possible function:

```python
resolve_profile_options(
    profile_name,
    overrides=None,
) -> dict
```

## Expected Files

```text
data_processor/config/profile_resolver.py
data_processor/config/profile_resolver.md
tests/test_profile_resolver.py
tests/test_profile_resolver.md
log_protocol/12_CSV_cleaning_profiles/004_profile_resolution_utility.md
```

## Acceptance Criteria

- Resolves known profile names.
- Raises clear error for unknown profiles.
- Applies explicit overrides safely.
- Does not call the pipeline.
- Tests cover default resolution and override precedence.

---

# Stage E — CLI Profile Option

## Goal

Add CLI support for selecting a built-in profile.

Expected option:

```text
--profile
```

Example:

```powershell
python scripts\run_csv_pipeline.py input.csv output.csv --profile migration_audit
```

Expected files:

```text
scripts/run_csv_pipeline.py
scripts/run_csv_pipeline.md
tests/test_cli_cleaning_profiles.py
tests/test_cli_cleaning_profiles.md
log_protocol/12_CSV_cleaning_profiles/005_cli_profile_option.md
```

## Acceptance Criteria

- CLI accepts `--profile`.
- Profile defaults are applied.
- Explicit CLI options override profile defaults where appropriate.
- Existing CLI behavior works without profile.
- Tests verify profile use through CLI.

---

# Stage F — Profile-Driven Output Path Policy

## Goal

Define how profiles should handle generated output paths.

Problem:

```text
profiles can enable reports or quarantine exports,
but paths must be predictable and safe
```

Suggested policy:

```text
profiles can enable output types
CLI should still require explicit paths in this stage
automatic path generation is deferred
```

Alternative future policy:

```text
--output-dir data/processed
profile generates report paths automatically
```

## Expected Files

```text
docs/design/profile_output_path_policy.md
log_protocol/12_CSV_cleaning_profiles/006_profile_output_path_policy.md
```

## Acceptance Criteria

- Output path policy is documented.
- Automatic path generation is explicitly deferred unless implemented.
- No accidental file generation occurs.

---

# Stage G — User Guide Update

## Goal

Update user documentation with profile examples.

Expected files:

```text
docs/user_guides/run_csv_pipeline_example.md
docs/user_guides/csv_cleaning_profiles.md
log_protocol/12_CSV_cleaning_profiles/007_user_guide_update.md
```

## Acceptance Criteria

- User guide explains available profiles.
- User guide shows CLI examples.
- User guide explains profile vs explicit CLI overrides.
- User guide states that profiles are optional.

---

# Stage H — Example Workflow Profile Test

## Goal

Update example workflow tests to verify at least one profile-driven run.

Expected files:

```text
tests/test_example_csv_workflow.py
tests/test_example_csv_workflow.md
log_protocol/12_CSV_cleaning_profiles/008_example_workflow_profile_test.md
```

## Acceptance Criteria

- Example workflow can run with a profile.
- Existing explicit-argument workflow still works.
- Tests do not require large files.

---

# Stage I — Profile Limitations and Future Config File Bridge

## Goal

Document how built-in profiles relate to the next planned stage, config-file pipeline execution.

Expected next stage:

```text
13_CSV_config_file_pipeline
```

## Expected Files

```text
docs/design/profile_to_config_file_bridge.md
log_protocol/12_CSV_cleaning_profiles/009_profile_to_config_file_bridge.md
```

## Acceptance Criteria

- Built-in profiles are documented as a first step.
- Full external config files are explicitly deferred to Stage 13.
- Future relationship between profile and config file is documented.

---

## Out Of Scope

This plan does not include:

```text
external profile config files
automatic output path generation unless separately confirmed
row deletion
automatic quarantine application
new parsing algorithms
new validation rules
Excel support
large-file stress testing
interactive profile editor
```

---

## Recommended Implementation Order

```text
Stage A — Current Option Surface Review
Stage B — Cleaning Profile Policy Design
Stage C — Built-In Profile Definitions
Stage D — Profile Resolution Utility
Stage E — CLI Profile Option
Stage F — Profile-Driven Output Path Policy
Stage G — User Guide Update
Stage H — Example Workflow Profile Test
Stage I — Profile Limitations and Future Config File Bridge
```

---

## Required Protocol Folder

When active, use:

```text
log_protocol/12_CSV_cleaning_profiles/
```

Protocol files:

```text
001_current_option_surface_review.md
002_cleaning_profile_policy.md
003_builtin_profile_definitions.md
004_profile_resolution_utility.md
005_cli_profile_option.md
006_profile_output_path_policy.md
007_user_guide_update.md
008_example_workflow_profile_test.md
009_profile_to_config_file_bridge.md
999_plan_completion.md
```

---

## Activation Rule

This plan is not active until the user explicitly confirms:

```text
Start 12_CSV_cleaning_profiles
```

Until then, continue only with the currently active confirmed plan.
