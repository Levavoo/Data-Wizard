# test_pipeline_config.py

## Purpose

Tests CSV pipeline JSON config loading and validation.

---

## Tested File

```text
data_processor/config/pipeline_config.py
```

---

## Covered Behavior

- accepts valid config dictionaries
- loads UTF-8 JSON config files
- rejects missing required fields
- rejects unknown fields
- rejects non-boolean `strict_mode`
- rejects non-object config content

---

## Run Tests

```bash
python -m pytest tests/test_pipeline_config.py
```

---

## Design Rule

Config loader tests verify loading and validation only.

Pipeline execution and CLI behavior are tested separately.
