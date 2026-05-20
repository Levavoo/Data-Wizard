# JSON Adapter Plan

## Status

```text
Draft — not active until user confirmation.
```

This plan adds JSON input support to the Data Wizard pipeline.

It must not be started automatically.

---

## Purpose

The CSV core is now stable enough to use as a foundation for additional input formats.

The next format should be JSON because it is simpler than Excel and is a good test of whether the internal `Table` / `Schema` model can support non-CSV input sources.

Goal:

```text
read JSON files
convert supported JSON structures into the internal Table model
preserve parse/source diagnostics
reuse existing cleaning, inference, validation, reporting, quarantine, config, and CLI layers
avoid deep arbitrary JSON flattening in the first implementation
```

---

## First Scope

The first JSON adapter should support a conservative, predictable subset.

Supported initially:

```text
JSON file containing a list of objects
flat object records
missing keys across records become null
extra keys across records become columns
primitive values: string, number, boolean, null
simple nested objects only if explicit flattening policy is implemented
```

Recommended first supported JSON shape:

```json
[
  {
    "customer_id": 1,
    "name": "Alice",
    "email": "alice@example.com",
    "amount": 120.5,
    "active": true
  },
  {
    "customer_id": 2,
    "name": "Bob",
    "email": "bob@example.com",
    "active": false
  }
]
```

Expected result:

```text
columns are union of all object keys
missing amount for Bob becomes None
existing CSV pipeline stages can process the resulting Table
```

---

## Out Of Scope For First JSON Adapter

Do not implement initially:

```text
arbitrary deep flattening
multiple root shapes in one adapter pass
streaming JSON parser
JSON Lines / NDJSON
schema inference beyond current Table model
business-specific JSON transformations
array explosion
nested table extraction
automatic relation modeling
```

These can be future stages.

---

## JSON Root Shape Policy

Supported root shape for Stage 18:

```text
list[object]
```

Rejected or deferred root shapes:

```text
single object
object with records under a nested key
list of primitive values
mixed list values
empty file
invalid JSON
```

Possible future support:

```text
single object as one-row table
root_path option for nested records
JSON Lines adapter
```

---

## Column Policy

Column names should come from JSON object keys.

Rules:

```text
preserve original key as column original_name
normalize key into internal column name using similar rules to CSV header normalization
make duplicate normalized keys unique if needed
union keys across all records
missing key in a record becomes None
```

Example:

```json
[
  {"Customer ID": 1, "Name": "Alice"},
  {"Customer ID": 2, "Email": "bob@example.com"}
]
```

Expected columns:

```text
customer_id
name
email
```

Expected rows:

```text
row 1: customer_id=1, name=Alice, email=None
row 2: customer_id=2, name=None, email=bob@example.com
```

---

## Primitive Value Policy

Supported JSON value types:

```text
string
number
boolean
null
```

Conversion into Table rows:

```text
string -> string
number -> int/float or raw Python numeric value
boolean -> bool
null -> None
```

Existing pipeline cleaning/type-casting should then handle values consistently.

---

## Nested Value Policy

First implementation should be conservative.

Recommended initial behavior:

```text
nested object values are preserved as compact JSON strings or flagged as unsupported, depending Stage A decision
array values are preserved as compact JSON strings or flagged as unsupported, depending Stage A decision
```

Important:

```text
Do not silently flatten nested data before policy is documented.
```

Preferred first decision:

```text
convert nested objects/arrays to compact JSON strings and report them in parse diagnostics
```

Reason:

```text
this avoids data loss while keeping one-row-per-object table shape
```

---

## Parse Diagnostics Policy

JSON adapter should attach source diagnostics similar to CSV parse diagnostics.

Expected diagnostic fields:

```text
source_format = json
root_type
record_count
column_count
missing_key_counts
extra_or_union_key_count
nested_value_columns
array_value_columns
invalid_record_indexes
warnings
```

Possible diagnostics object:

```text
JsonParseDiagnostics
```

Possible file:

```text
data_processor/adapters/json_parse_diagnostics.py
```

---

## Pipeline Integration Policy

First implementation should not rewrite the main pipeline heavily.

Possible approach:

```text
create JsonAdapter
create run_json_pipeline wrapper if needed
or generalize pipeline to adapter selection by input format
```

Preferred conservative approach:

```text
add JsonAdapter and a small run_json_pipeline function that mirrors run_csv_pipeline while reusing shared pipeline internals if available
```

Possible future improvement:

```text
general run_pipeline(input_path, output_path, input_format="auto")
```

Do not force this larger refactor unless necessary.

---

## CLI Policy

CLI should support JSON only after adapter tests pass.

Possible CLI approaches:

Option A:

```text
scripts/run_json_pipeline.py
```

Option B:

```text
scripts/run_data_pipeline.py --input-format json
```

Option C:

```text
extend scripts/run_csv_pipeline.py into a general runner later
```

Recommended first approach:

```text
create scripts/run_json_pipeline.py
```

Reason:

```text
avoids destabilizing the mature CSV CLI
keeps JSON scope isolated
allows later unification after JSON and Excel adapters exist
```

---

## Config Policy

JSON config support should be added only after CLI/pipeline behavior is stable.

Possible config fields:

```text
input_format = json
nested_values = stringify | reject
root_path = future only
```

First config behavior:

```text
minimal JSON config support or deferred until adapter is stable
```

Recommended:

```text
support JSON through dedicated script first
then add general config format after behavior is proven
```

---

# Stage A — JSON Scope and Shape Policy

## Goal

Document exactly which JSON shapes are supported and which are rejected/deferred.

Expected files:

```text
docs/design/json_adapter_scope.md
docs/design/json_shape_policy.md
log_protocol/18_JSON_adapter/001_json_scope_and_shape_policy.md
```

Acceptance criteria:

- Supported root shape is documented.
- Unsupported root shapes are documented.
- Nested value behavior is decided.
- Column union behavior is documented.
- No code changes required.

---

# Stage B — JSON Fixtures

## Goal

Create small JSON fixtures for supported and unsupported shapes.

Expected files:

```text
tests/fixtures/json/simple_customers.json
tests/fixtures/json/missing_keys_customers.json
tests/fixtures/json/nested_values_customers.json
tests/fixtures/json/invalid_root_object.json
tests/fixtures/json/mixed_list_values.json
tests/fixtures/json/README.md
log_protocol/18_JSON_adapter/002_json_fixtures.md
```

Acceptance criteria:

- Supported flat list fixture exists.
- Missing key fixture exists.
- Nested value fixture exists.
- Unsupported root fixtures exist.
- Fixture documentation exists.

---

# Stage C — JsonParseDiagnostics Model

## Goal

Create JSON-specific parse diagnostics.

Expected files:

```text
data_processor/adapters/json_parse_diagnostics.py
data_processor/adapters/json_parse_diagnostics.md
tests/test_json_parse_diagnostics.py
tests/test_json_parse_diagnostics.md
log_protocol/18_JSON_adapter/003_json_parse_diagnostics.md
```

Expected diagnostic fields:

```text
root_type
record_count
column_count
missing_key_counts
nested_value_columns
array_value_columns
invalid_record_indexes
warnings
```

Acceptance criteria:

- Diagnostics are serializable.
- Warnings can be added.
- Tests cover empty/default diagnostics.

---

# Stage D — JsonAdapter Implementation

## Goal

Implement JSON adapter that converts supported JSON files into the internal Table model.

Expected files:

```text
data_processor/adapters/json_adapter.py
data_processor/adapters/json_adapter.md
tests/test_json_adapter.py
tests/test_json_adapter.md
log_protocol/18_JSON_adapter/004_json_adapter_implementation.md
```

Acceptance criteria:

- Reads list-of-objects JSON files.
- Creates Table and Schema.
- Unions keys across records.
- Missing keys become None.
- Primitive values are preserved.
- Nested values follow Stage A policy.
- Unsupported root shapes raise clear errors.
- Metadata includes `source_format = json`.
- Metadata includes JSON parse diagnostics.

---

# Stage E — JSON Pipeline Integration

## Goal

Run JSON input through existing cleaning, inference, validation, reporting, and export layers.

Possible files:

```text
data_processor/core/json_pipeline.py
data_processor/core/json_pipeline.md
tests/test_json_pipeline.py
tests/test_json_pipeline.md
log_protocol/18_JSON_adapter/005_json_pipeline_integration.md
```

Acceptance criteria:

- JSON pipeline writes clean CSV output.
- JSON pipeline returns diagnostic bundle.
- Existing validation constraints work.
- JSON parse diagnostics appear in report.
- Existing CSV pipeline remains unchanged.

---

# Stage F — JSON CLI Support

## Goal

Add a user-facing JSON pipeline command.

Recommended file:

```text
scripts/run_json_pipeline.py
scripts/run_json_pipeline.md
```

Tests:

```text
tests/test_cli_json_pipeline.py
tests/test_cli_json_pipeline.md
```

Protocol:

```text
log_protocol/18_JSON_adapter/006_json_cli_support.md
```

Acceptance criteria:

- CLI processes supported JSON fixture.
- CLI writes clean CSV output.
- CLI can write JSON report.
- CLI can write HTML report if shared pipeline supports it.
- CLI can use constraints if supported by JSON pipeline.

---

# Stage G — JSON Report and Diagnostics Integration

## Goal

Ensure JSON parse diagnostics appear clearly in diagnostic reports.

Expected files:

```text
docs/testing/json_adapter_expected_report.md
tests/test_json_report_integration.py
tests/test_json_report_integration.md
log_protocol/18_JSON_adapter/007_json_report_diagnostics_integration.md
```

Acceptance criteria:

- Diagnostic bundle includes JSON parse diagnostics.
- JSON report export includes JSON diagnostics.
- HTML report can render JSON-origin diagnostics.
- Unsupported/nested values are visible in diagnostics.

---

# Stage H — JSON Config Support

## Goal

Decide and implement config-file support for JSON input if the pipeline shape is stable.

Possible files:

```text
examples/json/json_customer_config.json
examples/json/README.md
tests/test_json_config_pipeline.py
tests/test_json_config_pipeline.md
log_protocol/18_JSON_adapter/008_json_config_support.md
```

Acceptance criteria:

- Config can run JSON pipeline or decision to defer is documented.
- Input format is explicit if general config is used.
- CSV config behavior remains unchanged.

---

# Stage I — JSON User Guide

## Goal

Document how to use JSON support.

Expected files:

```text
docs/user_guides/json_pipeline.md
log_protocol/18_JSON_adapter/009_json_user_guide.md
```

Guide should explain:

```text
supported JSON shape
unsupported JSON shapes
how missing keys are handled
how nested values are handled
how to run CLI
how to generate reports
known limitations
```

Acceptance criteria:

- User can run JSON workflow from docs.
- Limitations are clear.
- No false claim of arbitrary JSON support.

---

# Stage J — JSON Adapter Completion Report

## Goal

Record final state and next steps.

Expected files:

```text
docs/release/json_adapter_state.md
log_protocol/18_JSON_adapter/999_plan_completion.md
```

Acceptance criteria:

- Completed features are listed.
- Unsupported JSON features are listed.
- Local verification commands are listed.
- Next recommended stage is documented.

---

## Recommended Implementation Order

```text
Stage A — JSON Scope and Shape Policy
Stage B — JSON Fixtures
Stage C — JsonParseDiagnostics Model
Stage D — JsonAdapter Implementation
Stage E — JSON Pipeline Integration
Stage F — JSON CLI Support
Stage G — JSON Report and Diagnostics Integration
Stage H — JSON Config Support
Stage I — JSON User Guide
Stage J — JSON Adapter Completion Report
```

---

## Required Protocol Folder

When active, use:

```text
log_protocol/18_JSON_adapter/
```

Protocol files:

```text
001_json_scope_and_shape_policy.md
002_json_fixtures.md
003_json_parse_diagnostics.md
004_json_adapter_implementation.md
005_json_pipeline_integration.md
006_json_cli_support.md
007_json_report_diagnostics_integration.md
008_json_config_support.md
009_json_user_guide.md
999_plan_completion.md
```

---

## Verification Commands

After implementation stages, run targeted tests:

```powershell
python -m pytest tests/test_json_parse_diagnostics.py
python -m pytest tests/test_json_adapter.py
python -m pytest tests/test_json_pipeline.py
python -m pytest tests/test_cli_json_pipeline.py
python -m pytest tests/test_json_report_integration.py
```

Then run full suite:

```powershell
python -m pytest
```

---

## Activation Rule

This plan is not active until the user explicitly confirms:

```text
Start 18_JSON_adapter
```

Until then, continue only with the currently active confirmed plan.
