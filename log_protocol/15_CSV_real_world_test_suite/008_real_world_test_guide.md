# Protocol — Stage H Real-World Test Guide

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/15_CSV_real_world_test_suite.md` |
| Stage | Stage H — Real-World Test Guide |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Test guide documentation |

---

## Purpose

Document how to run and interpret the real-world CSV test suite.

---

## Guide Added

```text
docs/testing/csv_real_world_test_suite.md
```

---

## Guide Covers

```text
fixture location
constraint config location
expected report location
observed weakness report location
Stage 15 test files
commands to run the real-world suite
command to generate processed outputs locally
processed output policy
how to inspect generated outputs
how to interpret test failures
what the suite should prove
what the suite should not claim
maintenance rules
future improvement stages
```

---

## Processed Output Policy

The guide documents that generated processed files should usually not be committed:

```text
data/processed/*.csv
data/processed/*.json
data/processed/*.html
```

Reason:

```text
they are reproducible artifacts
they may change when diagnostics improve
they add repository noise
```

---

## Important Decision

The real-world suite now has documentation for both:

```text
running tests
generating local processed outputs
```

Generated outputs remain local artifacts by default.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/testing/csv_real_world_test_suite.md` | Created | Explains how to run, inspect, and interpret the real-world suite. |
| `log_protocol/15_CSV_real_world_test_suite/008_real_world_test_guide.md` | Created | Records Stage H completion. |

---

## Next Step

Recommended next action:

```text
run all Stage 15 tests locally and then run the full pytest suite
```
