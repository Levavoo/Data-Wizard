# Mixed-Type Casting Policy

## Purpose

This document defines whether mixed-type diagnostics should change casting behavior.

---

## Decision

Mixed-type diagnostics are report-only for now.

Recommended policy:

```text
Option 1: diagnostics only, no casting change
```

---

## Reason

Automatically casting valid values while preserving or quarantining invalid values changes dataset mutation behavior.

That should wait until these systems exist:

```text
row quarantine
cleaning profiles
column-specific casting policies
issue report export
```

---

## Current Behavior

Mixed-type diagnostics report invalid values, but they do not:

- change schema inference
- cast valid values
- remove invalid values
- quarantine rows

---

## Future Options

### Option 2 — Cast valid values and preserve invalid values

Useful for flexible cleaning, but may create mixed Python types in one column.

### Option 3 — Cast valid values and quarantine invalid rows

Useful for strict migration workflows, but requires quarantine support.

---

## Architecture Rule

Casting should remain schema-driven until a dedicated policy layer exists.
