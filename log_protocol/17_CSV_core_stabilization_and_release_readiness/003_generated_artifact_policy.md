# Protocol — Stage C Generated Artifact Policy Review

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/17_CSV_core_stabilization_and_release_readiness.md` |
| Stage | Stage C — Generated Artifact Policy Review |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Release readiness documentation |

---

## Purpose

Confirm which outputs should stay uncommitted.

---

## Document Added

```text
docs/release/generated_artifact_policy.md
```

---

## Policy Summary

Usually commit:

```text
source code
tests
small source fixtures
configs
documentation
protocol logs
```

Usually do not commit:

```text
data/processed generated outputs
data/performance generated outputs
JSON diagnostic reports
HTML reports
quarantine exports
performance metrics
```

---

## Important Decision

Generated outputs remain reproducible local artifacts by default.

A future golden snapshot stage may define exceptions.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/release/generated_artifact_policy.md` | Created | Defines generated output policy before merge/release. |
| `log_protocol/17_CSV_core_stabilization_and_release_readiness/003_generated_artifact_policy.md` | Created | Records Stage C completion. |

---

## Next Stage

```text
Stage D — Known Limitations Summary
```
