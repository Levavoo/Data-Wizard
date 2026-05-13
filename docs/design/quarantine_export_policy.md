# Quarantine Export Policy

## Purpose

This document defines future quarantine export behavior.

Current implementation only reports quarantine candidates inside the diagnostic bundle.

---

## Current Policy

```text
candidate report only
```

Current behavior:

```text
rows remain in cleaned CSV
rows remain in table
quarantine candidates are included in report JSON
no separate quarantine export is written
```

---

## Future Output Options

Possible future outputs:

```text
cleaned CSV with all rows
quarantine_candidates.json
quarantine_rows.csv
accepted_rows.csv
```

---

## Future Modes

Possible modes:

```text
report_only
export_candidates
split_clean_and_quarantine
strict_fail_on_error_candidates
```

---

## Recommended Future Default

```text
report_only
```

Reason:

```text
avoid silent data loss
require explicit user decision before excluding rows
```

---

## Design Rule

Quarantine export must be explicit.

No future implementation should silently remove rows from the normal CSV export without a clear option or policy.
