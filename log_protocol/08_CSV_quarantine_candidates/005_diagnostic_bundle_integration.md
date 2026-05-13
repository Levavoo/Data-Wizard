# Protocol — Stage E Diagnostic Bundle Integration

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/08_CSV_quarantine_candidates.md` |
| Stage | Stage E — Diagnostic Bundle Integration |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Diagnostic bundle integration, tests, documentation |

---

## Purpose

Expose quarantine candidates in the diagnostic bundle.

---

## Bundle Section Added

```text
quarantine_candidates
```

Includes:

```text
candidate_count
summary
candidates
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `data_processor/reports/diagnostic_bundle.py` | Modified | Adds quarantine candidate report section. |
| `data_processor/reports/diagnostic_bundle.md` | Modified | Documents quarantine candidate section. |
| `tests/test_diagnostic_bundle.py` | Modified | Verifies candidate section. |
| `log_protocol/08_CSV_quarantine_candidates/005_diagnostic_bundle_integration.md` | Created | Records Stage E completion. |

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_diagnostic_bundle.py
```

Status:

```text
Not executed by assistant in this environment.
```
