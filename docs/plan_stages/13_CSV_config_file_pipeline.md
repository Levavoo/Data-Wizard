# CSV Config File Pipeline Plan

## Status

```text
Draft — not active until user confirmation.
```

This plan focuses on running the CSV pipeline from a single explicit configuration file.

It must not be started automatically.

---

## Purpose

The CSV pipeline now supports many CLI options:

```text
input/output paths
cleaning profiles
constraints
JSON reports
HTML reports
quarantine exports
strict mode
```

Long CLI commands are useful for direct control, but repeated migration workflows need a saveable configuration file.

Goal:

```text
pipeline config file
→ validated runtime options
→ run_csv_pipeline()
→ repeatable CSV workflow
```

---

## Current Default Policy

Current behavior must remain unchanged:

```text
existing positional CLI usage still works
existing --profile usage still works
existing explicit CLI options still work
config file usage is optional
config values must be explicit and inspectable
```

---

## Problem

Current commands can become long and error-prone:

```text
python scripts/run_csv_pipeline.py input.csv output.csv \
  --profile migration_audit \
  --constraints-path constraints.json \
  --report-path report.json \
  --html-report-path report.html \
  --quarantine-candidates-path quarantine_candidates.json \
  --quarantine-rows-path quarantine_rows.csv \
  --accepted-rows-path accepted_rows.csv
```

Users need a reusable file like:

```json
{
  "input_path": "data/raw/customers.csv",
  "output_path": "data/processed/customers_clean.csv",
  "profile": "migration_audit",
  "constraints_path": "data/raw/customer_constraints.json",
  "report_path": "data/processed/customers_report.json",
  "html_report_path": "data/processed/customers_report.html",
  "quarantine_candidates_path": "data/processed/quarantine_candidates.json",
  "quarantine_rows_path": "data/processed/quarantine_rows.csv",
  "accepted_rows_path": "data/processed/accepted_rows.csv",
  "strict_mode": false
}
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
scripts/
docs/
tests/
examples/
```

Rules:

```text
Config loading must not run the pipeline directly.
Config validation must not mutate data.
Config files must be explicit and inspectable.
Existing CLI usage must remain supported.
Explicit CLI overrides should remain possible where practical.
```

---

# Stage A — Current Config Inputs Review

## Goal

Document current profile, constraints, and path inputs that a config file should support.

Expected files to inspect:

```text
scripts/run_csv_pipeline.py
data_processor/config/profile_resolver.py
data_processor/validators/constraint_config.py
data_processor/core/pipeline.py
```

## Expected Files

```text
docs/design/current_config_input_surface.md
log_protocol/13_CSV_config_file_pipeline/001_current_config_input_surface.md
```

## Acceptance Criteria

- Current config-like inputs are documented.
- Config file fields are listed.
- No production code change is required in this stage.

---

# Stage B — CSV Pipeline Config Schema Design

## Goal

Define the initial JSON config file shape.

Suggested fields:

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
```

Optional future fields:

```text
output_dir
auto_generate_report_paths
null_policy
number_policy
encoding_policy
delimiter_policy
```

## Expected Files

```text
docs/design/csv_pipeline_config_schema.md
log_protocol/13_CSV_config_file_pipeline/002_config_schema_design.md
```

## Acceptance Criteria

- Config schema is documented.
- Required fields are documented.
- Optional fields are documented.
- Future fields are separated from current implementation.

---

# Stage C — Config Model and Loader

## Goal

Add a config loader that reads JSON into a validated config object or dictionary.

Possible file:

```text
data_processor/config/pipeline_config.py
```

Matching docs:

```text
data_processor/config/pipeline_config.md
```

Possible functions:

```python
load_pipeline_config(path) -> dict
validate_pipeline_config(config) -> dict
```

## Expected Files

```text
data_processor/config/pipeline_config.py
data_processor/config/pipeline_config.md
tests/test_pipeline_config.py
tests/test_pipeline_config.md
log_protocol/13_CSV_config_file_pipeline/003_config_model_and_loader.md
```

## Acceptance Criteria

- Loads UTF-8 JSON config files.
- Validates required fields.
- Rejects unknown fields with a clear error.
- Preserves optional fields.
- Does not run the pipeline.
- Tests cover valid config, missing required fields, and unknown fields.

---

# Stage D — Config-to-Pipeline Options Resolver

## Goal

Convert a loaded config into pipeline call arguments.

Possible file:

```text
data_processor/config/pipeline_config_resolver.py
```

Matching docs:

```text
data_processor/config/pipeline_config_resolver.md
```

Possible function:

```python
resolve_pipeline_config_options(config) -> dict
```

Responsibilities:

```text
resolve profile defaults
apply config strict_mode override
keep explicit paths from config
prepare constraints_path for CLI loader
```

## Expected Files

```text
data_processor/config/pipeline_config_resolver.py
data_processor/config/pipeline_config_resolver.md
tests/test_pipeline_config_resolver.py
tests/test_pipeline_config_resolver.md
log_protocol/13_CSV_config_file_pipeline/004_config_to_pipeline_resolver.md
```

## Acceptance Criteria

- Resolves profile defaults.
- Applies explicit `strict_mode` from config.
- Preserves configured paths.
- Does not load constraints directly unless explicitly designed.
- Does not run the pipeline.

---

# Stage E — CLI `--config` Support

## Goal

Allow the CLI to run from a JSON config file.

Expected option:

```text
--config
```

Example:

```powershell
python scripts\run_csv_pipeline.py --config configs\customer_migration.json
```

Important decision:

```text
When --config is used, positional input_path/output_path should not be required.
```

Expected files:

```text
scripts/run_csv_pipeline.py
scripts/run_csv_pipeline.md
tests/test_cli_pipeline_config.py
tests/test_cli_pipeline_config.md
log_protocol/13_CSV_config_file_pipeline/005_cli_config_option.md
```

## Acceptance Criteria

- CLI accepts `--config`.
- CLI can run without positional input/output paths when config provides them.
- Existing positional CLI usage still works.
- Config values are passed to pipeline.
- Tests verify successful config-driven CLI run.

---

# Stage F — CLI Override Policy

## Goal

Define and implement how explicit CLI values interact with config file values.

Recommended initial policy:

```text
--config provides defaults
explicit CLI arguments override config values when provided
```

Potential override fields:

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
strict/no-strict
```

## Expected Files

```text
docs/design/pipeline_config_override_policy.md
scripts/run_csv_pipeline.py
scripts/run_csv_pipeline.md
tests/test_cli_pipeline_config_overrides.py
tests/test_cli_pipeline_config_overrides.md
log_protocol/13_CSV_config_file_pipeline/006_cli_config_override_policy.md
```

## Acceptance Criteria

- Override policy is documented.
- Explicit CLI paths override config paths where provided.
- Explicit strict flags override config strict mode.
- Existing behavior without config remains unchanged.

---

# Stage G — Example Config File

## Goal

Add a small example config file for the customer migration example.

Possible file:

```text
examples/csv/customer_migration_config.json
```

Matching docs:

```text
examples/csv/customer_migration_config.md
```

## Expected Files

```text
examples/csv/customer_migration_config.json
examples/csv/customer_migration_config.md
log_protocol/13_CSV_config_file_pipeline/007_example_config_file.md
```

## Acceptance Criteria

- Example config references existing example CSV and constraints.
- Example config writes to ignored processed-data paths.
- Documentation explains every field.

---

# Stage H — User Guide Update

## Goal

Update user documentation to show config-file execution.

Expected files:

```text
docs/user_guides/run_csv_pipeline_example.md
docs/user_guides/csv_pipeline_config_files.md
log_protocol/13_CSV_config_file_pipeline/008_user_guide_update.md
```

## Acceptance Criteria

- User guide shows `--config` command.
- User guide explains config values vs CLI overrides.
- User guide explains relationship to profiles.

---

# Stage I — Example Workflow Config Test

## Goal

Update example workflow tests to verify config-file execution.

Expected files:

```text
tests/test_example_csv_workflow.py
tests/test_example_csv_workflow.md
log_protocol/13_CSV_config_file_pipeline/009_example_workflow_config_test.md
```

## Acceptance Criteria

- Example workflow can run through CLI using `--config`.
- Existing explicit-argument and profile workflow tests still work.
- Tests verify expected output files are written.

---

# Stage J — Config Limitations and Future Auto Paths

## Goal

Document limitations and future work for auto-generated paths.

Expected files:

```text
docs/design/config_auto_output_path_future.md
log_protocol/13_CSV_config_file_pipeline/010_config_limitations_and_future_paths.md
```

## Acceptance Criteria

- Current config file behavior is documented as explicit-path only.
- Auto output path generation is deferred.
- Future `output_dir` policy is described without implementing it.

---

## Out Of Scope

This plan does not include:

```text
YAML config files
TOML config files
automatic output path generation unless separately confirmed
external cleaning profile files
row deletion
new validation rules
new cleaning rules
batch folder processing
Excel input
JSON input
large-file stress testing
```

---

## Recommended Implementation Order

```text
Stage A — Current Config Inputs Review
Stage B — CSV Pipeline Config Schema Design
Stage C — Config Model and Loader
Stage D — Config-to-Pipeline Options Resolver
Stage E — CLI --config Support
Stage F — CLI Override Policy
Stage G — Example Config File
Stage H — User Guide Update
Stage I — Example Workflow Config Test
Stage J — Config Limitations and Future Auto Paths
```

---

## Required Protocol Folder

When active, use:

```text
log_protocol/13_CSV_config_file_pipeline/
```

Protocol files:

```text
001_current_config_input_surface.md
002_config_schema_design.md
003_config_model_and_loader.md
004_config_to_pipeline_resolver.md
005_cli_config_option.md
006_cli_config_override_policy.md
007_example_config_file.md
008_user_guide_update.md
009_example_workflow_config_test.md
010_config_limitations_and_future_paths.md
999_plan_completion.md
```

---

## Activation Rule

This plan is not active until the user explicitly confirms:

```text
Start 13_CSV_config_file_pipeline
```

Until then, continue only with the currently active confirmed plan.
