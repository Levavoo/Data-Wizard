# Protocol — Stage C Performance Fixture Generator

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/16_CSV_performance_layer.md` |
| Stage | Stage C — Performance Fixture Generator |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Performance fixture generator and documentation |

---

## Purpose

Create a reproducible CSV fixture generator for performance tests.

---

## Script Added

```text
scripts/performance/generate_csv_performance_fixture.py
```

Documentation:

```text
scripts/performance/generate_csv_performance_fixture.md
```

---

## Generator Features

```text
configurable row count
deterministic output
customer-like columns
controlled dirty values
comma or custom delimiter support
optional UTF-8 BOM
writes to data/performance by default
```

---

## Artifact Policy

Generated CSV files are not intended to be committed by default.

Recommended generated location:

```text
data/performance/
```

---

## Example Command

```powershell
python scripts\performance\generate_csv_performance_fixture.py `
    --rows 10000 `
    --output-path data\performance\csv_performance_10000.csv
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `scripts/performance/generate_csv_performance_fixture.py` | Created | Generates deterministic performance CSV fixtures. |
| `scripts/performance/generate_csv_performance_fixture.md` | Created | Documents generator usage and artifact policy. |
| `log_protocol/16_CSV_performance_layer/003_fixture_generator.md` | Created | Records Stage C completion. |

---

## Test Execution Status

```text
Not executed by assistant in this environment.
```

---

## Next Stage

```text
Stage D — Baseline Performance Runner
```
