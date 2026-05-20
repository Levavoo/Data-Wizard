# Protocol — Stage G Pipeline Candidate JSON Export Integration

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/11_CSV_quarantine_export.md` |
| Stage | Stage G — Pipeline Candidate JSON Export Integration |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Pipeline integration, tests, documentation |

---

## Purpose

Allow the pipeline to optionally export quarantine candidate JSON.

---

## Pipeline Parameter Added

```python
quarantine_candidates_path=None
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `data_processor/core/pipeline.py` | Modified | Adds optional quarantine candidate JSON export. |
| `data_processor/core/pipeline.md` | Modified | Documents quarantine candidate JSON export. |
| `tests/test_pipeline.py` | Modified | Verifies candidate JSON output. |
| `log_protocol/11_CSV_quarantine_export/007_pipeline_candidate_json_export.md` | Created | Records Stage G completion. |

---

## Behavior Added

```text
candidate JSON export is written only when path is provided
JSON report behavior remains unchanged
HTML report behavior remains unchanged
CSV export behavior remains unchanged
```

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_pipeline.py
```

Status:

```text
Not executed by assistant in this environment.
```
