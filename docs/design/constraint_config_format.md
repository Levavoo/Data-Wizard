# Constraint Config Format

## Purpose

This document defines the machine-readable constraint configuration format used by the CSV CLI and config loader.

---

## Format

The constraint config is a JSON list of dictionaries.

Example:

```json
[
    {
        "column": "customer_id",
        "type": "required"
    },
    {
        "column": "customer_id",
        "type": "unique"
    },
    {
        "column": "country",
        "type": "allowed_values",
        "values": ["Germany", "France"]
    },
    {
        "column": "email",
        "type": "regex",
        "pattern": "^[^@]+@[^@]+\\.[^@]+$"
    }
]
```

---

## Required Fields

```text
column
type
```

Aliases also supported:

```text
column_name
constraint_type
```

---

## Supported Types

```text
required
unique
min_value
max_value
allowed_values
regex_pattern
regex
```

---

## Type-Specific Fields

| Type | Required Field |
|---|---|
| `required` | none |
| `unique` | none |
| `min_value` | `value` |
| `max_value` | `value` |
| `allowed_values` | `values` |
| `regex_pattern` | `pattern` |
| `regex` | `pattern` |

---

## Invalid Config Behavior

Invalid configs raise `ValueError`.

Examples:

```text
missing column
missing type
unsupported constraint type
missing type-specific value field
```

---

## Design Rule

Config loading only creates `Constraint` objects.

It does not validate rows.
