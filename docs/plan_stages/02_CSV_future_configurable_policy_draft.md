# CSV Future Configurable Policy Draft

## Status

```text
Draft — not active until user confirmation.
```

This plan defines a future direction for configurable null-token behavior.

It must not be started automatically.

---

## Purpose

Design how future cleaning profiles can control null-token handling without making the default cleaner unsafe.

Goal:

```text
conservative default cleaner
→ optional profile-specific null behavior
→ optional column-specific overrides
→ safer migration workflows
```

---

## Background

Previous decisions:

```text
#N/A, NIL, --, ?, not available, not_applicable → None
unknown and missing are preserved by default
```

Reason:

```text
unknown and missing can be missing-value placeholders
but they can also be legitimate category values
```

Therefore, future support should be configurable instead of global.

---

## Architectural Layer

This plan belongs mainly to:

```text
09_Value_Normalization_Layer
13_Canonical_Model_Layer
```

Future implementation may also touch:

```text
cleaning profiles
pipeline configuration
diagnostic reporting
```

Rules:

```text
Adapters must not clean values.
Default cleaners should remain conservative.
Profile configuration should control optional aggressive behavior.
Column-specific rules should override global rules.
Diagnostics should explain which profile changed which values.
```

---

# Stage A — Configuration Shape Draft

## Goal

Define the first proposed shape for configurable null policies.

Possible future configuration:

```python
{
    "global_null_tokens": ["", "null", "n/a", "#N/A"],
    "extra_null_tokens": ["missing"],
    "preserve_tokens": ["unknown"],
    "columns": {
        "email": {
            "extra_null_tokens": ["unknown", "missing"]
        },
        "status": {
            "preserve_tokens": ["unknown", "missing"]
        }
    }
}
```

## Expected Files

```text
docs/design/null_token_profiles.md
log_protocol/02_CSV_future_configurable_policy_draft/001_configuration_shape.md
```

## Acceptance Criteria

- Configuration shape is documented.
- Global and column-specific behavior are separated.
- Preserve rules are included.
- No production implementation is required.

---

# Stage B — Policy Precedence Rules

## Goal

Define rule priority when global and column-specific settings conflict.

Recommended precedence:

```text
1. column preserve_tokens
2. column extra_null_tokens
3. global preserve_tokens
4. global extra_null_tokens
5. default NULL_VALUES
```

Example:

```python
{
    "extra_null_tokens": ["unknown"],
    "columns": {
        "status": {
            "preserve_tokens": ["unknown"]
        }
    }
}
```

Expected behavior:

```text
email = unknown  → None
status = unknown → "unknown"
```

## Expected Files

```text
docs/design/null_policy_precedence.md
log_protocol/02_CSV_future_configurable_policy_draft/002_policy_precedence.md
```

## Acceptance Criteria

- Conflict resolution is explicit.
- Column-specific preservation can protect meaningful categories.
- Default behavior remains conservative.

---

# Stage C — Profile Examples

## Goal

Draft reusable profile examples.

Example profiles:

```text
strict migration profile
survey profile
CRM profile
ERP import profile
financial import profile
```

## Example: Strict Migration Profile

```python
{
    "name": "strict_migration",
    "extra_null_tokens": ["unknown", "missing", "not provided"]
}
```

## Example: Survey Profile

```python
{
    "name": "survey",
    "preserve_tokens": ["unknown"],
    "extra_null_tokens": ["not answered"]
}
```

## Expected Files

```text
docs/design/null_profile_examples.md
log_protocol/02_CSV_future_configurable_policy_draft/003_profile_examples.md
```

## Acceptance Criteria

- At least three realistic profile examples are documented.
- Each profile explains when it should be used.
- No implementation is required.

---

# Stage D — Diagnostic Requirements

## Goal

Define what future diagnostics should report when configurable null policies are used.

Possible diagnostic output:

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

## Expected Files

```text
docs/design/null_policy_diagnostics.md
log_protocol/02_CSV_future_configurable_policy_draft/004_diagnostic_requirements.md
```

## Acceptance Criteria

- Diagnostics explain profile-driven changes.
- Diagnostics support auditability.
- Diagnostics remain report-only and do not mutate values.

---

# Stage E — Future Implementation Boundary

## Goal

Define where implementation should eventually live.

Possible future files:

```text
data_processor/cleaners/null_policy.py
data_processor/cleaners/null_policy.md
data_processor/cleaners/cleaning_profile.py
data_processor/cleaners/cleaning_profile.md
```

Possible future tests:

```text
tests/test_null_policy.py
tests/test_null_policy.md
tests/test_cleaning_profile.py
tests/test_cleaning_profile.md
```

## Important Boundary

Implementation should not be added directly to:

```text
data_processor/adapters/csv_adapter.py
```

Reason:

```text
Adapters parse only.
Null policy belongs to cleaning/profile layers.
```

## Expected Files

```text
docs/design/null_policy_implementation_boundary.md
log_protocol/02_CSV_future_configurable_policy_draft/005_implementation_boundary.md
```

## Acceptance Criteria

- Future implementation modules are proposed.
- Adapter boundary is protected.
- Relationship to cleaning profiles is clear.

---

## Out Of Scope

This plan does not include:

```text
actual cleaning profile implementation
actual null policy implementation
CLI profile loading
JSON/YAML config parsing
schema-specific validation
null token statistics implementation
CSV parser changes
number parsing changes
```

---

## Recommended Implementation Order

```text
Stage A — Configuration Shape Draft
Stage B — Policy Precedence Rules
Stage C — Profile Examples
Stage D — Diagnostic Requirements
Stage E — Future Implementation Boundary
```

---

## Required Protocol Folder

When active, use:

```text
log_protocol/02_CSV_future_configurable_policy_draft/
```

Protocol files:

```text
001_configuration_shape.md
002_policy_precedence.md
003_profile_examples.md
004_diagnostic_requirements.md
005_implementation_boundary.md
999_plan_completion.md
```

---

## Activation Rule

This plan is not active until the user explicitly confirms:

```text
Start 02_CSV_future_configurable_policy_draft
```

Until then, continue only with the currently active confirmed plan.
