# html_report_exporter.py

## Purpose

`html_report_exporter.py` writes rendered HTML report strings to disk.

It belongs to the exporter layer.

Architecture:

```text
HTML Report String
→ HTML Exporter
→ UTF-8 HTML File
```

---

## Main Function

### `export_report_to_html(html_report, output_path, encoding="utf-8")`

Writes an HTML report string to the requested file path.

---

## Behavior

The exporter:

```text
creates parent directories
writes UTF-8 text
preserves the rendered HTML string
```

---

## Design Rules

This module must not:

- render HTML
- mutate diagnostic data
- parse CSV files
- build diagnostic reports

Rendering belongs to:

```text
data_processor/reports/html_report.py
```
