# Current Pipeline Status Behavior

## Purpose

This document records the pipeline and CLI behavior before strict-mode status handling.

---

## Previous Default Behavior

The CSV pipeline reported issues but did not produce a structured status object.

Behavior:

```text
pipeline returned table, quality report, validation results, and diagnostic bundle
CSV export still ran when diagnostics contained validation failures
CLI process exited normally when execution succeeded
```

---

## Missing Before This Plan

Missing behavior:

```text
pipeline_status object
strict_mode flag
strict policy failure status
formal CLI exit code 2 for policy failure
```

---

## Current Decision

Default behavior remains non-strict.

Strict mode is opt-in.

---

## Design Rule

Policy failures are different from execution failures.

```text
policy failure = data processed, but serious diagnostics were found
execution failure = command could not complete successfully
```
