# Protocol — Stage J Performance Layer Guide

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/16_CSV_performance_layer.md` |
| Stage | Stage J — Performance Layer Guide |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Performance layer guide documentation |

---

## Purpose

Document how to run performance tools and interpret results.

---

## Guide Added

```text
docs/performance/csv_performance_layer_guide.md
```

---

## Guide Covers

```text
fixture generator usage
baseline runner usage
output mode comparison usage
optional pipeline step timings
performance smoke test
artifact policy
result interpretation
future optimization decision process
recommended local workflow
future improvement candidates
```

---

## Important Decision

Generated performance artifacts remain local/uncommitted by default.

Reason:

```text
metrics are machine-dependent
large generated files bloat the repository
artifacts are reproducible from scripts
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/performance/csv_performance_layer_guide.md` | Created | Explains how to run and interpret the performance layer. |
| `log_protocol/16_CSV_performance_layer/010_performance_layer_guide.md` | Created | Records Stage J completion. |

---

## Recommended Local Commands

```bash
python -m pytest tests/performance/test_csv_performance_smoke.py
python scripts/performance/run_csv_performance_baseline.py --rows 10000 --json-report --html-report
python scripts/performance/run_csv_output_mode_comparison.py --rows 10000 --output-dir data/performance/output_modes_10000
```

---

## Test Execution Status

```text
Not executed by assistant in this environment.
```
