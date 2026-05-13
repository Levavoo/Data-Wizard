# CLI Report Summary Design

## Purpose

This document proposes a future concise CLI summary for CSV pipeline results.

The full diagnostic JSON report should remain the source of truth.

---

## Problem

The current CLI prints full quality and validation report dictionaries.

This can become hard to read as diagnostics grow.

---

## Proposed Summary

Example:

```text
CSV Pipeline Summary
Rows: 25
Columns: 8
Missing values: 4
Mixed-type columns: 1
Suspicious rows: 2
Validation failures: 5
Report: data/processed/customer_migration_report.json
```

---

## Suggested Fields

```text
input file
output file
report file
row count
column count
missing value total
mixed-type column count
suspicious row count
validation failure count
```

---

## Design Rules

The summary should:

- be readable in PowerShell
- show only the most important counts
- point users to the full JSON report
- not replace the diagnostic bundle

The summary should not:

- hide validation failures
- print huge nested dictionaries
- mutate data
- change export behavior

---

## Future Implementation Area

Possible future file:

```text
data_processor/reports/cli_summary.py
```

Possible test file:

```text
tests/test_cli_summary.py
```

---

## Status

Design only.

No implementation is included in the current plan.
