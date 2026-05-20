# Protocol — Stage E Baseline Metrics Report Format

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/16_CSV_performance_layer.md` |
| Stage | Stage E — Baseline Metrics Report Format |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Metrics schema documentation |

---

## Purpose

Define a stable metrics report format.

---

## Document Added

```text
docs/performance/csv_performance_metrics_format.md
```

---

## Metrics Format Includes

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

## Artifact Policy

Generated metrics JSON files are artifacts and should not be committed by default.

Default output example:

```text
data/performance/csv_performance_baseline.json
```

---

## Future Extensions

Possible future fields:

```text
python_version
platform
commit_sha
peak_memory_mb
step_timings
constraint_count
quarantine_candidate_count
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/performance/csv_performance_metrics_format.md` | Created | Documents baseline metrics JSON format. |
| `log_protocol/16_CSV_performance_layer/005_metrics_report_format.md` | Created | Records Stage E completion. |

---

## Next Stage

```text
Stage F — Performance Smoke Test
```
