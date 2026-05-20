# JSON Adapter Fixtures

## Purpose

Fixtures for `18_JSON_adapter`.

---

## Fixtures

| File | Purpose |
|---|---|
| `simple_customers.json` | Supported flat list-of-objects JSON. |
| `missing_keys_customers.json` | Supported list with unioned keys and missing values. |
| `nested_values_customers.json` | Supported list where nested object/array values should be stringified and diagnosed. |
| `invalid_root_object.json` | Unsupported root object shape. |
| `mixed_list_values.json` | Unsupported mixed list shape. |

---

## Supported First Shape

```text
list[object]
```

---

## Unsupported First Shapes

```text
single root object
mixed list values
list of primitive values
```
