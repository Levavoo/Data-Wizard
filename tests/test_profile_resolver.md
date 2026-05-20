# test_profile_resolver.py

## Purpose

Tests cleaning profile resolution.

---

## Tested File

```text
data_processor/config/profile_resolver.py
```

---

## Covered Behavior

- default profile resolution
- known profile resolution
- explicit override precedence
- ignoring `None` overrides
- unknown profile error handling

---

## Run Tests

```bash
python -m pytest tests/test_profile_resolver.py
```

---

## Design Rule

Resolver tests verify configuration behavior only.

Pipeline and CLI behavior are tested separately.
