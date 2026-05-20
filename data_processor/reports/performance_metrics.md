# performance_metrics.py

## Purpose

`performance_metrics.py` provides optional timing helpers for pipeline performance measurement.

---

## Main Class

### `PerformanceTimer`

Collects named duration measurements.

---

## Example

```python
from data_processor.reports.performance_metrics import PerformanceTimer

performance_timer = PerformanceTimer()

with performance_timer.measure("adapter_read_seconds"):
    table = adapter.read()

metrics = performance_timer.to_dict()
```

---

## Design Rules

Timing collection must be optional.

It should not:

```text
change pipeline behavior
change output data
run unless requested
add runtime gates
```
