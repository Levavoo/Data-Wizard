# Protocol — Stage F Pipeline Integration Check

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/08_CSV_quarantine_candidates.md` |
| Stage | Stage F — Pipeline Integration Check |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Pipeline tests and documentation |

---

## Purpose

Verify quarantine candidates work through the normal CSV pipeline.

---

## Behavior Verified

```text
pipeline diagnostic bundle includes quarantine_candidates
validation failures produce error candidates
suspicious rows produce warning candidates
rows remain in cleaned table
CSV export still runs
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `tests/test_pipeline.py` | Modified | Adds pipeline quarantine candidate test. |
| `tests/test_pipeline.md` | Modified | Documents pipeline quarantine candidate coverage. |
| `log_protocol/08_CSV_quarantine_candidates/006_pipeline_integration_check.md` | Created | Records Stage F completion. |

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_pipeline.py
python -m pytest
```

Status:

```text
Not executed by assistant in this environment.
```
