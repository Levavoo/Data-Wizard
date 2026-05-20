# JSON Adapter Scope

## Purpose

Defines the first supported JSON scope for Data Wizard.

Plan:

```text
docs/plan_stages/18_JSON_adapter.md
```

---

## First Supported Scope

The first JSON adapter supports:

```text
single .json file
root value is a list
list items are objects
object keys become table columns
primitive values are preserved
missing keys become None
nested objects/arrays are converted to compact JSON strings and diagnosed
```

---

## Supported Primitive Values

```text
string
number
boolean
null
```

Conversion:

```text
JSON string -> Python str
JSON number -> Python int/float
JSON boolean -> Python bool
JSON null -> None
```

---

## Nested Values

Nested objects and arrays are allowed but not flattened.

Current policy:

```text
nested object -> compact JSON string
array -> compact JSON string
column name is recorded in diagnostics
```

Reason:

```text
preserve source information without adding arbitrary flattening behavior
```

---

## Out Of Scope

Not supported in the first adapter:

```text
JSON Lines / NDJSON
single root object as one-row table
root object with nested records path
arbitrary deep flattening
array explosion
multi-table extraction
streaming parser
business-specific transformations
```

---

## Adapter Boundary

The JSON adapter only parses JSON into the internal `Table` model.

It must not:

```text
clean values
validate constraints
infer types
export reports
apply business rules
```
