# CSV Core Stabilization and Release Readiness Plan

## Status

```text
Active
```

This plan consolidates the CSV pipeline before adding new adapters such as JSON or Excel.

---

## Purpose

The CSV core has grown significantly through stages 01-16.

Before scaling to additional formats, the project needs a stabilization and release-readiness pass.

Goal:

```text
verify current CSV behavior
fix remaining test failures
confirm CLI/config/report workflows
review generated artifact policy
prepare a clean merge/release checkpoint
record known limitations honestly
```

---

## Why This Stage Comes Before JSON/Excel

New adapters should reuse the same core systems:

```text
Table
Schema
Pipeline
Validation
Diagnostics
Reports
Quarantine exports
Performance metrics
Config/profile behavior
```

If the CSV core is unstable, JSON and Excel adapters will inherit unclear behavior.

---

## Out Of Scope

This stage does not add:

```text
JSON adapter
Excel adapter
GUI/web interface
streaming rewrite
new cleaning semantics
new validator types
large architectural refactor
```

This stage is about stabilization, verification, and release readiness.

---

# Stage A — Current Branch and Scope Review

## Goal

Document current branch scope and what is included since the last stable master checkpoint.

Expected files:

```text
docs/release/csv_core_current_branch_scope.md
log_protocol/17_CSV_core_stabilization_and_release_readiness/001_current_branch_scope.md
```

Acceptance criteria:

- Branch delta is summarized.
- Major completed stages are listed.
- New systems are grouped by capability.
- No code changes required.

---

# Stage B — Verification Command Checklist

## Goal

Create a clear checklist for local verification before merge/release.

Expected files:

```text
docs/release/csv_core_verification_checklist.md
log_protocol/17_CSV_core_stabilization_and_release_readiness/002_verification_checklist.md
```

Checklist should include:

```text
full pytest
targeted CSV suites
real-world suite
performance smoke tests
CLI commands
config-file commands
report generation commands
quarantine export commands
performance baseline commands
```

Acceptance criteria:

- Commands are copy-pasteable in PowerShell.
- Commands distinguish required vs optional checks.
- Generated artifact locations are documented.

---

# Stage C — Generated Artifact Policy Review

## Goal

Confirm which outputs should stay uncommitted.

Expected files:

```text
docs/release/generated_artifact_policy.md
log_protocol/17_CSV_core_stabilization_and_release_readiness/003_generated_artifact_policy.md
```

Acceptance criteria:

- `data/processed/` policy is documented.
- `data/performance/` policy is documented.
- Real-world generated outputs are documented as reproducible artifacts.
- Performance generated outputs are documented as reproducible artifacts.

---

# Stage D — Known Limitations Summary

## Goal

Create one release-facing limitations document.

Expected files:

```text
docs/release/csv_core_known_limitations.md
log_protocol/17_CSV_core_stabilization_and_release_readiness/004_known_limitations_summary.md
```

Acceptance criteria:

- Limitations from real-world suite are summarized.
- Performance limitations are summarized.
- Future stages are listed.
- No false claims of full dirty-data support.

---

# Stage E — User Workflow Readiness Guide

## Goal

Document the current end-to-end user workflow.

Expected files:

```text
docs/release/csv_user_workflow_readiness.md
log_protocol/17_CSV_core_stabilization_and_release_readiness/005_user_workflow_readiness.md
```

Guide should cover:

```text
basic CSV cleaning
config-file pipeline
profiles
constraints
JSON report
HTML report
quarantine exports
strict mode
real-world messy CSV run
performance baseline run
```

Acceptance criteria:

- User workflow is clear.
- Commands are PowerShell-friendly.
- Outputs are explained.

---

# Stage F — Developer Maintenance Checklist

## Goal

Document developer rules before new adapter work.

Expected files:

```text
docs/release/csv_core_developer_maintenance_checklist.md
log_protocol/17_CSV_core_stabilization_and_release_readiness/006_developer_maintenance_checklist.md
```

Checklist should include:

```text
atomic file rule
matching .md documentation rule
test documentation rule
protocol logging rule
artifact policy
adapter boundary rules
pipeline compatibility rules
```

Acceptance criteria:

- Future JSON/Excel work has clear rules.
- Adapter responsibilities are separated from cleaning/validation.
- Pipeline compatibility expectations are documented.

---

# Stage G — Merge Readiness Report

## Goal

Create final merge-readiness report for the CSV core.

Expected files:

```text
docs/release/csv_core_merge_readiness_report.md
log_protocol/17_CSV_core_stabilization_and_release_readiness/007_merge_readiness_report.md
```

Report should include:

```text
what is ready
what must be verified locally
what remains known limitation
recommended PR/merge command
recommended next stages
```

Acceptance criteria:

- Clearly says whether code was executed by assistant or must be run locally.
- Lists exact local commands.
- Recommends next stage order.

---

# Stage H — Plan Completion Record

## Goal

Record completion of Stage 17.

Expected file:

```text
log_protocol/17_CSV_core_stabilization_and_release_readiness/999_plan_completion.md
```

Acceptance criteria:

- Stage list is summarized.
- Next recommended stage is documented.
- No generated artifacts are committed.

---

## Recommended Implementation Order

```text
Stage A — Current Branch and Scope Review
Stage B — Verification Command Checklist
Stage C — Generated Artifact Policy Review
Stage D — Known Limitations Summary
Stage E — User Workflow Readiness Guide
Stage F — Developer Maintenance Checklist
Stage G — Merge Readiness Report
Stage H — Plan Completion Record
```

---

## Required Protocol Folder

```text
log_protocol/17_CSV_core_stabilization_and_release_readiness/
```

Protocol files:

```text
001_current_branch_scope.md
002_verification_checklist.md
003_generated_artifact_policy.md
004_known_limitations_summary.md
005_user_workflow_readiness.md
006_developer_maintenance_checklist.md
007_merge_readiness_report.md
999_plan_completion.md
```
