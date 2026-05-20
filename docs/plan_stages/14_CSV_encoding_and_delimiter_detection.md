# CSV Encoding and Delimiter Detection Plan

## Status

```text
Draft — not active until user confirmation.
```

This plan focuses on safer CSV input detection for real-world files.

It must not be started automatically.

---

## Purpose

The CSV pipeline can now clean, validate, report, export quarantine files, use profiles, and run from config files.

The next weakness is input robustness.

Real-world CSV files often differ in:

```text
encoding
delimiter
line endings
BOM presence
quote behavior
malformed rows
metadata/header placement
```

Goal:

```text
CSV file
→ detect encoding and delimiter safely
→ read with chosen parser settings
→ expose detection diagnostics
→ keep behavior predictable and configurable
```

---

## Current Default Policy

Current behavior must remain unchanged unless detection is explicitly integrated safely.

Policy:

```text
existing CSV parsing must continue to work
UTF-8 remains the safe default
comma remains the safe default where detection is inconclusive
ambiguous detection must be reported, not hidden
config/CLI overrides should win over auto-detection
```

---

## Problem

Current CSV parsing assumes stable input behavior.

Typical real-world failures:

```text
Windows-1252 files fail or misread special characters
UTF-8 BOM appears in first header
semicolon CSV is common in European exports
pipe/tab-delimited files are mislabeled as CSV
comma decimals conflict with semicolon-delimited exports
malformed rows are hard to diagnose
```

Expected future behavior:

```text
detect likely encoding
detect likely delimiter
allow explicit override
record parse detection diagnostics
use selected settings in CsvAdapter
surface detection result in diagnostic bundle/reports
```

---

## Architectural Layer

This plan belongs mainly to:

```text
Input Adapter Layer
Parse Diagnostics Layer
Configuration Layer
CLI Layer
Diagnostic Reporting Layer
```

Main module areas:

```text
data_processor/adapters/
data_processor/config/
data_processor/reports/
scripts/
docs/
tests/
```

Rules:

```text
Detection must be conservative.
Explicit config/CLI values override detection.
Detection should produce diagnostics.
Detection should not silently repair data.
Detection should not remove rows.
Detection should not change cleaning/validation semantics.
```

---

# Stage A — Current CSV Adapter Review

## Goal

Document the current CSV adapter behavior and parsing assumptions.

Expected files to inspect:

```text
data_processor/adapters/csv_adapter.py
data_processor/adapters/parse_diagnostics.py
data_processor/core/pipeline.py
```

## Expected Files

```text
docs/design/current_csv_adapter_detection_behavior.md
log_protocol/14_CSV_encoding_and_delimiter_detection/001_current_adapter_review.md
```

## Acceptance Criteria

- Current encoding behavior is documented.
- Current delimiter behavior is documented.
- Current parse diagnostics behavior is documented.
- No production code change is required in this stage.

---

# Stage B — Detection Policy Design

## Goal

Define conservative detection policy.

Policy decisions:

```text
explicit encoding overrides detection
explicit delimiter overrides detection
UTF-8 is preferred when valid
UTF-8-SIG handles BOM safely
fallback encodings are limited and documented
ambiguous delimiter detection falls back safely
```

Suggested encoding candidates:

```text
utf-8-sig
utf-8
cp1252
latin-1
```

Suggested delimiter candidates:

```text
,
;
\t
|
```

## Expected Files

```text
docs/design/csv_detection_policy.md
log_protocol/14_CSV_encoding_and_delimiter_detection/002_detection_policy.md
```

## Acceptance Criteria

- Encoding detection policy is documented.
- Delimiter detection policy is documented.
- Override precedence is documented.
- Ambiguity behavior is documented.

---

# Stage C — Encoding Detection Utility

## Goal

Add a small, dependency-free encoding detection utility.

Possible file:

```text
data_processor/adapters/encoding_detection.py
```

Matching docs:

```text
data_processor/adapters/encoding_detection.md
```

Possible function:

```python
detect_text_encoding(path, candidates=None) -> dict
```

Returned diagnostics should include:

```text
selected_encoding
candidate_results
confidence
reason
```

## Expected Files

```text
data_processor/adapters/encoding_detection.py
data_processor/adapters/encoding_detection.md
tests/test_encoding_detection.py
tests/test_encoding_detection.md
log_protocol/14_CSV_encoding_and_delimiter_detection/003_encoding_detection_utility.md
```

## Acceptance Criteria

- Detects UTF-8 files.
- Detects UTF-8 BOM safely.
- Falls back to cp1252/latin-1 when needed.
- Returns diagnostics, not only a string.
- Tests cover UTF-8, UTF-8 BOM, and cp1252-like content.

---

# Stage D — Delimiter Detection Utility

## Goal

Add a delimiter detection utility that samples text and chooses a likely delimiter conservatively.

Possible file:

```text
data_processor/adapters/delimiter_detection.py
```

Matching docs:

```text
data_processor/adapters/delimiter_detection.md
```

Possible function:

```python
detect_delimiter(text_sample, candidates=None) -> dict
```

Returned diagnostics should include:

```text
selected_delimiter
candidate_scores
confidence
reason
```

## Expected Files

```text
data_processor/adapters/delimiter_detection.py
data_processor/adapters/delimiter_detection.md
tests/test_delimiter_detection.py
tests/test_delimiter_detection.md
log_protocol/14_CSV_encoding_and_delimiter_detection/004_delimiter_detection_utility.md
```

## Acceptance Criteria

- Detects comma-delimited samples.
- Detects semicolon-delimited samples.
- Detects tab-delimited samples.
- Detects pipe-delimited samples.
- Falls back to comma when ambiguous.
- Tests cover ambiguous sample behavior.

---

# Stage E — CSV Adapter Integration

## Goal

Integrate detection into `CsvAdapter` while keeping explicit values supported.

Possible adapter parameters:

```python
encoding=None
delimiter=None
auto_detect=True
```

Behavior:

```text
explicit encoding wins
explicit delimiter wins
auto detection fills missing values
fallbacks are recorded
```

Expected files:

```text
data_processor/adapters/csv_adapter.py
data_processor/adapters/csv_adapter.md
tests/test_csv_adapter.py
tests/test_csv_adapter.md
log_protocol/14_CSV_encoding_and_delimiter_detection/005_csv_adapter_detection_integration.md
```

## Acceptance Criteria

- Existing CSV adapter tests still pass.
- Explicit delimiter still works.
- Semicolon files can be read through detection.
- BOM headers do not include BOM marker.
- Adapter stores parse detection diagnostics.

---

# Stage F — Parse Diagnostics Integration

## Goal

Expose encoding and delimiter detection in parse diagnostics.

Expected diagnostic section:

```text
parse_diagnostics.detection
```

Possible fields:

```text
selected_encoding
selected_delimiter
encoding_confidence
delimiter_confidence
encoding_reason
delimiter_reason
overrides_used
```

Expected files:

```text
data_processor/adapters/parse_diagnostics.py
data_processor/adapters/parse_diagnostics.md
tests/test_parse_diagnostics.py
tests/test_parse_diagnostics.md
log_protocol/14_CSV_encoding_and_delimiter_detection/006_parse_diagnostics_integration.md
```

## Acceptance Criteria

- Detection results appear in parse diagnostics.
- Explicit overrides are visible in diagnostics.
- Existing parse diagnostics remain backward-compatible where possible.

---

# Stage G — Pipeline Parameter Support

## Goal

Allow the pipeline to pass encoding/delimiter options to the CSV adapter.

Possible pipeline parameters:

```python
encoding=None
delimiter=None
auto_detect_csv=True
```

Expected files:

```text
data_processor/core/pipeline.py
data_processor/core/pipeline.md
tests/test_pipeline.py
tests/test_pipeline.md
log_protocol/14_CSV_encoding_and_delimiter_detection/007_pipeline_detection_options.md
```

## Acceptance Criteria

- Pipeline can read semicolon files through detection.
- Pipeline can read explicit delimiter override.
- Existing pipeline calls remain valid.
- Detection diagnostics remain available in reports.

---

# Stage H — Config File Support

## Goal

Add config-file support for encoding and delimiter options.

Possible config fields:

```text
encoding
delimiter
auto_detect_csv
```

Expected files:

```text
data_processor/config/pipeline_config.py
data_processor/config/pipeline_config.md
data_processor/config/pipeline_config_resolver.py
data_processor/config/pipeline_config_resolver.md
tests/test_pipeline_config.py
tests/test_pipeline_config_resolver.py
log_protocol/14_CSV_encoding_and_delimiter_detection/008_config_detection_options.md
```

## Acceptance Criteria

- Config accepts `encoding`.
- Config accepts `delimiter`.
- Config accepts `auto_detect_csv`.
- Unknown field rejection remains intact.
- Resolver passes values forward.

---

# Stage I — CLI Detection Options

## Goal

Expose encoding and delimiter controls through CLI.

Expected options:

```text
--encoding
--delimiter
--no-auto-detect-csv
```

Expected files:

```text
scripts/run_csv_pipeline.py
scripts/run_csv_pipeline.md
tests/test_cli_csv_detection_options.py
tests/test_cli_csv_detection_options.md
log_protocol/14_CSV_encoding_and_delimiter_detection/009_cli_detection_options.md
```

## Acceptance Criteria

- CLI accepts explicit encoding.
- CLI accepts explicit delimiter.
- CLI can disable auto-detection.
- CLI overrides config detection values.
- Existing CLI behavior remains unchanged.

---

# Stage J — Report and HTML Visibility

## Goal

Ensure detection diagnostics are visible in JSON and HTML reports.

Expected files:

```text
data_processor/reports/html_report.py
data_processor/reports/html_report.md
tests/test_html_report.py
tests/test_example_csv_workflow.py
log_protocol/14_CSV_encoding_and_delimiter_detection/010_report_detection_visibility.md
```

## Acceptance Criteria

- JSON diagnostic bundle includes detection details.
- HTML report shows selected encoding and delimiter.
- Example workflow still works.

---

# Stage K — User Guide and Examples

## Goal

Document detection behavior and add example commands/config snippets.

Expected files:

```text
docs/user_guides/csv_encoding_and_delimiter_detection.md
docs/user_guides/csv_pipeline_config_files.md
docs/user_guides/run_csv_pipeline_example.md
examples/csv/semicolon_customers_config.json
examples/csv/semicolon_customers_config.md
log_protocol/14_CSV_encoding_and_delimiter_detection/011_user_guide_and_examples.md
```

## Acceptance Criteria

- User guide explains auto-detection.
- User guide explains explicit override.
- User guide explains ambiguous fallback behavior.
- Example config demonstrates semicolon CSV.

---

# Stage L — Example Workflow Detection Test

## Goal

Add workflow-level coverage for detection behavior.

Expected files:

```text
tests/test_example_csv_workflow.py
tests/test_example_csv_workflow.md
log_protocol/14_CSV_encoding_and_delimiter_detection/012_example_workflow_detection_test.md
```

## Acceptance Criteria

- Example workflow can read semicolon CSV through detection.
- Example workflow can use explicit delimiter override.
- Existing example workflow tests still pass.

---

## Out Of Scope

This plan does not include:

```text
full malformed CSV repair
streaming parser rewrite
large-file performance optimization
external encoding detection libraries
Excel input
JSON input
automatic row deletion
interactive file import wizard
advanced dialect sniffing beyond conservative delimiter detection
```

---

## Recommended Implementation Order

```text
Stage A — Current CSV Adapter Review
Stage B — Detection Policy Design
Stage C — Encoding Detection Utility
Stage D — Delimiter Detection Utility
Stage E — CSV Adapter Integration
Stage F — Parse Diagnostics Integration
Stage G — Pipeline Parameter Support
Stage H — Config File Support
Stage I — CLI Detection Options
Stage J — Report and HTML Visibility
Stage K — User Guide and Examples
Stage L — Example Workflow Detection Test
```

---

## Required Protocol Folder

When active, use:

```text
log_protocol/14_CSV_encoding_and_delimiter_detection/
```

Protocol files:

```text
001_current_adapter_review.md
002_detection_policy.md
003_encoding_detection_utility.md
004_delimiter_detection_utility.md
005_csv_adapter_detection_integration.md
006_parse_diagnostics_integration.md
007_pipeline_detection_options.md
008_config_detection_options.md
009_cli_detection_options.md
010_report_detection_visibility.md
011_user_guide_and_examples.md
012_example_workflow_detection_test.md
999_plan_completion.md
```

---

## Activation Rule

This plan is not active until the user explicitly confirms:

```text
Start 14_CSV_encoding_and_delimiter_detection
```

Until then, continue only with the currently active confirmed plan.
