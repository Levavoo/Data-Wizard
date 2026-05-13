# Protocol — Stage G Example Workflow Update

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/08_CSV_quarantine_candidates.md` |
| Stage | Stage G — Example Workflow Update |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | User guides and example workflow test |

---

## Purpose

Update the existing example workflow so users can see quarantine candidates in the report.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/user_guides/csv_diagnostic_report.md` | Modified | Adds quarantine candidate section. |
| `docs/user_guides/csv_report_interpretation.md` | Modified | Adds interpretation guidance for candidates. |
| `tests/test_example_csv_workflow.py` | Modified | Verifies example workflow produces candidates. |
| `tests/test_example_csv_workflow.md` | Modified | Documents example workflow candidate checks. |
| `log_protocol/08_CSV_quarantine_candidates/007_example_workflow_update.md` | Created | Records Stage G completion. |

---

## Behavior Verified

```text
example workflow report includes quarantine_candidates
candidate_count > 0
error candidates exist
warning candidates exist
```

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_example_csv_workflow.py
```

Status:

```text
Not executed by assistant in this environment.
```
