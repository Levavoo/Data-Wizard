# Protocol — Stage F Performance Smoke Test

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/16_CSV_performance_layer.md` |
| Stage | Stage F — Performance Smoke Test |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Performance smoke test and documentation |

---

## Purpose

Add a lightweight performance smoke test that verifies scripts work without enforcing speed thresholds.

---

## Test Added

```text
tests/performance/test_csv_performance_smoke.py
```

Documentation:

```text
tests/performance/test_csv_performance_smoke.md
```

---

## Covered Behavior

```text
fixture generator creates a tiny CSV file
controlled dirty values are present
baseline runner writes metrics JSON
metrics include row count
metrics include column count
metrics include runtime seconds
metrics include rows per second
metrics include selected output flags
```

---

## Assertion Policy

No runtime thresholds are enforced.

Reason:

```text
runtime varies by machine and CI environment
Stage 16 initially measures performance instead of gating it
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `tests/performance/test_csv_performance_smoke.py` | Created | Adds tiny smoke test for performance tooling. |
| `tests/performance/test_csv_performance_smoke.md` | Created | Documents smoke test behavior and assertion policy. |
| `log_protocol/16_CSV_performance_layer/006_performance_smoke_test.md` | Created | Records Stage F completion. |

---

## Recommended Local Test Command

```bash
python -m pytest tests/performance/test_csv_performance_smoke.py
```

---

## Test Execution Status

```text
Not executed by assistant in this environment.
```

---

## Next Stage

```text
Stage G — Pipeline Timing Hooks
```
