# Protocol — Stage B Constraint Config for Real-World Fixture

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/15_CSV_real_world_test_suite.md` |
| Stage | Stage B — Constraint Config for Real-World Fixture |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Fixture constraint config and documentation |

---

## Purpose

Create constraints used for the heavy messy customer fixture.

---

## Fixture

```text
tests/fixtures/csv/real_world_messy_customers_heavy.csv
```

---

## Constraint Config

Created:

```text
tests/fixtures/csv/real_world_messy_customers_constraints.json
```

Documented:

```text
tests/fixtures/csv/real_world_messy_customers_constraints.md
```

---

## Constraints Added

```text
customer_id required
customer_id unique
email required
email regex
email unique
country required
country allowed values
amount min_value 0
score min_value 0
score max_value 100
```

---

## Intentionally Deferred

```text
phone validation
postal code validation
signup_date required/date range
active allowed values
notes safety/spreadsheet injection rule
secondary email validation
country normalization database
```

---

## Important Decision

No tests were added in this stage.

Reason:

```text
Stage B only defines the validation policy for later observation and test stages.
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `tests/fixtures/csv/real_world_messy_customers_constraints.json` | Created | Provides validation constraints for the heavy fixture. |
| `tests/fixtures/csv/real_world_messy_customers_constraints.md` | Created | Documents each constraint and expected purpose. |
| `log_protocol/15_CSV_real_world_test_suite/002_real_world_constraint_config.md` | Created | Records Stage B completion. |

---

## Next Stage

```text
Stage C — Baseline Observation Script/Test
```
