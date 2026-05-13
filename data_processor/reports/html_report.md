# html_report.py

## Purpose

`html_report.py` renders a diagnostic bundle as a static, self-contained HTML report.

It belongs to the report layer.

Architecture:

```text
Diagnostic Bundle + optional Pipeline Status
→ HTML Renderer
→ HTML String
```

---

## Main Function

### `render_html_report(diagnostic_bundle, pipeline_status=None)`

Returns a complete HTML document string.

---

## Included Sections

The report currently includes:

```text
Summary
Pipeline Status
Quality Report
Validation Report
Quarantine Candidates
Row Classification
Type Diagnostics
Parse Diagnostics
Metadata
```

---

## Safety

The renderer escapes values using Python's standard library `html.escape`.

This prevents raw data values from being inserted as active HTML.

---

## Styling

The report uses inline CSS.

Current styling goals:

```text
self-contained
static
readable in browser
print-friendly
no JavaScript
no external assets
```

---

## Design Rules

This module must not:

- write files
- mutate diagnostic data
- change diagnostic bundle shape
- depend on external CSS or JavaScript

File writing belongs to `html_report_exporter.py`.
