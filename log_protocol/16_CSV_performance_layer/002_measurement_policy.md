# Protocol — Stage B Performance Measurement Policy

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/16_CSV_performance_layer.md` |
| Stage | Stage B — Performance Measurement Policy |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Performance policy documentation |

---

## Purpose

Define how performance should be measured.

---

## Document Added

```text
docs/performance/csv_performance_measurement_policy.md
```

---

## Covered Policy Areas

```text
baseline metrics
input sizes
output modes
runtime thresholds
memory measurement
generated artifact policy
CI policy
interpretation policy
optimization policy
```

---

## Important Decisions

```text
normal correctness tests should not become runtime-gated
performance tools should be opt-in at first
thresholds are advisory until baseline metrics exist
generated performance artifacts should not be committed by default
optimization must not silently reduce diagnostics or correctness
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/performance/csv_performance_measurement_policy.md` | Created | Defines performance measurement policy and artifact policy. |
| `log_protocol/16_CSV_performance_layer/002_measurement_policy.md` | Created | Records Stage B completion. |

---

## Next Stage

```text
Stage C — Performance Fixture Generator
```
