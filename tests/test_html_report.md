# test_html_report.py

## Purpose

Tests the static HTML diagnostic report renderer.

---

## Tested File

```text
data_processor/reports/html_report.py
```

---

## Covered Behavior

- returns complete HTML document
- includes expected report sections
- includes optional pipeline status
- escapes HTML-like data values

---

## Run Tests

```bash
python -m pytest tests/test_html_report.py
```

---

## Design Rule

Renderer tests should verify HTML content and escaping.

They should not test file writing.
