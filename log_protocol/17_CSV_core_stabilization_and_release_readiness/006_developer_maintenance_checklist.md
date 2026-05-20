# Protocol — Stage F Developer Maintenance Checklist

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/17_CSV_core_stabilization_and_release_readiness.md` |
| Stage | Stage F — Developer Maintenance Checklist |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Release readiness documentation |

---

## Purpose

Document developer rules before new adapter work.

---

## Document Added

```text
docs/release/csv_core_developer_maintenance_checklist.md
```

---

## Checklist Covers

```text
atomic file rule
matching .md documentation rule
test documentation rule
protocol logging rule
adapter boundary rules
pipeline compatibility rules
diagnostics rules
generated artifact rules
test strategy rules
future JSON adapter rules
future Excel adapter rules
GUI readiness rules
release-before-scaling rule
```

---

## Important Decision

Future JSON/Excel work should start from adapter-specific plan files and should not bypass the established documentation/test/protocol pattern.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/release/csv_core_developer_maintenance_checklist.md` | Created | Documents development rules before scaling to new formats. |
| `log_protocol/17_CSV_core_stabilization_and_release_readiness/006_developer_maintenance_checklist.md` | Created | Records Stage F completion. |

---

## Next Stage

```text
Stage G — Merge Readiness Report
```
