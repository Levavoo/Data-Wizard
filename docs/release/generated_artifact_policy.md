# Generated Artifact Policy

## Purpose

This document defines which files created by CSV verification, reporting, and performance workflows should remain uncommitted.

Plan:

```text
docs/plan_stages/17_CSV_core_stabilization_and_release_readiness.md
```

---

## Core Rule

Generated outputs should not be committed by default.

Commit source files, tests, docs, configs, and fixtures.

Do not commit reproducible processing outputs unless a future golden-snapshot stage explicitly requires them.

---

## Usually Commit

```text
source code
unit tests
integration tests
small source fixtures
constraint/config examples
documentation
plan stages
protocol logs
```

---

## Usually Do Not Commit

```text
cleaned CSV outputs
JSON diagnostic reports
HTML diagnostic reports
quarantine candidate exports
quarantine rows exports
accepted rows exports
performance generated fixtures
performance metrics reports
performance output comparisons
```

---

## `data/processed/` Policy

Files in `data/processed/` are generated pipeline outputs.

Examples:

```text
data/processed/*_clean.csv
data/processed/*_report.json
data/processed/*_report.html
data/processed/*_quarantine_candidates.json
data/processed/*_quarantine_rows.csv
data/processed/*_accepted_rows.csv
```

Policy:

```text
do not commit by default
regenerate locally when needed
remove before merge if accidentally tracked/untracked
```

---

## `data/performance/` Policy

Files in `data/performance/` are generated performance artifacts.

Examples:

```text
data/performance/*.csv
data/performance/*.json
data/performance/*.html
data/performance/output_modes*/
```

Policy:

```text
do not commit by default
metrics are machine-dependent
fixtures are reproducible from scripts/performance/
```

---

## Real-World CSV Generated Outputs

The real-world fixture is committed:

```text
tests/fixtures/csv/real_world_messy_customers_heavy.csv
```

The real-world generated outputs should not be committed by default:

```text
data/processed/real_world_messy_customers_clean.csv
data/processed/real_world_messy_customers_report.json
data/processed/real_world_messy_customers_report.html
data/processed/real_world_messy_customers_quarantine_candidates.json
data/processed/real_world_messy_customers_quarantine_rows.csv
data/processed/real_world_messy_customers_accepted_rows.csv
```

---

## Performance Generated Outputs

Performance scripts should generate files under:

```text
data/performance/
```

These outputs should remain local.

Reason:

```text
metrics depend on machine and environment
large generated CSV files bloat the repository
outputs are reproducible
```

---

## Before Commit / PR Checklist

Run:

```powershell
git status
```

Review generated files.

If generated files appear and should not be committed:

```powershell
git restore <tracked-file>
Remove-Item <untracked-generated-file>
```

For folders:

```powershell
Remove-Item data\processed\* -Recurse -Force
Remove-Item data\performance\* -Recurse -Force
```

Use deletion carefully and only when those folders contain generated files.

---

## Future Golden Snapshot Exception

A future stage may introduce committed expected output snapshots.

Possible future stage:

```text
CSV_golden_snapshot_policy
```

If that happens, snapshots must be:

```text
small
intentional
documented
stable
reviewed
```

Until then, generated outputs remain uncommitted by default.
