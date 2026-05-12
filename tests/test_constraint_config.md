# test_constraint_config.py

## Purpose

Tests the constraint configuration loader.

These tests verify that machine-readable constraint dictionaries can be converted into `Constraint` objects.

---

## Tested File

```text
data_processor/validators/constraint_config.py
```

---

## Covered Behavior

- required constraint config
- allowed values constraint config
- regex alias normalization
- min/max value constraints
- invalid top-level config type
- missing column field
- missing type field
- unsupported constraint type
- missing required value fields

---

## Run Tests

```bash
python -m pytest tests/test_constraint_config.py
```

---

## Design Rule

The config loader only converts config into constraint objects.

It does not validate table rows or mutate data.
