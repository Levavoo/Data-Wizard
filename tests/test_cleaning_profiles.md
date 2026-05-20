# test_cleaning_profiles.py

## Purpose

Tests built-in CSV cleaning profile definitions.

---

## Tested File

```text
data_processor/config/cleaning_profiles.py
```

---

## Covered Behavior

- available profile names
- default profile behavior
- strict CRM profile behavior
- unknown profile error handling

---

## Run Tests

```bash
python -m pytest tests/test_cleaning_profiles.py
```

---

## Design Rule

Profile definition tests verify data definitions only.

Pipeline and CLI behavior are tested separately.
