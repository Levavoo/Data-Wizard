# Protocol — Stage G Pipeline Timing Hooks

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/16_CSV_performance_layer.md` |
| Stage | Stage G — Pipeline Timing Hooks |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Optional pipeline timing helper, pipeline integration, tests, documentation |

---

## Purpose

Add optional step timing around major pipeline phases.

---

## Files Added / Modified

```text
data_processor/reports/performance_metrics.py
data_processor/reports/performance_metrics.md
data_processor/core/pipeline.py
tests/test_pipeline_performance_metrics.py
tests/test_pipeline_performance_metrics.md
```

---

## Behavior Added

Pipeline now accepts:

```python
collect_step_timings: bool = False
```

Default behavior:

```text
performance_metrics are omitted
existing callers remain compatible
```

When enabled:

```text
result["performance_metrics"] contains named step durations
```

---

## Timing Fields

Current timing fields include:

```text
adapter_read_seconds
cleaning_seconds
type_inference_first_pass_seconds
type_casting_seconds
type_inference_second_pass_seconds
validation_seconds
quality_report_seconds
diagnostic_bundle_seconds
pipeline_status_seconds
clean_csv_export_seconds
json_report_export_seconds
html_report_export_seconds
quarantine_json_export_seconds
quarantine_rows_export_seconds
accepted_rows_export_seconds
```

---

## Important Decision

Timing is optional and disabled by default.

Reason:

```text
performance diagnostics should not alter normal pipeline output shape unless explicitly requested
```

---

## Tests

Recommended local command:

```bash
python -m pytest tests/test_pipeline_performance_metrics.py
```

Status:

```text
Not executed by assistant in this environment.
```

---

## Next Stage

```text
Stage H — Report Performance Split
```
