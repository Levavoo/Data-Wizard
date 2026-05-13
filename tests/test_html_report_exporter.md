# test_html_report_exporter.py

## Purpose

Tests HTML report file export.

---

## Tested File

```text
data_processor/exporters/html_report_exporter.py
```

---

## Covered Behavior

- writes HTML file
- writes UTF-8 text
- creates parent directories

---

## Run Tests

```bash
python -m pytest tests/test_html_report_exporter.py
```

---

## Design Rule

Exporter tests should verify file writing only.

Rendering belongs to `test_html_report.py`.
