# Protocol — Stage C Quarantine Candidate Builder

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/08_CSV_quarantine_candidates.md` |
| Stage | Stage C — Quarantine Candidate Builder |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Report module, tests, documentation |

---

## Purpose

Add a non-mutating report module that builds quarantine candidates from existing diagnostics.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `data_processor/reports/quarantine_candidates.py` | Created | Builds candidate report data. |
| `data_processor/reports/quarantine_candidates.md` | Created | Documents candidate builder. |
| `tests/test_quarantine_candidates.py` | Created | Tests candidate building behavior. |
| `tests/test_quarantine_candidates.md` | Created | Documents candidate tests. |
| `log_protocol/08_CSV_quarantine_candidates/003_candidate_builder.md` | Created | Records Stage C completion. |

---

## Behavior Added

```text
groups reasons by row index
supports validation failures
supports suspicious rows
supports mixed-type invalid values
preserves diagnostic source
```

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_quarantine_candidates.py
```

Status:

```text
Not executed by assistant in this environment.
```
