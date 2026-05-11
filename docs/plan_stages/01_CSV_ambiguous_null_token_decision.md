# CSV Ambiguous Null Token Decision Plan

## Status

```text
Draft — not active until user confirmation.
```

This plan focuses only on deciding how ambiguous null-like tokens should be handled.

It must not be started automatically.

---

## Purpose

Define a safe policy for ambiguous null-like values such as:

```text
unknown
missing
```

These values often mean missing data in migration files, but they can also be legitimate category values.

Goal:

```text
avoid silent data loss
→ preserve meaningful categories by default
→ prepare configurable null handling for future profiles
```

---

## Architectural Layer

This plan belongs mainly to:

```text
09_Value_Normalization_Layer
13_Canonical_Model_Layer, future profile/config metadata only
```

Rules:

```text
Adapters must not normalize nulls.
Cleaners normalize values.
Default cleaners should be conservative.
Ambiguous behavior should be configurable later.
Validators should not mutate values.
Profilers should not mutate values.
```

---

## Current Behavior

The conservative null-token stage intentionally keeps these values unchanged:

```text
unknown → "unknown"
missing → "missing"
```

This is safer than globally converting them to `None`.

Reason:

```text
unknown and missing can be real domain/category values.
```

Examples:

```csv
status,value
unknown,100
missing,200
```

In this case, changing `unknown` or `missing` to `None` could destroy useful categorical data.

---

# Stage A — Ambiguous Token Policy Decision

## Goal

Document the default policy for ambiguous null-like tokens.

Recommended default:

```text
unknown and missing are preserved by default.
```

They should not be added to global `NULL_VALUES` until configurable cleaning profiles exist.

## Expected Files

```text
docs/design/ambiguous_null_tokens.md
log_protocol/01_CSV_ambiguous_null_token_decision/001_ambiguous_token_policy.md
```

## Acceptance Criteria

- The decision is documented.
- `unknown` and `missing` remain unchanged by default.
- The reason for preserving them is explained.
- Future configurability is described.
- No production code change is required if current tests already verify this behavior.

---

# Stage B — Regression Test Confirmation

## Goal

Ensure ambiguous tokens remain unchanged unless future configuration says otherwise.

Target file:

```text
tests/test_nulls.py
```

Expected tests:

```python
assert normalize_null("unknown") == "unknown"
assert normalize_null("missing") == "missing"
```

If these tests already exist, no code change is needed.

## Expected Files

Possible changes:

```text
tests/test_nulls.py
tests/test_nulls.md
log_protocol/01_CSV_ambiguous_null_token_decision/002_regression_test_confirmation.md
```

## Acceptance Criteria

- Tests confirm ambiguous tokens are preserved.
- Test documentation explains why.
- No adapter, validator, profiler, or exporter changes are made.

---

# Stage C — Future Configurable Policy Draft

## Goal

Design how future cleaning profiles could treat ambiguous tokens differently.

Future examples:

```text
strict migration profile: unknown → None, missing → None
survey profile: unknown remains category
CRM profile: missing → None, unknown remains category
```

Possible configuration shape:

```python
{
    "null_tokens": ["", "null", "n/a", "#N/A"],
    "ambiguous_null_tokens": ["unknown", "missing"],
    "columns": {
        "status": {
            "preserve_tokens": ["unknown"]
        },
        "email": {
            "extra_null_tokens": ["missing", "unknown"]
        }
    }
}
```

## Expected Files

```text
docs/design/null_token_profiles.md
log_protocol/01_CSV_ambiguous_null_token_decision/003_future_configurable_policy.md
```

## Acceptance Criteria

- Future config direction is documented.
- Column-specific behavior is considered.
- Global default remains conservative.
- No implementation unless separately approved.

---

## Out Of Scope

This plan does not include:

```text
adding unknown to default NULL_VALUES
adding missing to default NULL_VALUES
cleaning profile implementation
column-specific null rules implementation
null token statistics implementation
CSV parser diagnostics
number parsing
mixed-type diagnostics
```

---

## Recommended Implementation Order

```text
Stage A — Ambiguous Token Policy Decision
Stage B — Regression Test Confirmation
Stage C — Future Configurable Policy Draft
```

---

## Required Protocol Folder

When active, use:

```text
log_protocol/01_CSV_ambiguous_null_token_decision/
```

Protocol files:

```text
001_ambiguous_token_policy.md
002_regression_test_confirmation.md
003_future_configurable_policy.md
999_plan_completion.md
```

---

## Activation Rule

This plan is not active until the user explicitly confirms:

```text
Start 01_CSV_ambiguous_null_token_decision
```

Until then, continue only with the currently active confirmed plan.
