# CSV HTML Report Export Plan

## Status

```text
Draft — not active until user confirmation.
```

This plan focuses on exporting the existing diagnostic bundle as a readable HTML report.

It must not be started automatically.

---

## Purpose

The CSV pipeline currently supports JSON diagnostic reports.

JSON is machine-readable, but users need a report that is easier to open, scan, and share.

Goal:

```text
CSV diagnostic bundle
→ HTML report renderer
→ optional HTML report export
→ readable browser-based report
```

---

## Current Default Policy

Current behavior must remain unchanged:

```text
CSV export still works
JSON report export still works
HTML report export is optional
no diagnostic behavior changes
no row removal
no strict policy changes
```

---

## Problem

Current diagnostic output is rich but JSON-only.

Current risks:

```text
users struggle to read large JSON reports
important errors are buried in nested structures
non-technical users cannot easily review diagnostics
reports are hard to share visually
```

Expected future behavior:

```text
user runs pipeline with --html-report-path
pipeline writes cleaned CSV
pipeline writes optional JSON report
pipeline writes optional HTML report
HTML report summarizes key sections clearly
```

---

## Architectural Layer

This plan belongs mainly to:

```text
17_Report_Export
14_Output_Serialization_Layer
User Reporting Layer
```

Main module areas:

```text
data_processor/exporters/
data_processor/reports/
scripts/
docs/
tests/
```

Rules:

```text
HTML export must not mutate data.
HTML export must not change diagnostic bundle shape.
HTML export should consume existing diagnostic_bundle only.
HTML export should use standard library only unless explicitly approved.
HTML output should be static and self-contained.
```

---

# Stage A — Current Report Export Review

## Goal

Document current JSON report export behavior and identify how HTML export should fit beside it.

Expected files to inspect:

```text
data_processor/exporters/json_report_exporter.py
data_processor/reports/diagnostic_bundle.py
scripts/run_csv_pipeline.py
```

## Expected Files

```text
docs/design/current_report_export_behavior.md
log_protocol/10_CSV_html_report_export/001_current_report_export_review.md
```

## Acceptance Criteria

- Current JSON export behavior is documented.
- HTML export placement is documented.
- No production code change is required in this stage.

---

# Stage B — HTML Report Structure Design

## Goal

Design the first readable HTML report structure.

Suggested sections:

```text
summary
pipeline status
quality report
validation report
quarantine candidates
row classification
type diagnostics
parse diagnostics
metadata
```

## Expected Files

```text
docs/design/html_report_structure.md
log_protocol/10_CSV_html_report_export/002_html_report_structure.md
```

## Acceptance Criteria

- HTML sections are documented.
- Section order is documented.
- Required fields are documented.
- Large/nested data handling is documented.

---

# Stage C — HTML Report Renderer

## Goal

Add a renderer that converts a diagnostic bundle and optional pipeline status into HTML text.

Possible file:

```text
data_processor/reports/html_report.py
```

Matching docs:

```text
data_processor/reports/html_report.md
```

Possible function:

```python
render_html_report(
    diagnostic_bundle,
    pipeline_status=None,
) -> str
```

## Expected Files

```text
data_processor/reports/html_report.py
data_processor/reports/html_report.md
tests/test_html_report.py
tests/test_html_report.md
log_protocol/10_CSV_html_report_export/003_html_report_renderer.md
```

## Acceptance Criteria

- Renderer returns valid HTML string.
- Renderer escapes user/data values safely.
- Renderer includes summary fields.
- Renderer includes validation report summary.
- Renderer includes quarantine candidate summary.
- Renderer includes pipeline status if provided.
- Renderer does not write files.

---

# Stage D — HTML Report Exporter

## Goal

Add a file exporter for HTML report strings.

Possible file:

```text
data_processor/exporters/html_report_exporter.py
```

Matching docs:

```text
data_processor/exporters/html_report_exporter.md
```

Possible function:

```python
export_report_to_html(
    html_report,
    output_path,
)
```

## Expected Files

```text
data_processor/exporters/html_report_exporter.py
data_processor/exporters/html_report_exporter.md
tests/test_html_report_exporter.py
tests/test_html_report_exporter.md
log_protocol/10_CSV_html_report_export/004_html_report_exporter.md
```

## Acceptance Criteria

- Exports UTF-8 HTML file.
- Creates parent directories if needed.
- Does not modify diagnostic data.
- Tests verify written content.

---

# Stage E — Pipeline HTML Report Integration

## Goal

Allow the pipeline to optionally export an HTML diagnostic report.

Potential signature:

```python
run_csv_pipeline(
    input_path,
    output_path,
    report_path=None,
    html_report_path=None,
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
log_protocol/10_CSV_html_report_export/005_pipeline_html_report_integration.md
```

## Acceptance Criteria

- Existing calls continue to work.
- `html_report_path` defaults to `None`.
- HTML report is exported only when path is provided.
- JSON report behavior remains unchanged.
- CSV export behavior remains unchanged.
- Tests verify HTML report file creation.

---

# Stage F — CLI HTML Report Option

## Goal

Add CLI support for HTML report export.

Expected option:

```text
--html-report-path
```

Expected files:

```text
scripts/run_csv_pipeline.py
scripts/run_csv_pipeline.md
tests/test_cli_html_report.py
tests/test_cli_html_report.md
log_protocol/10_CSV_html_report_export/006_cli_html_report_option.md
```

## Acceptance Criteria

- CLI accepts `--html-report-path`.
- CLI passes path to pipeline.
- CLI prints HTML report path when provided.
- Existing CLI options continue to work.
- Tests verify HTML report creation through CLI.

---

# Stage G — User Guide Update

## Goal

Update user documentation to show HTML report usage.

Expected files:

```text
docs/user_guides/run_csv_pipeline_example.md
docs/user_guides/csv_diagnostic_report.md
docs/user_guides/csv_report_interpretation.md
log_protocol/10_CSV_html_report_export/007_user_guide_update.md
```

## Acceptance Criteria

- User guide shows `--html-report-path` command.
- Diagnostic guide explains JSON vs HTML reports.
- Interpretation guide explains HTML report is for human review.

---

# Stage H — Example Workflow Update

## Goal

Update the example workflow test to verify HTML report export.

Expected files:

```text
tests/test_example_csv_workflow.py
tests/test_example_csv_workflow.md
log_protocol/10_CSV_html_report_export/008_example_workflow_update.md
```

## Acceptance Criteria

- Example workflow writes HTML report.
- HTML report contains expected title/sections.
- Existing JSON and CSV outputs still work.

---

# Stage I — Report Styling Policy

## Goal

Document styling policy for HTML reports.

Suggested initial policy:

```text
static inline CSS
no JavaScript
no external assets
accessible contrast
print-friendly layout
```

Expected files:

```text
docs/design/html_report_styling_policy.md
log_protocol/10_CSV_html_report_export/009_html_report_styling_policy.md
```

## Acceptance Criteria

- Styling policy is documented.
- No external dependency is introduced.
- Report remains self-contained.

---

## Out Of Scope

This plan does not include:

```text
interactive HTML dashboards
JavaScript charts
external CSS frameworks
PDF report export
Excel report export
new diagnostics
row removal
strict policy changes
automatic report opening in browser
```

---

## Recommended Implementation Order

```text
Stage A — Current Report Export Review
Stage B — HTML Report Structure Design
Stage C — HTML Report Renderer
Stage D — HTML Report Exporter
Stage E — Pipeline HTML Report Integration
Stage F — CLI HTML Report Option
Stage G — User Guide Update
Stage H — Example Workflow Update
Stage I — Report Styling Policy
```

---

## Required Protocol Folder

When active, use:

```text
log_protocol/10_CSV_html_report_export/
```

Protocol files:

```text
001_current_report_export_review.md
002_html_report_structure.md
003_html_report_renderer.md
004_html_report_exporter.md
005_pipeline_html_report_integration.md
006_cli_html_report_option.md
007_user_guide_update.md
008_example_workflow_update.md
009_html_report_styling_policy.md
999_plan_completion.md
```

---

## Activation Rule

This plan is not active until the user explicitly confirms:

```text
Start 10_CSV_html_report_export
```

Until then, continue only with the currently active confirmed plan.
