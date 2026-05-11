# Null Policy Precedence

## Purpose

This document defines how future null-token policies should resolve conflicts between global rules and column-specific rules.

---

## Recommended Precedence

Use this order from highest priority to lowest priority:

```text
1. column preserve_tokens
2. column extra_null_tokens
3. global preserve_tokens
4. global extra_null_tokens
5. default NULL_VALUES
```

---

## Why Precedence Matters

A token such as `unknown` may need different behavior depending on the column.

Example:

```text
email = unknown  → None
status = unknown → "unknown"
```

This is only possible if column-level rules can override global behavior.

---

## Example Policy

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

---

## Conflict Rule

Preserve rules should win over null-conversion rules at the same or higher specificity.

This protects meaningful category values from accidental deletion.

---

## Default Behavior

If no profile is configured, only the built-in conservative `NULL_VALUES` set should be used.

Ambiguous tokens remain unchanged by default.

---

## Implementation Notes

Future implementation should centralize precedence handling in a null policy module.

Suggested future file:

```text
data_processor/cleaners/null_policy.py
```

The CSV adapter must not implement or evaluate these rules.
