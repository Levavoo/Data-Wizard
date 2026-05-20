# JSON Adapter

## Purpose

Reads supported JSON files and converts them into the internal `Table` model.

---

## Supported Shape

```text
root value: list
list items: objects
```

---

## Behavior

```text
object keys become columns
missing keys become None
nested objects become compact JSON strings
arrays become compact JSON strings
parse diagnostics are stored in table metadata
```

---

## Unsupported Shapes

```text
single object root
mixed list values
list of primitives
invalid JSON
```

---

## Boundary

The adapter does not clean, validate, infer types, or export reports.
