# Protocol — Stage E User Workflow Readiness Guide

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/17_CSV_core_stabilization_and_release_readiness.md` |
| Stage | Stage E — User Workflow Readiness Guide |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Release readiness documentation |

---

## Purpose

Document the current end-to-end user workflow.

---

## Document Added

```text
docs/release/csv_user_workflow_readiness.md
```

---

## Workflows Covered

```text
basic CSV cleaning
cleaning with profile
config file pipeline
constraint validation
JSON diagnostic report
HTML diagnostic report
quarantine exports
full real-world diagnostic run
strict mode
encoding/delimiter controls
performance baseline
output mode performance comparison
```

---

## Output Policy

Generated outputs are directed to:

```text
data/processed/
data/performance/
```

and should not be committed by default.

---

## Important Decision

This stage documents current workflows only.

It does not add new user-facing features.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/release/csv_user_workflow_readiness.md` | Created | Documents release-ready CLI workflows. |
| `log_protocol/17_CSV_core_stabilization_and_release_readiness/005_user_workflow_readiness.md` | Created | Records Stage E completion. |

---

## Next Stage

```text
Stage F — Developer Maintenance Checklist
```
