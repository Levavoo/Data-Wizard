# CSV Quarantine Export Plan

## Status

```text
Draft — not active until user confirmation.
```

This plan focuses on exporting quarantine candidate information and optionally exporting affected rows for manual review.

It must not be started automatically.

---

## Purpose

The CSV pipeline already identifies quarantine candidates in the diagnostic bundle.

Current behavior:

```text
rows are flagged for review
rows remain in cleaned CSV
no separate quarantine file is written
```

This plan adds optional export outputs so users can review problematic rows separately.

Goal:

```text
quarantine candidates
→ quarantine candidate JSON export
→ optional quarantine rows CSV export
→ optional accepted rows CSV export
→ safer migration review workflow
```

---

## Current Default Policy

Default behavior must remain unchanged:

```text
CSV export still includes all rows
quarantine candidates remain report-only by default
no rows are removed unless an explicit split export option is used
strict mode behavior remains unchanged
```

---

## Problem

The pipeline can now say which rows should be reviewed, but users still need to manually extract those rows from the full dataset.

Current limitation:

```text
quarantine_candidates exists inside diagnostic reports
but there is no dedicated candidate export
and no dedicated CSV of rows to review
```

Expected future behavior:

```text
normal cleaned CSV still exists
optional quarantine_candidates.json exists
optional quarantine_rows.csv exists
optional accepted_rows.csv exists
```

---

## Architectural Layer

This plan belongs mainly to:

```text
17_Report_Export
14_Output_Serialization_Layer
10_Constraint_Validation_Layer
Pipeline Orchestration Layer
```

Main module areas:

```text
data_processor/exporters/
data_processor/reports/
data_processor/core/
scripts/
docs/
tests/
```

Rules:

```text
Quarantine export must be explicit.
Default CSV export must not change.
Exporters must not mutate table rows.
Exporters must preserve row indexes.
Quarantine export should use existing quarantine_candidates data.
```

---

# Stage A — Current Quarantine Candidate Review

## Goal

Document the current quarantine candidate behavior and export gap.

Expected files to inspect:

```text
data_processor/reports/quarantine_candidates.py
data_processor/reports/diagnostic_bundle.py
data_processor/core/pipeline.py
```

## Expected Files

```text
docs/design/current_quarantine_candidate_behavior.md
log_protocol/11_CSV_quarantine_export/001_current_quarantine_behavior_review.md
```

## Acceptance Criteria

- Current candidate-only behavior is documented.
- Export gap is documented.
- Default no-removal policy is documented.
- No production code change is required in this stage.

---

# Stage B — Quarantine Export Policy Design

## Goal

Define explicit export modes and safety rules.

Suggested output types:

```text
quarantine_candidates.json
quarantine_rows.csv
accepted_rows.csv
```

Suggested policy:

```text
candidate JSON export = safe report export
quarantine rows CSV export = explicit review export
accepted rows CSV export = explicit split export
normal cleaned CSV remains unchanged by default
```

## Expected Files

```text
docs/design/quarantine_export_modes.md
log_protocol/11_CSV_quarantine_export/002_quarantine_export_policy.md
```

## Acceptance Criteria

- Export modes are documented.
- Default behavior is unchanged.
- Row-removal risks are documented.
- Split export is explicit.

---

# Stage C — Quarantine Candidate JSON Exporter

## Goal

Add an exporter that writes only the quarantine candidate section to JSON.

Possible file:

```text
data_processor/exporters/quarantine_json_exporter.py
```

Matching docs:

```text
data_processor/exporters/quarantine_json_exporter.md
```

Possible function:

```python
export_quarantine_candidates_to_json(
    quarantine_candidates,
    output_path,
)
```

## Expected Files

```text
data_processor/exporters/quarantine_json_exporter.py
data_processor/exporters/quarantine_json_exporter.md
tests/test_quarantine_json_exporter.py
tests/test_quarantine_json_exporter.md
log_protocol/11_CSV_quarantine_export/003_quarantine_candidate_json_exporter.md
```

## Acceptance Criteria

- Writes UTF-8 JSON file.
- Creates parent directories.
- Exports only quarantine candidate report data.
- Does not mutate diagnostic data.
- Tests verify exported JSON shape.

---

# Stage D — Quarantine Row Selection Utility

## Goal

Add a utility that separates table rows by quarantine candidate row indexes.

Possible file:

```text
data_processor/reports/quarantine_row_selection.py
```

Matching docs:

```text
data_processor/reports/quarantine_row_selection.md
```

Possible functions:

```python
get_quarantine_row_indexes(quarantine_candidates)
select_quarantine_rows(table, quarantine_candidates)
select_accepted_rows(table, quarantine_candidates)
```

## Expected Files

```text
data_processor/reports/quarantine_row_selection.py
data_processor/reports/quarantine_row_selection.md
tests/test_quarantine_row_selection.py
tests/test_quarantine_row_selection.md
log_protocol/11_CSV_quarantine_export/004_quarantine_row_selection.md
```

## Acceptance Criteria

- Extracts candidate row indexes.
- Selects quarantine rows without mutating the original table.
- Selects accepted rows without mutating the original table.
- Preserves schema/column order where applicable.
- Tests cover empty candidates and multiple candidates.

---

# Stage E — Quarantine Rows CSV Export

## Goal

Export quarantine rows to a separate CSV file when explicitly requested.

Possible pipeline parameter:

```python
quarantine_rows_path=None
```

Expected files:

```text
data_processor/core/pipeline.py
data_processor/core/pipeline.md
tests/test_pipeline.py
tests/test_pipeline.md
log_protocol/11_CSV_quarantine_export/005_quarantine_rows_csv_export.md
```

## Acceptance Criteria

- `quarantine_rows_path` defaults to `None`.
- No quarantine rows CSV is written unless path is provided.
- Existing cleaned CSV still includes all rows.
- Quarantine rows CSV includes only candidate rows.
- Tests verify file creation and row contents.

---

# Stage F — Accepted Rows CSV Export

## Goal

Export accepted rows to a separate CSV file when explicitly requested.

Possible pipeline parameter:

```python
accepted_rows_path=None
```

Expected files:

```text
data_processor/core/pipeline.py
data_processor/core/pipeline.md
tests/test_pipeline.py
tests/test_pipeline.md
log_protocol/11_CSV_quarantine_export/006_accepted_rows_csv_export.md
```

## Acceptance Criteria

- `accepted_rows_path` defaults to `None`.
- No accepted rows CSV is written unless path is provided.
- Accepted rows CSV excludes quarantine candidate rows.
- Normal cleaned CSV remains unchanged.
- Tests verify split behavior.

---

# Stage G — Pipeline Candidate JSON Export Integration

## Goal

Allow the pipeline to optionally export quarantine candidate JSON.

Possible pipeline parameter:

```python
quarantine_candidates_path=None
```

Expected files:

```text
data_processor/core/pipeline.py
data_processor/core/pipeline.md
tests/test_pipeline.py
tests/test_pipeline.md
log_protocol/11_CSV_quarantine_export/007_pipeline_candidate_json_export.md
```

## Acceptance Criteria

- `quarantine_candidates_path` defaults to `None`.
- Candidate JSON export happens only when path is provided.
- JSON report behavior remains unchanged.
- HTML report behavior remains unchanged.
- CSV export behavior remains unchanged.

---

# Stage H — CLI Quarantine Export Options

## Goal

Add CLI support for explicit quarantine exports.

Expected options:

```text
--quarantine-candidates-path
--quarantine-rows-path
--accepted-rows-path
```

Expected files:

```text
scripts/run_csv_pipeline.py
scripts/run_csv_pipeline.md
tests/test_cli_quarantine_export.py
tests/test_cli_quarantine_export.md
log_protocol/11_CSV_quarantine_export/008_cli_quarantine_export_options.md
```

## Acceptance Criteria

- CLI accepts all three optional paths.
- CLI passes paths to pipeline.
- CLI prints export paths when provided.
- Existing CLI behavior remains unchanged.
- Tests verify exported files are created.

---

# Stage I — User Guide Update

## Goal

Update user documentation to explain quarantine export workflow.

Expected files:

```text
docs/user_guides/run_csv_pipeline_example.md
docs/user_guides/csv_diagnostic_report.md
docs/user_guides/csv_report_interpretation.md
log_protocol/11_CSV_quarantine_export/009_user_guide_update.md
```

## Acceptance Criteria

- User guide shows quarantine export command.
- Documentation explains difference between cleaned CSV, quarantine rows CSV, and accepted rows CSV.
- Documentation clearly says normal cleaned CSV still includes all rows by default.

---

# Stage J — Example Workflow Update

## Goal

Update the example workflow test to verify quarantine export outputs.

Expected files:

```text
tests/test_example_csv_workflow.py
tests/test_example_csv_workflow.md
log_protocol/11_CSV_quarantine_export/010_example_workflow_update.md
```

## Acceptance Criteria

- Example workflow writes quarantine candidate JSON.
- Example workflow writes quarantine rows CSV.
- Example workflow writes accepted rows CSV.
- Existing cleaned CSV, JSON report, and HTML report outputs still work.

---

## Out Of Scope

This plan does not include:

```text
automatic row deletion
changing default cleaned CSV contents
interactive review UI
manual approval workflow
database quarantine tables
HTML quarantine-only report
new validation rules
new quarantine candidate sources
strict policy changes
```

---

## Recommended Implementation Order

```text
Stage A — Current Quarantine Candidate Review
Stage B — Quarantine Export Policy Design
Stage C — Quarantine Candidate JSON Exporter
Stage D — Quarantine Row Selection Utility
Stage E — Quarantine Rows CSV Export
Stage F — Accepted Rows CSV Export
Stage G — Pipeline Candidate JSON Export Integration
Stage H — CLI Quarantine Export Options
Stage I — User Guide Update
Stage J — Example Workflow Update
```

---

## Required Protocol Folder

When active, use:

```text
log_protocol/11_CSV_quarantine_export/
```

Protocol files:

```text
001_current_quarantine_behavior_review.md
002_quarantine_export_policy.md
003_quarantine_candidate_json_exporter.md
004_quarantine_row_selection.md
005_quarantine_rows_csv_export.md
006_accepted_rows_csv_export.md
007_pipeline_candidate_json_export.md
008_cli_quarantine_export_options.md
009_user_guide_update.md
010_example_workflow_update.md
999_plan_completion.md
```

---

## Activation Rule

This plan is not active until the user explicitly confirms:

```text
Start 11_CSV_quarantine_export
```

Until then, continue only with the currently active confirmed plan.
