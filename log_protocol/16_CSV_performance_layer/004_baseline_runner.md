# Protocol — Stage D Baseline Performance Runner

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/16_CSV_performance_layer.md` |
| Stage | Stage D — Baseline Performance Runner |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Baseline runner and documentation |

---

## Purpose

Create a script that runs the current pipeline on generated fixtures and records runtime metrics.

---

## Script Added

```text
scripts/performance/run_csv_performance_baseline.py
```

Documentation:

```text
scripts/performance/run_csv_performance_baseline.md
```

---

## Metrics Recorded

```text
scenario
row_count
column_count
input_file_size_bytes
output_file_size_bytes
runtime_seconds
rows_per_second
pipeline_status
outputs
artifact_sizes
fixture
```

---

## Output Modes Supported

```text
clean CSV only
clean CSV + JSON report
clean CSV + HTML report
clean CSV + quarantine exports
```

---

## Artifact Policy

Generated metrics and generated fixtures are not intended to be committed by default.

Default artifact folder:

```text
data/performance/
```

---

## Example Command

```powershell
python scripts\performance\run_csv_performance_baseline.py `
    --rows 10000 `
    --json-report `
    --html-report
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `scripts/performance/run_csv_performance_baseline.py` | Created | Generates fixture, runs pipeline, writes metrics. |
| `scripts/performance/run_csv_performance_baseline.md` | Created | Documents runner usage and metrics. |
| `log_protocol/16_CSV_performance_layer/004_baseline_runner.md` | Created | Records Stage D completion. |

---

## Test Execution Status

```text
Not executed by assistant in this environment.
```

---

## Next Stage

```text
Stage E — Baseline Metrics Report Format
```
