# Null Token Profiles

## Purpose

This document defines a future configuration shape for profile-driven null-token handling.

The goal is to keep the default null cleaner conservative while allowing migration-specific or column-specific behavior when explicitly configured.

---

## Problem

Some tokens are safe default null values:

```text
""
null
n/a
#N/A
NIL
--
?
not available
```

Other tokens are ambiguous:

```text
unknown
missing
```

They may mean missing data in one project and a meaningful category in another.

---

## Proposed Configuration Shape

```python
{
    "name": "strict_migration",
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

---

## Field Meaning

### `name`

Human-readable profile name.

Example:

```text
strict_migration
```

---

### `global_null_tokens`

Defines the complete global null token list for a profile.

If omitted, the system should use the built-in conservative defaults.

---

### `extra_null_tokens`

Adds tokens to the default global null token list.

Example:

```python
"extra_null_tokens": ["missing"]
```

---

### `preserve_tokens`

Protects tokens from becoming null globally.

Example:

```python
"preserve_tokens": ["unknown"]
```

---

### `columns`

Defines column-specific overrides.

Column policies should override global policies.

Example:

```python
"columns": {
    "status": {
        "preserve_tokens": ["unknown"]
    }
}
```

---

## Design Rule

Profiles should be explicit.

The default cleaner should stay conservative and deterministic.

---

## Out Of Scope

This document does not implement profile loading or cleaner behavior.

Future implementation should be handled in dedicated cleaner/profile modules, not adapters.
