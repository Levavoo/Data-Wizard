# Protocol — Stage E Expected Cleaning and Preservation Tests

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/15_CSV_real_world_test_suite.md` |
| Stage | Stage E — Expected Cleaning and Preservation Tests |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Cleaning/preservation tests and documentation |

---

## Purpose

Test what should be normalized and what should remain unchanged for the heavy real-world CSV fixture.

---

## Fixture

```text
tests/fixtures/csv/real_world_messy_customers_heavy.csv
```

---

## Test Added

```text
tests/test_real_world_cleaning_preservation.py
```

Documentation:

```text
tests/test_real_world_cleaning_preservation.md
```

---

## Covered Expectations

```text
leading/trailing whitespace is trimmed
repeated internal whitespace is collapsed
multiline quoted notes are preserved
escaped quote text is preserved
quoted delimiter characters inside notes are preserved
Unicode text is preserved
emoji text is preserved
formula-like text remains text
HTML-like text remains text
phone values remain text-like values
```

---

## Intentionally Avoided

```text
validation failure counts
quarantine candidate counts
all numeric normalization behavior
all date normalization behavior
malformed quote recovery behavior
spreadsheet injection escaping
HTML sanitization
```

---

## Important Decision

The risky text preservation test does not claim spreadsheet injection hardening is solved.

It only verifies that the pipeline does not execute or reinterpret risky strings.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `tests/test_real_world_cleaning_preservation.py` | Created | Adds safe cleaning and preservation tests for the heavy fixture. |
| `tests/test_real_world_cleaning_preservation.md` | Created | Documents Stage E test coverage and assertion policy. |
| `log_protocol/15_CSV_real_world_test_suite/005_cleaning_and_preservation_tests.md` | Created | Records Stage E completion. |

---

## Recommended Local Test Command

```bash
python -m pytest tests/test_real_world_cleaning_preservation.py
```

---

## Test Execution Status

```text
Not executed by assistant in this environment.
```

---

## Next Stage

```text
Stage F — Expected Diagnostics and Quarantine Tests
```
