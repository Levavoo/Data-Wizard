# CSV Performance Measurement Policy

## Purpose

This document defines how CSV pipeline performance should be measured.

Plan:

```text
docs/plan_stages/16_CSV_performance_layer.md
```

---

## Core Policy

Performance measurement must be explicit and reproducible.

Normal correctness tests should not become fragile because of runtime variability.

---

## What To Measure

Baseline metrics:

```text
row_count
column_count
input_file_size_bytes
runtime_seconds
rows_per_second
output_file_size_bytes
report_file_size_bytes
status
selected output modes
```

Optional metrics:

```text
peak_memory_mb
step timings
HTML report size
quarantine candidate count
accepted/quarantine row counts
```

---

## Input Sizes

Suggested generated fixture sizes:

```text
small: 1,000 rows
medium: 10,000 rows
large-local: 100,000 rows
stress-local: 1,000,000 rows
```

Policy:

```text
small and medium are suitable for routine local checks
large-local is for manual performance review
stress-local is optional and should not run automatically
```

---

## Output Modes

Measure output modes separately:

```text
clean CSV only
clean CSV + JSON report
clean CSV + HTML report
clean CSV + quarantine exports
full output mode
```

Reason:

```text
reporting and quarantine exports may dominate runtime for larger files
```

---

## Runtime Thresholds

Initial thresholds should be advisory.

Policy:

```text
do not fail normal CI based on runtime at first
record metrics before setting gates
only add thresholds after baseline behavior is known
```

---

## Memory Measurement

Memory measurement is useful but optional at first.

Reason:

```text
cross-platform memory measurement can be inconsistent
simple runtime metrics are easier to establish first
```

Future memory options:

```text
tracemalloc
resource module where available
psutil if dependency policy allows it later
```

---

## Generated Artifact Policy

Generated performance files should not be committed by default.

Examples:

```text
data/performance/*.csv
data/performance/*.json
data/generated/*.csv
```

Reason:

```text
large files bloat the repository
metrics vary by machine
fixtures are reproducible from generator scripts
```

Commit:

```text
generator scripts
runner scripts
documentation
small code tests
```

Do not commit by default:

```text
generated CSV performance fixtures
generated benchmark reports
generated HTML reports
```

---

## CI Policy

Performance tools should be opt-in at first.

Normal CI can run only lightweight smoke tests if they are stable.

Recommended split:

```text
normal pytest: correctness tests
performance smoke: validates tooling only
manual performance command: measures runtime
future optional CI workflow: scheduled or manual benchmark
```

---

## Interpretation Policy

Performance metrics must be interpreted with context:

```text
machine CPU
disk speed
Python version
OS
row count
column count
output mode
report mode
```

A single slow run should not automatically trigger optimization.

Look for:

```text
consistent bottlenecks
large regressions
specific expensive stages
scaling problems as row count increases
```

---

## Optimization Policy

Optimization must not silently reduce correctness or diagnostics.

If an optimization changes output behavior, it must be treated as a correctness change and tested separately.

Allowed optimization examples:

```text
avoid repeated full-table passes where safe
avoid unnecessary report construction when report is not requested
make expensive diagnostics optional by profile/config
cache reusable intermediate results
```

Not allowed without explicit design:

```text
skip validation silently
truncate diagnostics silently
drop rows silently
change parsing behavior silently
```
