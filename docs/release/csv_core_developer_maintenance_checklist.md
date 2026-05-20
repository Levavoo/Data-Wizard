# CSV Core Developer Maintenance Checklist

## Purpose

This checklist defines developer rules before continuing with new adapters or major CSV pipeline changes.

Plan:

```text
docs/plan_stages/17_CSV_core_stabilization_and_release_readiness.md
```

---

## Atomic File Rule

Every new code file should have a matching documentation file.

Example:

```text
data_processor/adapters/json_adapter.py
data_processor/adapters/json_adapter.md
```

---

## Test Documentation Rule

Every new test file should have a matching `.md` explanation file.

Example:

```text
tests/test_json_adapter.py
tests/test_json_adapter.md
```

---

## Protocol Logging Rule

Every planned stage should record protocol logs under:

```text
log_protocol/<stage_name>/
```

Protocol logs should explain:

```text
what changed
why it changed
which files changed
what tests should be run
what was not executed by assistant if applicable
```

---

## Adapter Boundary Rules

Adapters should only handle source parsing and conversion into the internal model.

Adapters should not perform:

```text
cleaning
constraint validation
type inference
report generation
quarantine candidate generation
business-specific transformations
```

Adapter responsibilities:

```text
validate source file
parse source format
create Table
create Schema
attach source metadata
attach parse/source diagnostics where useful
```

---

## Pipeline Compatibility Rule

New pipeline options must be backward-compatible.

Rules:

```text
new parameters should have safe defaults
existing calls should keep working
new optional output should be omitted unless requested
CLI changes should not break existing commands
config changes should reject unknown fields intentionally
```

---

## Diagnostics Rule

Diagnostics should be explicit and serializable.

Rules:

```text
include diagnostics in diagnostic_bundle when relevant
avoid hiding ambiguity
avoid silently truncating diagnostics without policy
use stable field names where possible
update docs when report shape changes
```

---

## Generated Artifact Rule

Generated files should not be committed by default.

Generated areas:

```text
data/processed/
data/performance/
data/generated/
```

Commit generated outputs only if a future golden-snapshot policy explicitly requires it.

---

## Test Strategy Rule

Use layered tests:

```text
unit tests for small utilities
adapter tests for parsing behavior
pipeline tests for integration
CLI tests for user workflows
real-world tests for messy data behavior
performance smoke tests for tooling
```

Avoid:

```text
exact counts for unstable messy diagnostics
runtime thresholds in normal tests
large committed fixtures when a generator can reproduce them
```

---

## Future JSON Adapter Rules

When adding JSON support:

```text
start with JSON plan file
define supported JSON shapes first
separate flat records vs nested records
document flattening policy before implementation
preserve raw path/context diagnostics where possible
avoid business-specific JSON normalization in adapter
```

Recommended first JSON scope:

```text
list of objects
flat object records
simple nested objects only if flattening policy is explicit
```

Avoid initially:

```text
arbitrary deeply nested JSON
multiple incompatible root shapes in one adapter pass
schema inference magic beyond current Table model
```

---

## Future Excel Adapter Rules

When adding Excel support:

```text
start with Excel plan file
define sheet selection policy first
define header row policy first
define formula handling policy first
define date serial behavior first
define merged-cell behavior first
```

Recommended first Excel scope:

```text
single sheet
explicit or first detected header row
cell values only, not formatting
formulas as cached/displayed values if library supports safely
```

Avoid initially:

```text
merged-cell repair
multiple sheet merging
formula execution
format-based semantic inference
hidden row/column policy without documentation
```

---

## GUI Readiness Rule

A GUI should not replace the CLI/config workflow.

Before GUI work, ensure:

```text
CLI is stable
config files are stable
reports are usable
generated artifact paths are clear
pipeline errors are readable
```

Recommended first GUI scope:

```text
local web interface
upload/select file
choose profile/config
run pipeline
view HTML report
download clean/quarantine/accepted outputs
```

---

## Release Before Scaling Rule

Before new formats:

```text
run full pytest
run real-world suite
run performance smoke tests
verify CLI/config examples
git status clean except ignored generated artifacts
merge/release CSV core checkpoint
```

Then start new adapter stages.
