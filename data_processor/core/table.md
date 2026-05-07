# table.py

## Purpose

`table.py` defines the `Table` class.

The `Table` class is the canonical internal dataset representation used throughout the project.

All input formats should eventually become a `Table`.

Examples:

```text
CSV
→ Table

Excel
→ Table

JSON
→ Table
```

This allows the cleaning engine to work independently from file formats.

---

# Main Class

## `Table`

Represents one dataset in memory.

Contains:

- dataset name
- schema
- rows
- metadata

---

# Attributes

| Attribute | Type | Description |
|---|---|---|
| `name` | `str` | Human-readable dataset name |
| `schema` | `Schema` | Dataset structure definition |
| `rows` | `list[dict[str, Any]]` | Dataset records |
| `metadata` | `dict[str, Any]` | Additional dataset information |

---

# Row Structure

Rows are stored as dictionaries.

Example:

```python
{
    "customer_id": 1001,
    "name": "Alice",
    "country": "Germany"
}
```

---

# Main Methods

## `add_row(row)`

Adds one row to the dataset.

Example:

```python
table.add_row(
    {
        "id": 1,
        "name": "Alice"
    }
)
```

---

## `add_rows(rows)`

Adds multiple rows.

---

## `row_count()`

Returns total number of rows.

---

## `column_count()`

Returns total number of columns defined in the schema.

---

## `is_empty()`

Checks whether the table contains rows.

Returns:

- `True`
- `False`

---

## `add_metadata(key, value)`

Adds extra dataset metadata.

Example:

```python
table.add_metadata("source_file", "customers.csv")
```

---

## `head(limit=5)`

Returns the first rows of the dataset.

Useful for:

- debugging
- previews
- testing

---

## `to_dict()`

Converts the table into a serializable dictionary.

Useful for:

- testing
- debugging
- JSON export
- reports

---

# Example

```python
from data_processor.core.table import Table

table = Table(name="customers")

table.add_row(
    {
        "id": 1,
        "name": "Alice"
    }
)

print(table.row_count())
```

---

# Developer Notes

This file must remain format-independent.

It should not contain:

- CSV parsing logic
- Excel parsing logic
- JSON parsing logic
- cleaning logic
- validation logic
- export logic

The `Table` only defines the internal dataset structure.

---

# Design Principle

The project architecture is:

```text
Many Inputs
→ One Internal Table Model
→ Shared Cleaning Engine
→ Many Outputs
```

The `Table` class is the center of this architecture.

---

# Future Improvements

Possible future additions:

- row indexing
- lazy loading
- chunked processing
- streaming support
- row metadata
- relationship tracking
- memory optimization
- column statistics
- schema version tracking