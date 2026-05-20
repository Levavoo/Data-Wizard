# Protocol — Stage G Weakness Report Update

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/15_CSV_real_world_test_suite.md` |
| Stage | Stage G — Weakness Report Update |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Observed weakness documentation |

---

## Purpose

After running Stage 15 tests, update the expected report with observed weaknesses and current limitations.

---

## Weakness Report Added

```text
docs/testing/real_world_messy_customers_observed_weaknesses.md
```

---

## Observations Recorded

```text
sparse metadata rows initially broke header detection
multiline note newlines are collapsed by text cleaning
fixture duplicate email columns can shift test expectations
diagnostic report shapes differed from early test assumptions
accepted rows export may be header-only for very dirty fixtures
unbalanced quote diagnosis remains weak
leading-zero preservation remains a concern
currency, percent, and text amounts need better diagnostics
Excel serial dates are likely unsupported
German boolean tokens may be unsupported
spreadsheet injection hardening is not solved
HTML-like text is not sanitized
extra fields are detected but not preserved as data
summary/footer rows are flagged but not removed
```

---

## Processed Output Policy

The report documents that the real messy CSV should be run through the pipeline during local testing and CI.

Generated processed files should usually remain uncommitted:

```text
data/processed/real_world_messy_customers_clean.csv
data/processed/real_world_messy_customers_report.json
data/processed/real_world_messy_customers_report.html
data/processed/real_world_messy_customers_quarantine_candidates.json
data/processed/real_world_messy_customers_quarantine_rows.csv
data/processed/real_world_messy_customers_accepted_rows.csv
```

Reason:

```text
processed outputs are reproducible artifacts
outputs may change when diagnostics improve
committing generated outputs would add repository noise
```

---

## Important Decision

No generated processed CSV/report output was committed in this stage.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/testing/real_world_messy_customers_observed_weaknesses.md` | Created | Records observed weaknesses and future improvement candidates. |
| `log_protocol/15_CSV_real_world_test_suite/007_observed_weakness_report.md` | Created | Records Stage G completion. |

---

## Next Stage

```text
Stage H — Real-World Test Guide
```
