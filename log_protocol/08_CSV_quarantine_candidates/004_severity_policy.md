# Protocol — Stage D Severity Policy

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/08_CSV_quarantine_candidates.md` |
| Stage | Stage D — Severity Policy |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Design documentation and deterministic implementation |

---

## Purpose

Define deterministic severity levels for quarantine candidates.

---

## Severity Levels

```text
info
warning
error
```

---

## Initial Mapping

```text
validation failure → error
mixed-type invalid value → warning
suspicious row classification → warning
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/design/quarantine_candidate_severity_policy.md` | Created | Documents severity policy. |
| `data_processor/reports/quarantine_candidates.py` | Created | Implements deterministic severity mapping. |
| `log_protocol/08_CSV_quarantine_candidates/004_severity_policy.md` | Created | Records Stage D completion. |

---

## Production Code Decision

Severity does not block export by default.
