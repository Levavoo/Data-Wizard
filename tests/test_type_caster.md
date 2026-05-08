# test_type_caster.py

## Purpose

Tests the type-aware casting module.

This verifies that values are cast based on inferred column type instead of applying every cleaner to every value.

---

# Tested File

```text
data_processor/cleaners/type_caster.py
```

---

# Current Test Coverage

## `test_cast_integer_value`

Verifies:

```text
"1"
→ 1
```

when inferred type is:

```text
integer
```

---

## `test_cast_float_value`

Verifies:

```text
"25.50"
→ 25.5
```

when inferred type is:

```text
float
```

---

## `test_cast_boolean_value`

Verifies:

```text
"yes"
→ True
```

when inferred type is:

```text
boolean
```

---

## `test_cast_date_value`

Verifies date-like strings become Python `date` objects.

---

## `test_preserve_string_value`

Verifies string columns are not cast.

---

## `test_preserve_unknown_type`

Verifies unknown types are preserved unchanged.

---

## `test_preserve_none`

Verifies `None` remains unchanged.

---

## `test_cast_table_by_schema`

Verifies full table casting using schema column types.

---

# Important Design Rule

Casting should be schema-driven.

Correct flow:

```text
clean nulls/text
→ infer types
→ cast by schema
```

This prevents incorrect conversions like:

```text
customer_id = "1"
→ True
```

---

# Run Tests

```powershell
pytest tests\test_type_caster.py
```

---

# Recommended Validation Workflow

```powershell
ruff check `
    data_processor\cleaners\type_caster.py `
    tests\test_type_caster.py

black `
    data_processor\cleaners\type_caster.py `
    tests\test_type_caster.py

pytest tests\test_type_caster.py
```