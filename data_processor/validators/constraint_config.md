# constraint_config.py

## Purpose

`constraint_config.py` converts machine-readable constraint configuration dictionaries into `Constraint` objects.

This module belongs to the validator layer.

Architecture:

```text
Constraint JSON/config
→ constraint_config loader
→ Constraint objects
→ validation engine
```

---

## Main Function

### `load_constraints_from_config(config)`

Converts a list of dictionaries into a list of `Constraint` objects.

Example input:

```python
[
    {
        "column": "customer_id",
        "type": "required"
    },
    {
        "column": "email",
        "type": "regex",
        "pattern": "^[^@]+@[^@]+\\.[^@]+$"
    }
]
```

---

## Supported Constraint Types

```text
required
unique
min_value
max_value
allowed_values
regex_pattern
regex
```

`regex` is normalized to:

```text
regex_pattern
```

---

## Required Fields

All constraints require:

```text
column
type
```

or aliases:

```text
column_name
constraint_type
```

---

## Value Fields

Some constraints require extra fields:

| Constraint | Required Field |
|---|---|
| `min_value` | `value` |
| `max_value` | `value` |
| `allowed_values` | `values` |
| `regex_pattern` | `pattern` |
| `regex` | `pattern` |

---

## Errors

Invalid configuration raises `ValueError` with a clear message.

Examples:

```text
Constraint config must be a list of dictionaries.
Unsupported constraint type: foreign_key
Constraint type 'regex_pattern' requires field: pattern
```

---

## Design Rules

This module only loads configuration.

It must not:

- validate table rows
- mutate table data
- export reports
- parse CSV files

Validation remains in `constraints.py`.
