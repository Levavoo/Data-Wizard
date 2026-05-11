# test_csv_adapter.py

## Purpose

Tests the CSV adapter integration.

This verifies that:

```text
CSV
→ CsvAdapter
→ Table
```

works correctly.

---

# Tested File

```text
data_processor/adapters/csv_adapter.py
```

---

# Current Test Coverage

## `test_csv_adapter_returns_table`

Verifies:

- adapter returns a `Table` object

---

## `test_csv_adapter_row_count`

Verifies:

- all rows are parsed correctly

---

## `test_csv_adapter_column_count`

Verifies:

- schema column count is correct

---

## `test_csv_adapter_normalized_headers`

Verifies:

- headers are normalized correctly

Expected normalization:

```text
trim whitespace
lowercase
spaces → underscores
```

---

## `test_csv_adapter_preserves_raw_values`

Verifies:

- values remain raw strings
- no cleaning happens yet
- no type inference happens yet

This is architecturally important.

---

## `test_csv_adapter_duplicate_headers_are_unique`

Verifies duplicate headers are preserved safely by renaming duplicates.

Example:

```text
name
name
```

becomes:

```text
name
name_2
```

This prevents data loss.

---

## `test_csv_adapter_empty_headers_are_named`

Verifies empty headers are converted into:

```text
unnamed_column
```

---

## `test_csv_adapter_duplicate_empty_headers_are_unique`

Verifies multiple empty headers become:

```text
unnamed_column
unnamed_column_2
```

---

## `test_csv_adapter_short_rows_fill_missing_values`

Verifies rows with fewer fields than headers are padded with:

```python
None
```

Example:

```csv
customer_id,name,country
1,Alice
```

becomes:

```python
{
    "customer_id": "1",
    "name": "Alice",
    "country": None
}
```

---

## `test_csv_adapter_extra_fields_are_ignored`

Verifies extra fields beyond known headers are ignored for now.

Example:

```csv
customer_id,name
1,Alice,Germany
```

becomes:

```python
{
    "customer_id": "1",
    "name": "Alice"
}
```

Future parser diagnostics should report ignored extra fields.

---

## `test_csv_adapter_stores_parser_metadata`

Verifies parser metadata is stored on the table.

Expected metadata:

```python
{
    "source_format": "csv",
    "encoding": "utf-8",
    "delimiter": ";"
}
```

---

# Design Principle

The adapter layer should only parse structure.

Later pipeline stages handle:

- cleaning
- type inference
- validation
- transformations
- export

---

# Why Duplicate Header Handling Matters

Real migration files often contain duplicate headers.

Without safe handling:

```text
name,name
```

can cause one value to overwrite another.

The adapter now preserves both by creating:

```text
name,name_2
```

---

# Why Short Row Handling Matters

Some CSV rows may have fewer fields than the header row.

The adapter does not crash.

It fills missing fields with:

```python
None
```

This allows later quality reports to detect missing data.

---

# Why Extra Field Handling Matters

Some CSV rows may have more fields than the header row.

Current behavior:

```text
ignore extra fields
```

This is temporary.

Future parser diagnostics should report these as warnings.

---

# Run Tests

```powershell
pytest tests\test_csv_adapter.py
```

---

# Recommended Validation Workflow

```powershell
ruff check `
    data_processor\adapters\csv_adapter.py `
    tests\test_csv_adapter.py

black `
    data_processor\adapters\csv_adapter.py `
    tests\test_csv_adapter.py

pytest tests\test_csv_adapter.py
pytest
```

---

# Developer Notes

CSV adapter tests are especially important because CSV files can vary widely.

Keep adding tests here whenever real-world CSV issues appear.

---

# Future Improvements

Possible future tests:

- malformed rows
- quoted values
- multiline fields
- duplicate headers with different casing
- duplicate headers with spaces
- empty files
- invalid CSV handling
- encoding fallback
- strict/tolerant mode
- parse warnings