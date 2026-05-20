# Protocol — Stage C Baseline Observation Script/Test

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/15_CSV_real_world_test_suite.md` |
| Stage | Stage C — Baseline Observation Script/Test |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Baseline observation test and documentation |

---

## Purpose

Run the current pipeline against the heavy fixture and capture observed behavior without pretending everything is correct.

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
tests/test_real_world_messy_csv_observation.py
```

Documentation:

```text
tests/test_real_world_messy_csv_observation.md
```

---

## Assertion Policy

This baseline test intentionally uses broad assertions.

It verifies:

```text
pipeline completes
outputs are generated
diagnostic sections exist
parse detection diagnostics exist
semicolon delimiter is detected
UTF-8 BOM encoding is detected
metadata-before-header is detected
validation failures exist
quarantine candidates exist
```

It intentionally avoids:

```text
exact row counts
exact validation failure counts
exact quarantine candidate counts
exact malformed quote behavior
exact extra/missing field counts
```

---

## Important Decision

The test should reveal current behavior and weaknesses.

It should not hide dirty-data issues by pretending the fixture is fully solved.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `tests/test_real_world_messy_csv_observation.py` | Created | Adds baseline observation coverage for the heavy CSV fixture. |
| `tests/test_real_world_messy_csv_observation.md` | Created | Documents broad observation test policy. |
| `log_protocol/15_CSV_real_world_test_suite/003_baseline_observation_test.md` | Created | Records Stage C completion. |

---

## Recommended Local Test Command

```bash
python -m pytest tests/test_real_world_messy_csv_observation.py
```

---

## Test Execution Status

```text
Not executed by assistant in this environment.
```

---

## Next Stage

```text
Stage D — Expected Parser Diagnostics Tests
```
