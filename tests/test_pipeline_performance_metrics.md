# test_pipeline_performance_metrics.py

## Purpose

Tests optional pipeline step timing behavior.

---

## Tested File

```text
data_processor/core/pipeline.py
```

---

## Covered Behavior

```text
performance_metrics are omitted by default
performance_metrics are returned when collect_step_timings=True
timing values are non-negative
existing pipeline calls remain compatible
```

---

## Run Test

```bash
python -m pytest tests/test_pipeline_performance_metrics.py
```

---

## Design Rule

Pipeline timings are optional diagnostics for performance analysis.

They must not change output correctness behavior.
