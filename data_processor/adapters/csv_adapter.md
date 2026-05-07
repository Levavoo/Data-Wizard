# csv_adapter.py

## Purpose

`csv_adapter.py` reads CSV files and converts them into the internal `Table` model.

This is the first real ingestion adapter in the system.

Architecture:

```text
CSV File
→ CsvAdapter
→ Table
```

---

# Responsibilities

The CSV adapter is responsible for:

- validating the source file
- detecting encoding
- detecting delimiter
- reading CSV rows
- normalizing headers
- building the schema
- building the internal table

The adapter is NOT responsible for:

- cleaning values
- type inference
- validation
- transformations
- exporting

---

# Main Class

## `CsvAdapter`

Inherits from:

```python
BaseAdapter
```

Supported extensions:

```python
(".csv",)
```

---

# Supported Encodings

Current fallback order:

```text
utf-8
utf-8-sig
cp1252
```

Purpose:

- support common Windows CSV files
- support BOM-based UTF files
- support legacy encodings

---

# Supported Delimiters

Current candidates:

```text
,
;
\t
|
```

Delimiter detection uses:

```python
csv.Sniffer()
```

Fallback delimiter:

```text
,
```

---

# Header Normalization

Current normalization rules:

```text
trim whitespace
lowercase
replace spaces with underscores
```

Example:

```text
" Customer ID "
→ "customer_id"
```

---

# Row Handling

Rows are initially stored as raw strings.

Example:

```python
{
    "customer_id": "1001",
    "country": "Germany"
}
```

Important:

No type conversion happens here.

This is intentional.

Type inference belongs to later pipeline stages.

---

# Main Methods

## `read()`

Main adapter entry point.

Flow:

```text
validate file
→ detect encoding
→ detect delimiter
→ parse CSV
→ build schema
→ build table
→ return Table
```

---

## `_detect_encoding()`

Tries multiple encodings until one succeeds.

Raises:

```python
ValueError
```

if decoding fails.

---

## `_detect_delimiter()`

Uses `csv.Sniffer()` to detect delimiter.

Fallback:

```text
,
```

---

## `_normalize_header()`

Converts external headers into internal names.

Current rules:

- trim
- lowercase
- spaces → underscores

---

## `_build_schema()`

Creates a `Schema` object from CSV headers.

Creates one `Column` per header.

---

## `_normalize_row()`

Converts raw CSV rows into normalized row dictionaries.

Maps:

```text
original header
→ normalized internal header
```

---

# Example

```python
from data_processor.adapters.csv_adapter import CsvAdapter

adapter = CsvAdapter("data/raw/customers.csv")

table = adapter.read()

print(table.row_count())
print(table.schema.column_names())
```

---

# Developer Notes

This adapter intentionally avoids:

- pandas
- implicit type casting
- implicit null handling
- automatic datetime parsing

Reason:

The cleaning pipeline should stay explicit and deterministic.

---

# Future Improvements

Possible later additions:

- malformed row recovery
- duplicate header handling
- streaming/chunked reading
- quoted newline support
- configurable delimiter detection
- configurable encoding policy
- row-level error quarantine
- multi-table CSV support
- large-file memory optimization