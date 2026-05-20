# Protocol — Stage D Expected Parser Diagnostics Tests

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/15_CSV_real_world_test_suite.md` |
| Stage | Stage D — Expected Parser Diagnostics Tests |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Parser diagnostics tests and documentation |

---

## Purpose

Add focused assertions for stable parser-level expectations on the heavy real-world CSV fixture.

---

## Fixture

```text
tests/fixtures/csv/real_world_messy_customers_heavy.csv
```

---

## Test Added

```text
tests/test_real_world_parser_diagnostics.py
```

Documentation:

```text
tests/test_real_world_parser_diagnostics.md
```

---

## Covered Expectations

```text
UTF-8 BOM is detected as utf-8-sig
semicolon delimiter is detected
header row index is 4
preamble row count is 4
duplicate Email header is detected
schema normalizes duplicate headers into email and email_2
extra field diagnostics exist
missing field diagnostics exist
metadata rows are preserved as preamble metadata
```

---

## Intentionally Avoided

```text
exact malformed quote recovery behavior
exact extra field row list
exact missing field row list
exact total row count
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `tests/test_real_world_parser_diagnostics.py` | Created | Adds focused parser diagnostics checks for the heavy fixture. |
| `tests/test_real_world_parser_diagnostics.md` | Created | Documents parser diagnostics test coverage and assertion policy. |
| `log_protocol/15_CSV_real_world_test_suite/004_parser_diagnostics_tests.md` | Created | Records Stage D completion. |

---

## Recommended Local Test Command

```bash
python -m pytest tests/test_real_world_parser_diagnostics.py
```

---

## Test Execution Status

```text
Not executed by assistant in this environment.
```

---

## Next Stage

```text
Stage E — Expected Cleaning and Preservation Tests
```
