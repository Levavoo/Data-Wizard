# Suspicious Row Quarantine Policy

## Purpose

This document defines whether suspicious row classification should affect row removal, quarantine, or export behavior.

---

## Decision

Suspicious row classification is diagnostics-only for now.

Current policy:

```text
diagnostics only, no row removal
```

---

## Reason

Automatic row removal can cause silent data loss.

Rows should only be removed or quarantined when a dedicated quarantine model and explicit user-facing policy exist.

---

## Current Behavior

Suspicious rows are:

```text
classified
reported in diagnostic bundle
kept in the table
kept in CSV export
```

Suspicious rows are not:

```text
removed
quarantined
repaired
excluded from export
```

---

## Future Options

### Option 2 — Optional exclude from export

The user could choose to exclude suspicious rows when exporting.

### Option 3 — Quarantine candidate export

Suspicious rows could be exported to a separate issue/quarantine file.

### Option 4 — Automatic quarantine

Not recommended until rules are configurable and auditable.

---

## Architecture Rule

Row classification should remain separate from quarantine and export behavior.
