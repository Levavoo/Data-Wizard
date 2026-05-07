# column.py

## Purpose

`column.py` defines the `Column` class.

A `Column` represents one field inside the internal canonical table model.

This file belongs to the core layer and should stay independent from specific file formats such as CSV, Excel, or JSON.

---

## Main Class

## `Column`

Represents metadata about one table column.

### Attributes

| Attribute | Type | Description |
|---|---|---|
| `name` | `str` | Standardized internal column name |
| `original_name` | `str | None` | Original source column name |
| `inferred_type` | `str` | Logical type detected later by inference |
| `nullable` | `bool` | Whether missing/null values are allowed |
| `metadata` | `dict[str, Any]` | Extra extensible information |

---

## Main Methods

### `__post_init__()`

Runs automatically after object creation.

Current behavior:

- trims whitespace from `name`
- trims whitespace from `original_name` if available

---

### `display_name()`

Returns the best human-readable name.

Priority:

1. `original_name`
2. `name`

---

### `set_type(inferred_type: str)`

Updates the logical type of the column.

Example:

```python
column.set_type("integer")