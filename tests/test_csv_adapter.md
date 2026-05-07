# test_csv_adapter.py

## Purpose

Tests the CSV adapter integration.

This test verifies that:

```text
CSV
→ CsvAdapter
→ Table
```

works correctly.

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

# Design Principle

The adapter layer should only parse structure.

Later pipeline stages will handle:

- cleaning
- type inference
- validation
- transformations

---

# Future Improvements

Possible future tests:

- delimiter detection
- encoding fallback
- malformed rows
- quoted values
- multiline fields
- duplicate headers
- empty files
- invalid CSV handling