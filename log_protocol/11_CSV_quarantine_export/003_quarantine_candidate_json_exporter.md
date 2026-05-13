# Protocol — Stage C Quarantine Candidate JSON Exporter

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/11_CSV_quarantine_export.md` |
| Stage | Stage C — Quarantine Candidate JSON Exporter |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Exporter, tests, documentation |

---

## Purpose

Add an exporter that writes only the quarantine candidate section to JSON.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `data_processor/exporters/quarantine_json_exporter.py` | Created | Writes quarantine candidate report data to JSON. |
| `data_processor/exporters/quarantine_json_exporter.md` | Created | Documents exporter behavior. |
| `tests/test_quarantine_json_exporter.py` | Created | Tests JSON export behavior. |
| `tests/test_quarantine_json_exporter.md` | Created | Documents exporter tests. |
| `log_protocol/11_CSV_quarantine_export/003_quarantine_candidate_json_exporter.md` | Created | Records Stage C completion. |

---

## Behavior Added

```text
writes UTF-8 JSON
creates parent directories
preserves quarantine candidate report shape
```

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_quarantine_json_exporter.py
```

Status:

```text
Not executed by assistant in this environment.
```
