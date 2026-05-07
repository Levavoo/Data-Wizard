# csv_exporter.py

## Purpose

`csv_exporter.py` writes the internal `Table` model to a CSV file.

This module belongs to the exporter layer.

Architecture:

```text
Table
→ CSV Exporter
→ CSV File
```

---

# Main Responsibilities

The CSV exporter handles:

- creating output folders if needed
- writing UTF-8 CSV files
- writing headers in schema column order
- writing rows from `Table.rows`
- serializing cleaned Python values into CSV-safe strings

---

# Main Functions

## `export_table_to_csv(table, output_path, encoding="utf-8")`

Exports a `Table` object to a CSV file.

Example:

```python
from data_processor.exporters.csv_exporter import export_table_to_csv

export_table_to_csv(
    table=table,
    output_path="data/processed/customers_clean.csv",
)
```

---

# Header Handling

Headers come from:

```python
table.schema.column_names()
```

This preserves schema order.

Example:

```text
id,name,country
```

---

# Row Handling

Rows are written from:

```python
table.rows
```

Only schema columns are exported.

Extra keys in row dictionaries are ignored.

Missing row keys are written as empty values.

---

# Value Serialization

## `serialize_csv_value(value)`

Converts Python values into CSV-safe strings.

Current behavior:

| Python Value | CSV Output |
|---|---|
| `None` | `""` |
| `True` | `"true"` |
| `False` | `"false"` |
| `date(...)` | ISO date string |
| `datetime(...)` | ISO datetime string |
| other values | `str(value)` |

---

# Examples

## Input Row

```python
{
    "name": "Alice",
    "active": True,
    "birth_date": date(2026, 1, 31),
    "email": None
}
```

## CSV Output

```text
Alice,true,2026-01-31,
```

---

# Important Design Rule

Exporters only write data.

They should not:

- clean values
- validate constraints
- infer types
- transform rows
- modify the table

Those actions belong to earlier pipeline stages.

---

# Pipeline Position

Recommended pipeline order:

```text
Parsing
→ Cleaning
→ Type Inference
→ Schema Inference
→ Quality Report
→ Export
```

---

# Developer Notes

This exporter intentionally avoids pandas.

Reason:

The project uses its own canonical internal model and should keep CSV output explicit and deterministic.

---

# Current Limitations

Current implementation does not support:

- custom delimiter
- quoting policy configuration
- line ending configuration
- append mode
- chunked output
- compressed CSV output
- metadata sidecar files

---

# Future Improvements

Possible future additions:

- configurable delimiter
- configurable quote handling
- gzip CSV export
- metadata export
- report export beside CSV
- large-file streaming support
- output schema validation