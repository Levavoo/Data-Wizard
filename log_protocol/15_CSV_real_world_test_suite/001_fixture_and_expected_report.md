# Protocol — Stage A Fixture and Expected Report Review

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/15_CSV_real_world_test_suite.md` |
| Stage | Stage A — Fixture and Expected Report Review |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Fixture review and expected outcome documentation |

---

## Purpose

Review the heavy fixture and write a human expected outcome report before adding assertions.

---

## Fixture

```text
tests/fixtures/csv/real_world_messy_customers_heavy.csv
```

The fixture was created before activating this plan and includes:

```text
metadata before header
UTF-8 BOM
semicolon delimiter
duplicate headers
extra fields
missing fields
multiline quoted fields
escaped quotes
broken quote area
mixed number/date/boolean formats
invalid emails
duplicate IDs
missing values
risky text values
summary/footer rows
```

---

## Expected Report

Created:

```text
docs/testing/real_world_messy_customers_expected_report.md
```

The report documents:

```text
expected parser diagnostics
expected cleaning behavior
expected type diagnostics
expected validation behavior
expected quarantine behavior
expected preserved values
expected weaknesses
initial testing strategy
```

---

## Important Decision

No test assertions were added in this stage.

Reason:

```text
expected behavior must be documented before actual testing begins
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/testing/real_world_messy_customers_expected_report.md` | Created | Defines expected outcomes before tests. |
| `log_protocol/15_CSV_real_world_test_suite/001_fixture_and_expected_report.md` | Created | Records Stage A completion. |

---

## Next Stage

```text
Stage B — Constraint Config for Real-World Fixture
```
