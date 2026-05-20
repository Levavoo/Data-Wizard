# pipeline_config_resolver.py

## Purpose

`pipeline_config_resolver.py` converts a validated pipeline config dictionary into runtime options.

It belongs to the configuration layer.

Architecture:

```text
validated config
→ profile resolution
→ path conversion
→ runtime options
```

---

## Main Function

### `resolve_pipeline_config_options(config)`

Returns runtime options for CLI/pipeline usage.

---

## Responsibilities

The resolver:

```text
resolves profile defaults
applies config strict_mode override
preserves input_format
preserves configured paths
converts path strings to Path objects
```

---

## Returned Data

Returned fields include:

```text
profile_options
input_format
input_path
output_path
constraints_path
report_path
html_report_path
quarantine_candidates_path
quarantine_rows_path
accepted_rows_path
strict_mode
encoding
delimiter
auto_detect_csv
```

---

## Design Rules

This module must not:

- run the pipeline
- load constraints
- write files
- mutate data
- validate raw config shape

Validation belongs to `pipeline_config.py`.
