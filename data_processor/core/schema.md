# schema.py

## Purpose

`schema.py` defines the `Schema` class.

A schema describes the structural definition of a dataset through its columns.

The schema belongs to the canonical internal model and is shared across all supported formats.

---

# Main Class

## `Schema`

Represents dataset structure.

Contains:

- ordered columns
- schema metadata

---

# Attributes

| Attribute | Type | Description |
|---|---|---|
| `columns` | `list[Column]` | Ordered list of dataset columns |
| `metadata` | `dict[str, Any]` | Additional schema information |

---

# Main Methods

## `add_column(column: Column)`

Adds a column to the schema.

Example:

```python
schema.add_column(column)
```

---

## `get_column(name: str)`

Finds a column by internal name.

Returns:

- matching `Column`
- or `None`

Example:

```python
column = schema.get_column("customer_id")
```

---

## `has_column(name: str)`

Checks whether a column exists.

Returns:

- `True`
- `False`

---

## `remove_column(name: str)`

Removes a column from the schema.

Returns:

- `True` if removed
- `False` if not found

---

## `column_names()`

Returns all internal column names.

Example:

```python
["id", "name", "email"]
```

---

## `add_metadata(key, value)`

Adds additional schema metadata.

Example:

```python
schema.add_metadata("source_format", "csv")
```

---

## `to_dict()`

Converts the schema into a serializable dictionary.

Useful for:

- debugging
- reports
- JSON export
- tests

---

# Example

```python
from data_processor.core.column import Column
from data_processor.core.schema import Schema

schema = Schema()

schema.add_column(
    Column(
        name="customer_id",
        original_name="Customer ID",
    )
)

print(schema.column_names())
```

---

# Developer Notes

This file should remain format-independent.

It should not contain:

- CSV parsing
- Excel parsing
- JSON parsing
- value cleaning
- validation rules
- export logic

The schema only describes structure.

---

# Future Improvements

Possible future additions:

- schema versioning
- schema comparison
- schema merge support
- constraint definitions
- relationship metadata
- primary key definitions
- foreign key definitions
- inferred statistics