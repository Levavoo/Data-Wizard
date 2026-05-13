# test_cli_html_report.py

## Purpose

Tests CLI HTML report export behavior.

---

## Tested File

```text
scripts/run_csv_pipeline.py
```

---

## Covered Behavior

- CLI accepts `--html-report-path`
- CLI writes HTML report
- CLI HTML report works with strict mode
- strict policy failure can still write HTML report

---

## Run Tests

```bash
python -m pytest tests/test_cli_html_report.py
```

---

## Design Rule

CLI tests verify argument wiring and output files.

Detailed HTML rendering behavior belongs to `test_html_report.py`.
