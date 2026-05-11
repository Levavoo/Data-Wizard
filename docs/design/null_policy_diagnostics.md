# Null Policy Diagnostics

## Purpose

This document defines future diagnostic requirements for configurable null-token policies.

Diagnostics should make profile-driven value changes auditable.

---

## Why Diagnostics Are Needed

When a cleaning profile changes values to `None`, users need to know what changed and why.

Without diagnostics, profile-driven cleaning can become silent data loss.

---

## Proposed Diagnostic Shape

```python
{
    "null_policy_diagnostics": {
        "profile": "strict_migration",
        "changed_values": {
            "email": {
                "unknown": 4,
                "missing": 2
            }
        },
        "preserved_values": {
            "status": {
                "unknown": 5
            }
        }
    }
}
```

---

## Required Fields

### `profile`

Name of the active cleaning profile.

---

### `changed_values`

Counts tokens converted to `None`, grouped by column.

---

### `preserved_values`

Counts ambiguous tokens explicitly preserved by policy, grouped by column.

---

## Design Rules

Diagnostics should:

- be machine-readable
- be grouped by column
- preserve the original token text where possible
- explain profile-driven changes
- support audit review

Diagnostics should not:

- mutate values
- replace validation reports
- duplicate full dataset rows

---

## Future Placement

Possible future placement:

```text
diagnostic_bundle["null_policy_diagnostics"]
```

or:

```text
diagnostic_bundle["cleaning_diagnostics"]["null_policy"]
```

Final placement should be decided when cleaning profiles are implemented.
