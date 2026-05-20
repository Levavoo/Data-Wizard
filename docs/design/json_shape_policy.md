# JSON Shape Policy

## Purpose

Defines supported and unsupported JSON root/record shapes for the first JSON adapter.

---

## Supported Root Shape

Supported:

```text
list[object]
```

Example:

```json
[
  {"customer_id": 1, "name": "Alice"},
  {"customer_id": 2, "name": "Bob"}
]
```

---

## Unsupported Root Shapes

Rejected for first implementation:

```text
single object root
list of primitive values
mixed list values
empty file
invalid JSON
```

Deferred for future:

```text
object with nested records under a key
JSON Lines / NDJSON
multiple table extraction
```

---

## Column Union Policy

Columns are the union of all keys across all object records.

Rules:

```text
first appearance determines column order
missing keys in later/earlier records become None
keys are normalized into internal column names
original key is stored as original_name
```

---

## Nested Value Policy

Nested values are preserved as compact JSON strings.

Rules:

```text
object value -> compact JSON string
array value -> compact JSON string
column is recorded in nested/array diagnostics
```

Example:

```json
{"name": "Alice", "address": {"city": "Berlin"}}
```

Stored value:

```json
{"city":"Berlin"}
```

---

## Error Policy

Invalid or unsupported JSON should raise clear `ValueError` messages.

Examples:

```text
JSON root must be a list of objects.
JSON record at index 2 is not an object.
JSON file is empty.
```

---

## Future Extension Points

Possible future options:

```text
root_path
nested_values = stringify | reject | flatten
json_lines = true
single_object_as_row = true
```
