# parse_diagnostics.py

## Purpose

`parse_diagnostics.py` defines structured parser diagnostics for input adapters.

The diagnostics describe structural parsing observations, such as short rows, extra fields, duplicate headers, empty headers, detected delimiter, and detected encoding.

They do not clean, validate, quarantine, or transform data.

---

## Architecture Position

```text
Input file
→ Adapter
→ ParseDiagnostics
→ Table.metadata["parse_diagnostics"]
→ Diagnostic Bundle
```

---

## Main Class

### `ParseDiagnostics`

A dataclass used by adapters to collect parser observations.

Important fields:

- `header_row_index`
- `preamble_row_count`
- `rows_with_extra_fields`
- `extra_field_count`
- `rows_with_missing_fields`
- `missing_field_count`
- `duplicate_headers`
- `empty_headers`
- `delimiter`
- `encoding`
- `warnings`

---

## Design Rules

Parser diagnostics may record structural facts.

They must not:

- clean cell values
- infer semantic types
- validate business constraints
- remove rows
- quarantine rows
- export reports

---

## Serialization

Use:

```python
parse_diagnostics.to_dict()
```

to attach diagnostics to table metadata.

Example:

```python
table.add_metadata("parse_diagnostics", parse_diagnostics.to_dict())
```

---

## Example Output

```python
{
    "header_row_index": 0,
    "preamble_row_count": 0,
    "rows_with_extra_fields": [3],
    "extra_field_count": 1,
    "rows_with_missing_fields": [2],
    "missing_field_count": 1,
    "duplicate_headers": ["name"],
    "empty_headers": [3],
    "delimiter": ",",
    "encoding": "utf-8",
    "warnings": [
        "One or more rows contain extra fields."
    ]
}
```

---

## Developer Notes

This model is intentionally format-independent enough to be reused by future adapters such as Excel or JSON where similar structural diagnostics are useful.
