# Null Policy Implementation Boundary

## Purpose

This document defines where future configurable null-token policy implementation should live.

The goal is to protect the existing architecture and avoid putting cleaning behavior into adapters.

---

## Proposed Future Files

Possible implementation files:

```text
data_processor/cleaners/null_policy.py
data_processor/cleaners/null_policy.md
data_processor/cleaners/cleaning_profile.py
data_processor/cleaners/cleaning_profile.md
```

Possible test files:

```text
tests/test_null_policy.py
tests/test_null_policy.md
tests/test_cleaning_profile.py
tests/test_cleaning_profile.md
```

---

## Responsibilities

### `null_policy.py`

Should handle:

- global null-token policy
- column-specific overrides
- preserve-token rules
- policy precedence
- diagnostic event creation

---

### `cleaning_profile.py`

Should handle:

- reusable cleaning profile definitions
- profile validation
- profile defaults
- profile metadata

---

## Files That Should Not Own This Logic

Do not implement configurable null policy in:

```text
data_processor/adapters/csv_adapter.py
```

Reason:

```text
Adapters parse formats only.
```

Do not implement it in validators.

Reason:

```text
Validators validate only and must not mutate data.
```

Do not implement it in profilers.

Reason:

```text
Profilers analyze only and must not mutate data.
```

---

## Pipeline Boundary

The pipeline may later accept a cleaning profile and pass it to cleaner modules.

Example future flow:

```text
Adapter
→ Table
→ Null Cleaner with optional Null Policy
→ Text Cleaner
→ Type Inference
→ Type-Aware Casting
→ Diagnostics
```

The pipeline should orchestrate the profile, not contain the null policy logic itself.

---

## Design Rule

Default behavior should remain deterministic without a profile.

Configured behavior should be explicit, documented, and auditable.
