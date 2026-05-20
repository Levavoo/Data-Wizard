# CSV Performance Layer Plan

## Status

```text
Draft — not active until user confirmation.
```

This plan focuses on measuring and improving CSV pipeline performance without changing correctness behavior.

It must not be started automatically.

---

## Purpose

The CSV pipeline now has broad real-world behavior coverage.

The next important layer is performance.

Goal:

```text
measure current runtime and memory behavior
create reproducible performance fixtures
identify bottlenecks
separate performance checks from normal correctness tests
improve performance safely without hiding diagnostics
```

---

## Core Rule

Do not optimize blindly.

First:

```text
measure baseline
record current behavior
identify bottleneck areas
set realistic thresholds
```

Then optimize only where evidence shows a problem.

---

## Current Risk Areas

Potential performance-heavy parts:

```text
CSV parsing
row object creation
null cleaning
text cleaning
number normalization
type inference
type casting
schema metadata inference
quality report generation
row profiling
row classification
mixed-type diagnostics
constraint validation
quarantine candidate generation
JSON report export
HTML report rendering
CSV export
```

---

## Out Of Scope For This Stage

This plan does not include:

```text
streaming/chunked pipeline rewrite
parallel processing
external dataframe libraries
full database-backed processing
Excel adapter
automatic production benchmarking service
cloud performance dashboard
```

Those can be later stages after baseline performance is understood.

---

## Performance Test Policy

Performance tests must be separate from normal correctness tests.

Reason:

```text
performance varies by machine
CI machines may be slower or inconsistent
normal pytest should remain stable and fast
```

Suggested structure:

```text
tests/performance/
scripts/performance/
docs/performance/
```

Performance tests should not fail normal CI unless explicitly enabled.

Possible command style:

```powershell
python scripts\performance\run_csv_performance_baseline.py
```

or later:

```powershell
python -m pytest tests/performance --run-performance
```

---

## Fixture Strategy

Use generated fixtures instead of committing huge files.

Reason:

```text
large CSV fixtures bloat the repository
generated fixtures are reproducible
sizes can be adjusted locally or in CI
```

Suggested generated fixture sizes:

```text
small: 1,000 rows
medium: 10,000 rows
large-local: 100,000 rows
stress-local: 1,000,000 rows, optional only
```

Committed files should include:

```text
fixture generator script
fixture generation docs
small sample if needed
```

Generated files should go to:

```text
data/generated/
data/performance/
```

and should usually not be committed.

---

# Stage A — Current Performance Surface Review

## Goal

Document current pipeline steps and likely performance hotspots.

Expected files:

```text
docs/performance/current_csv_pipeline_performance_surface.md
log_protocol/16_CSV_performance_layer/001_current_performance_surface.md
```

## Acceptance Criteria

- Pipeline stages are listed.
- Potential hotspots are documented.
- Existing output/report behavior is documented.
- No code changes required in this stage.

---

# Stage B — Performance Measurement Policy

## Goal

Define how performance should be measured.

Policy should cover:

```text
runtime measurement
memory measurement if feasible
input sizes
output sizes
which outputs are enabled
machine variability
non-blocking thresholds
local vs CI behavior
```

Expected files:

```text
docs/performance/csv_performance_measurement_policy.md
log_protocol/16_CSV_performance_layer/002_measurement_policy.md
```

## Acceptance Criteria

- Normal tests are not performance-gated.
- Performance tests are explicit opt-in.
- Thresholds are advisory at first.
- Generated artifacts are not committed.

---

# Stage C — Performance Fixture Generator

## Goal

Create a reproducible CSV fixture generator for performance tests.

Possible file:

```text
scripts/performance/generate_csv_performance_fixture.py
```

Matching docs:

```text
scripts/performance/generate_csv_performance_fixture.md
```

Generated fixture characteristics:

```text
configurable row count
stable deterministic output
realistic customer-like columns
some controlled dirty values
optional semicolon/comma delimiter
optional UTF-8/BOM mode
```

Expected files:

```text
scripts/performance/generate_csv_performance_fixture.py
scripts/performance/generate_csv_performance_fixture.md
log_protocol/16_CSV_performance_layer/003_fixture_generator.md
```

## Acceptance Criteria

- Generator can create at least 1,000-row and 10,000-row CSVs.
- Output is deterministic.
- Generated files are written outside tracked fixture folders by default.
- Generator has clear CLI arguments.

---

# Stage D — Baseline Performance Runner

## Goal

Create a script that runs the current pipeline on generated fixtures and records runtime metrics.

Possible file:

```text
scripts/performance/run_csv_performance_baseline.py
```

Matching docs:

```text
scripts/performance/run_csv_performance_baseline.md
```

Metrics:

```text
row_count
column_count
input_file_size_bytes
runtime_seconds
rows_per_second
selected_outputs
status
```

Optional metrics:

```text
peak_memory_mb
report_size_bytes
output_size_bytes
```

Expected files:

```text
scripts/performance/run_csv_performance_baseline.py
scripts/performance/run_csv_performance_baseline.md
log_protocol/16_CSV_performance_layer/004_baseline_runner.md
```

## Acceptance Criteria

- Runner can execute pipeline on a generated fixture.
- Runner writes a JSON metrics file.
- Runner prints a readable summary.
- Runner does not run automatically in normal pytest.

---

# Stage E — Baseline Metrics Report Format

## Goal

Define a stable metrics report format.

Possible output:

```text
data/performance/csv_performance_baseline.json
```

Report shape:

```json
{
  "scenario": "medium_default_reports",
  "row_count": 10000,
  "input_file_size_bytes": 1234567,
  "runtime_seconds": 1.23,
  "rows_per_second": 8130.08,
  "outputs": {
    "clean_csv": true,
    "json_report": true,
    "html_report": false,
    "quarantine_exports": false
  }
}
```

Expected files:

```text
docs/performance/csv_performance_metrics_format.md
log_protocol/16_CSV_performance_layer/005_metrics_report_format.md
```

## Acceptance Criteria

- Metrics format is documented.
- Generated metrics files are treated as artifacts.
- Future comparisons can use the same schema.

---

# Stage F — Performance Smoke Test

## Goal

Add a lightweight performance smoke test that verifies scripts work, without enforcing speed thresholds.

Possible file:

```text
tests/performance/test_csv_performance_smoke.py
```

Important:

```text
should use a small row count
should not be brittle
should not fail based on runtime unless timeout is extreme
should focus on metrics structure
```

Expected files:

```text
tests/performance/test_csv_performance_smoke.py
tests/performance/test_csv_performance_smoke.md
log_protocol/16_CSV_performance_layer/006_performance_smoke_test.md
```

## Acceptance Criteria

- Smoke test verifies fixture generation.
- Smoke test verifies baseline runner creates metrics.
- No strict runtime threshold yet.
- Test is safe for normal suite only if small and stable; otherwise it must be opt-in.

---

# Stage G — Pipeline Timing Hooks

## Goal

Add optional step timing around major pipeline phases.

Possible approach:

```text
internal timing helper
optional collect_step_timings=True parameter
pipeline result includes performance_metrics when enabled
```

Possible fields:

```text
adapter_read_seconds
cleaning_seconds
type_inference_seconds
validation_seconds
quality_report_seconds
diagnostic_bundle_seconds
export_seconds
total_seconds
```

Expected files:

```text
data_processor/reports/performance_metrics.py
data_processor/reports/performance_metrics.md
data_processor/core/pipeline.py
data_processor/core/pipeline.md
tests/test_pipeline_performance_metrics.py
tests/test_pipeline_performance_metrics.md
log_protocol/16_CSV_performance_layer/007_pipeline_timing_hooks.md
```

## Acceptance Criteria

- Timing is optional and disabled by default.
- Existing pipeline calls remain compatible.
- Timing metrics are returned only when requested.
- Tests validate metric presence and non-negative durations.

---

# Stage H — Report Performance Split

## Goal

Measure the cost of different output modes.

Scenarios:

```text
clean CSV only
clean CSV + JSON report
clean CSV + JSON + HTML report
clean CSV + quarantine exports
full output mode
```

Expected files:

```text
docs/performance/csv_output_mode_performance_scenarios.md
scripts/performance/run_csv_output_mode_comparison.py
scripts/performance/run_csv_output_mode_comparison.md
log_protocol/16_CSV_performance_layer/008_output_mode_performance_split.md
```

## Acceptance Criteria

- Output scenarios are documented.
- Script can compare multiple output modes.
- Results are written as JSON artifacts.
- No optimization is made yet unless data supports it.

---

# Stage I — Initial Bottleneck Review

## Goal

Use baseline metrics and timing hooks to document likely bottlenecks.

Expected files:

```text
docs/performance/csv_initial_bottleneck_review.md
log_protocol/16_CSV_performance_layer/009_initial_bottleneck_review.md
```

## Acceptance Criteria

- Bottlenecks are based on metrics, not guesses.
- Each bottleneck has a possible future improvement path.
- No large refactor is hidden inside the review.

---

# Stage J — Performance Layer Guide

## Goal

Document how to run performance tools and interpret results.

Expected files:

```text
docs/performance/csv_performance_layer_guide.md
log_protocol/16_CSV_performance_layer/010_performance_layer_guide.md
```

Guide should explain:

```text
how to generate fixtures
how to run baseline measurement
where outputs are written
which files should not be committed
how to compare output modes
how to read step timings
how to decide future optimizations
```

## Acceptance Criteria

- Developer can run performance layer locally.
- Artifact policy is clear.
- Next optimization candidates are listed.

---

## Recommended Implementation Order

```text
Stage A — Current Performance Surface Review
Stage B — Performance Measurement Policy
Stage C — Performance Fixture Generator
Stage D — Baseline Performance Runner
Stage E — Baseline Metrics Report Format
Stage F — Performance Smoke Test
Stage G — Pipeline Timing Hooks
Stage H — Report Performance Split
Stage I — Initial Bottleneck Review
Stage J — Performance Layer Guide
```

---

## Required Protocol Folder

When active, use:

```text
log_protocol/16_CSV_performance_layer/
```

Protocol files:

```text
001_current_performance_surface.md
002_measurement_policy.md
003_fixture_generator.md
004_baseline_runner.md
005_metrics_report_format.md
006_performance_smoke_test.md
007_pipeline_timing_hooks.md
008_output_mode_performance_split.md
009_initial_bottleneck_review.md
010_performance_layer_guide.md
999_plan_completion.md
```

---

## Activation Rule

This plan is not active until the user explicitly confirms:

```text
Start 16_CSV_performance_layer
```

Until then, continue only with the currently active confirmed plan.
