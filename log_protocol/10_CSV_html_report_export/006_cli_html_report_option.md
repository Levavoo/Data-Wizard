# Protocol — Stage F CLI HTML Report Option

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/10_CSV_html_report_export.md` |
| Stage | Stage F — CLI HTML Report Option |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | CLI integration, tests, documentation |

---

## Purpose

Add CLI support for HTML diagnostic report export.

---

## CLI Option Added

```text
--html-report-path
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `scripts/run_csv_pipeline.py` | Modified | Adds `--html-report-path` argument and passes it to the pipeline. |
| `scripts/run_csv_pipeline.md` | Modified | Documents HTML report CLI usage. |
| `tests/test_cli_html_report.py` | Created | Tests CLI HTML report export. |
| `tests/test_cli_html_report.md` | Created | Documents CLI HTML report tests. |
| `log_protocol/10_CSV_html_report_export/006_cli_html_report_option.md` | Created | Records Stage F completion. |

---

## Behavior Added

```text
CLI can write HTML report
CLI prints HTML report path
HTML report works with strict mode
```

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_cli_html_report.py
```

Status:

```text
Not executed by assistant in this environment.
```
