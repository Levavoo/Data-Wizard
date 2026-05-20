# Protocol — Stage A JSON Scope and Shape Policy

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/18_JSON_adapter.md` |
| Stage | Stage A — JSON Scope and Shape Policy |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | JSON design documentation |

---

## Purpose

Document exactly which JSON shapes are supported and which are rejected/deferred for the first JSON adapter implementation.

---

## Files Created

```text
docs/design/json_adapter_scope.md
docs/design/json_shape_policy.md
```

---

## Supported First Scope

```text
single .json file
root value is a list
list items are objects
object keys become table columns
primitive values are preserved
missing keys become None
nested objects and arrays are converted to compact JSON strings and diagnosed
```

---

## Supported Root Shape

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

## Unsupported / Deferred Shapes

```text
single root object
list of primitive values
mixed list values
JSON Lines / NDJSON
object root with nested records path
arbitrary deep flattening
array explosion
multi-table extraction
streaming parser
business-specific transformations
```

---

## Column Policy

```text
columns are the union of all keys across object records
first key appearance determines column order
missing keys become None
keys are normalized into internal column names
original key is stored as original_name
```

---

## Nested Value Policy

```text
nested object values are converted to compact JSON strings
array values are converted to compact JSON strings
affected columns are recorded in diagnostics
```

Reason:

```text
this preserves information without inventing arbitrary flattening behavior
```

---

## Important Decision

No production code was changed in Stage A.

Stage A only created JSON design policy documentation.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/design/json_adapter_scope.md` | Created | Defines first JSON adapter scope and boundaries. |
| `docs/design/json_shape_policy.md` | Created | Defines supported root shape, column policy, nested value policy, and error policy. |
| `log_protocol/18_JSON_adapter/001_json_scope_and_shape_policy.md` | Created | Records Stage A completion after interrupted run. |

---

## Repair Note

This protocol file was created after the initial `Start 18_JSON_adapter` process was interrupted.

The Stage A design docs already existed before this repair.

---

## Next Stage

```text
Stage B — JSON Fixtures
```
