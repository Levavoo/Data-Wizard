# Protocol — Stage H CLI Quarantine Export Options

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/11_CSV_quarantine_export.md` |
| Stage | Stage H — CLI Quarantine Export Options |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | CLI integration, tests, documentation |

---

## Purpose

Add CLI support for explicit quarantine exports.

---

## CLI Options Added

```text
--quarantine-candidates-path
--quarantine-rows-path
--accepted-rows-path
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `scripts/run_csv_pipeline.py` | Modified | Adds quarantine export CLI arguments and passes them to the pipeline. |
| `scripts/run_csv_pipeline.md` | Modified | Documents quarantine export CLI usage. |
| `tests/test_cli_quarantine_export.py` | Created | Tests CLI quarantine export behavior. |
| `tests/test_cli_quarantine_export.md` | Created | Documents CLI quarantine export tests. |
| `log_protocol/11_CSV_quarantine_export/008_cli_quarantine_export_options.md` | Created | Records Stage H completion. |

---

## Behavior Added

```text
CLI can write candidate JSON
CLI can write quarantine rows CSV
CLI can write accepted rows CSV
strict policy failure can still write quarantine exports
```

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_cli_quarantine_export.py
```

Status:

```text
Not executed by assistant in this environment.
```
