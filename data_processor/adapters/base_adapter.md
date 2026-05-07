# base_adapter.py

## Purpose

`base_adapter.py` defines the base interface for all input adapters.

An adapter converts an external data source into the internal `Table` model.

Examples:

```text
CSV file
→ CsvAdapter
→ Table

Excel file
→ ExcelAdapter
→ Table

JSON file
→ JsonAdapter
→ Table
```

---

# Main Class

## `BaseAdapter`

Abstract base class for format-specific adapters.

All future input adapters should inherit from this class.

---

# Responsibilities

Adapters should handle:

- checking whether the source file exists
- checking whether the file extension is supported
- reading the external file format
- converting parsed data into a `Table`

Adapters should not handle:

- value cleaning
- type inference
- validation
- transformation
- output/export logic

---

# Attributes

| Attribute | Type | Description |
|---|---|---|
| `supported_extensions` | `tuple[str, ...]` | File extensions supported by the adapter |
| `file_path` | `Path` | Path to the source file |

---

# Main Methods

## `__init__(file_path)`

Stores the source file path as a `Path` object.

Example:

```python
adapter = CsvAdapter("data/raw/customers.csv")
```

---

## `validate_file()`

Checks:

1. source path exists
2. source path is a file
3. file extension is supported

Raises:

- `FileNotFoundError`
- `ValueError`

---

## `source_name()`

Returns the file name without extension.

Example:

```python
customers.csv
→ customers
```

This is useful for naming the internal `Table`.

---

## `read()`

Abstract method.

Every adapter must implement this method.

Expected behavior:

```python
table = adapter.read()
```

Returns:

```python
Table
```

---

# Example Subclass

```python
from data_processor.adapters.base_adapter import BaseAdapter
from data_processor.core.table import Table


class CsvAdapter(BaseAdapter):
    supported_extensions = (".csv",)

    def read(self) -> Table:
        self.validate_file()

        # CSV parsing happens here.
        return Table(name=self.source_name())
```

---

# Developer Notes

This file belongs to the adapter layer.

Keep it stable and minimal.

This file should not contain:

- CSV-specific parsing
- Excel-specific parsing
- JSON-specific parsing
- cleaning logic
- validation logic
- transformation logic
- export logic

---

# Future Improvements

Possible future additions:

- adapter metadata
- source checksum validation
- file size checks
- permission checks
- streaming support
- multi-table source support
- adapter registry