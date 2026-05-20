# Protocol — Stage B Verification Command Checklist

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/17_CSV_core_stabilization_and_release_readiness.md` |
| Stage | Stage B — Verification Command Checklist |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Release readiness documentation |

---

## Purpose

Create a clear checklist for local verification before merge/release.

---

## Document Added

```text
docs/release/csv_core_verification_checklist.md
```

---

## Required Checks Covered

```text
full pytest
real-world CSV suite
performance smoke tests
pipeline timing tests
basic CLI workflow
config workflow
full report/quarantine CLI workflow
```

---

## Optional Checks Covered

```text
performance baseline
output mode comparison
semicolon detection example
```

---

## Important Decision

Generated verification outputs are documented as local artifacts.

Default generated areas:

```text
data/processed/
data/performance/
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/release/csv_core_verification_checklist.md` | Created | Provides local release verification commands. |
| `log_protocol/17_CSV_core_stabilization_and_release_readiness/002_verification_checklist.md` | Created | Records Stage B completion. |

---

## Next Stage

```text
Stage C — Generated Artifact Policy Review
```
