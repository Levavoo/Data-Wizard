# Profile Output Path Policy

## Purpose

This document defines how cleaning profiles interact with output paths.

---

## Current Policy

Profiles can recommend output types.

Profiles do not generate output paths automatically in this stage.

---

## Reason

Automatic path generation can create unexpected files.

This project currently prefers explicit user-controlled output paths.

---

## Current Behavior

Example:

```text
--profile migration_audit
```

selects workflow intent and defaults, but does not automatically create:

```text
report.json
report.html
quarantine_candidates.json
quarantine_rows.csv
accepted_rows.csv
```

Users must still provide explicit paths:

```text
--report-path
--html-report-path
--quarantine-candidates-path
--quarantine-rows-path
--accepted-rows-path
```

---

## Future Policy Option

A future config-file stage may support:

```text
--output-dir data/processed
```

and generate paths from profile defaults.

---

## Design Rule

Profiles must not silently create files without explicit user paths.
