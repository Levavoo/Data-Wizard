# Current Report Export Behavior

## Purpose

This document records the report export behavior before and during HTML report export support.

---

## Existing JSON Export

Existing module:

```text
data_processor/exporters/json_report_exporter.py
```

Behavior:

```text
accepts report dictionary
creates parent directories
writes UTF-8 JSON
uses JSON-safe serialization for selected non-native values
```

---

## HTML Export Placement

HTML export is added beside JSON export.

Architecture:

```text
Diagnostic Bundle
→ JSON Exporter
→ report.json

Diagnostic Bundle + Pipeline Status
→ HTML Renderer
→ HTML Exporter
→ report.html
```

---

## Design Decision

HTML export must be optional.

Existing calls without `html_report_path` continue to work.

---

## Design Rule

Report exporters only serialize data.

They must not clean, validate, infer, or mutate table rows.
