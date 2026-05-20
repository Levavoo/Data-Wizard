# Protocol — Stage F Expected Diagnostics and Quarantine Tests

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/15_CSV_real_world_test_suite.md` |
| Stage | Stage F — Expected Diagnostics and Quarantine Tests |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Diagnostics/quarantine tests and documentation |

---

## Purpose

Test that dirty rows and problematic values appear in diagnostics and review outputs for the heavy real-world CSV fixture.

---

## Fixture

```text
tests/fixtures/csv/real_world_messy_customers_heavy.csv
```

---

## Constraints

```text
tests/fixtures/csv/real_world_messy_customers_constraints.json
```

---

## Test Added

```text
tests/test_real_world_quarantine_and_diagnostics.py
```

Documentation:

```text
tests/test_real_world_quarantine_and_diagnostics.md
```

---

## Covered Expectations

```text
validation report has failures
type diagnostics are present
representative problematic columns are diagnosed
row classification finds suspicious rows
summary/footer-like rows are surfaced somewhere in diagnostics
quarantine candidates exist
quarantine candidate JSON export is written
quarantine rows CSV export is written
accepted rows CSV export is written
JSON report includes expected diagnostic sections
HTML report includes expected diagnostic sections
```

---

## Intentionally Avoided

```text
exact validation failure count
exact quarantine candidate count
exact suspicious row count
exact type diagnostic item count
```

---

## Important Decision

The tests use representative assertions.

Reason:

```text
the heavy fixture contains malformed and ambiguous data, and exact counts may change when diagnostics improve
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `tests/test_real_world_quarantine_and_diagnostics.py` | Created | Adds diagnostics and quarantine export tests for the heavy fixture. |
| `tests/test_real_world_quarantine_and_diagnostics.md` | Created | Documents Stage F test coverage and assertion policy. |
| `log_protocol/15_CSV_real_world_test_suite/006_quarantine_and_diagnostics_tests.md` | Created | Records Stage F completion. |

---

## Recommended Local Test Command

```bash
python -m pytest tests/test_real_world_quarantine_and_diagnostics.py
```

---

## Test Execution Status

```text
Not executed by assistant in this environment.
```

---

## Next Stage

```text
Stage G — Weakness Report Update
```
