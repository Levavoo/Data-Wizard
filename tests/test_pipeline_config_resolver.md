# test_pipeline_config_resolver.py

## Purpose

Tests config-to-runtime option resolution.

---

## Tested File

```text
data_processor/config/pipeline_config_resolver.py
```

---

## Covered Behavior

- resolves profile defaults
- applies config `strict_mode` override
- preserves optional paths
- converts path strings into `Path` objects
- uses default profile when none is configured

---

## Run Tests

```bash
python -m pytest tests/test_pipeline_config_resolver.py
```

---

## Design Rule

Config resolver tests verify option resolution only.

Pipeline execution and CLI behavior are tested separately.
