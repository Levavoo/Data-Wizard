# CSV Core Current Branch Scope

## Purpose

This document summarizes the current `codex` branch scope before release/merge readiness review.

Plan:

```text
docs/plan_stages/17_CSV_core_stabilization_and_release_readiness.md
```

---

## Branch Context

At the start of Stage 17, `codex` contained a large set of CSV core improvements after the previous master checkpoint.

Observed branch status from repository comparison:

```text
codex ahead of master by approximately 192 commits
codex behind master by 0 commits
```

This means the current CSV work exists on `codex` and should be verified before merge/release.

---

## Major Capability Groups Added

### Quarantine Exports

Added capabilities:

```text
quarantine candidate JSON export
quarantine rows CSV export
accepted rows CSV export
CLI options for quarantine exports
pipeline integration for quarantine exports
```

Main areas:

```text
data_processor/exporters/
data_processor/reports/
scripts/run_csv_pipeline.py
tests/
docs/design/
docs/user_guides/
```

---

### Cleaning Profiles

Added capabilities:

```text
built-in cleaning profiles
profile resolver
CLI --profile option
profile documentation
profile tests
```

Main areas:

```text
data_processor/config/
scripts/run_csv_pipeline.py
docs/user_guides/csv_cleaning_profiles.md
```

---

### Config File Pipeline

Added capabilities:

```text
JSON pipeline config loader
config validation
config resolver
CLI --config support
CLI override policy
example config files
config user guide
```

Main areas:

```text
data_processor/config/pipeline_config.py
data_processor/config/pipeline_config_resolver.py
scripts/run_csv_pipeline.py
examples/csv/
docs/user_guides/csv_pipeline_config_files.md
```

---

### Encoding and Delimiter Detection

Added capabilities:

```text
encoding detection utility
delimiter detection utility
adapter detection integration
parse diagnostics detection section
pipeline detection options
config detection options
CLI detection options
```

Main areas:

```text
data_processor/adapters/encoding_detection.py
data_processor/adapters/delimiter_detection.py
data_processor/adapters/csv_adapter.py
data_processor/adapters/parse_diagnostics.py
```

---

### Real-World CSV Test Suite

Added capabilities:

```text
heavy messy CSV fixture
real-world constraint config
expected outcome report
baseline observation test
parser diagnostics tests
cleaning/preservation tests
diagnostics/quarantine tests
observed weakness report
real-world test guide
```

Main areas:

```text
tests/fixtures/csv/real_world_messy_customers_heavy.csv
docs/testing/
tests/test_real_world_*.py
```

---

### Performance Layer

Added capabilities:

```text
performance fixture generator
baseline performance runner
metrics format documentation
performance smoke test
optional pipeline step timings
output mode comparison runner
performance guide
```

Main areas:

```text
scripts/performance/
docs/performance/
data_processor/reports/performance_metrics.py
data_processor/core/pipeline.py
tests/performance/
```

---

## Core Files Changed Significantly

Important core files changed or expanded:

```text
data_processor/adapters/csv_adapter.py
data_processor/adapters/parse_diagnostics.py
data_processor/core/pipeline.py
scripts/run_csv_pipeline.py
```

These should be included in focused review before release.

---

## Documentation Growth

New documentation areas:

```text
docs/design/
docs/user_guides/
docs/testing/
docs/performance/
docs/plan_stages/
log_protocol/
```

This is useful, but release readiness should ensure users can find the most important guides.

---

## Test Growth

New test categories:

```text
unit tests for config/profile/detection utilities
CLI tests
pipeline tests
real-world messy CSV tests
performance smoke tests
```

Before merge/release, run:

```text
full pytest
real-world suite
performance smoke tests
```

---

## Release Readiness Risk Areas

Current risk areas:

```text
large branch delta
many new docs and protocols
possible stale test assumptions
performance scripts not yet locally verified by assistant
real-world generated artifacts should remain uncommitted
adapter/pipeline API compatibility must be preserved
```

---

## Scope Boundary

This branch does not yet include:

```text
JSON adapter
Excel adapter
GUI/web interface
streaming pipeline rewrite
spreadsheet injection hardening
semantic text column policy
large-file stress-test gate
```

These belong to future stages after stabilization.
