# test_csv_performance_smoke.py

## Purpose

Tests that CSV performance tooling works on tiny generated fixtures.

This is a smoke test, not a benchmark.

---

## Tested Files

```text
scripts/performance/generate_csv_performance_fixture.py
scripts/performance/run_csv_performance_baseline.py
```

---

## Covered Behavior

```text
fixture generator creates a small CSV file
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

This test does not enforce speed thresholds.

Reason:

```text
runtime varies by machine and CI environment
Stage 16 initially measures performance instead of gating it
```

---

## Run Test

```bash
python -m pytest tests/performance/test_csv_performance_smoke.py
```

---

## Design Rule

Keep this test tiny and stable.

Real performance measurements should be run through explicit scripts, not normal correctness tests.
