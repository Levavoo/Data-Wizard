# Current Config Input Surface

## Purpose

This document records current config-like CSV pipeline inputs before config-file execution support.

---

## Current Inputs

The CLI currently accepts:

```text
input_path
output_path
--profile
--constraints-path
--report-path
--html-report-path
--quarantine-candidates-path
--quarantine-rows-path
--accepted-rows-path
--strict
--no-strict
```

---

## Existing Config-Like Modules

Profile resolution:

```text
data_processor/config/profile_resolver.py
```

Constraint config loading:

```text
data_processor/validators/constraint_config.py
```

Pipeline execution:

```text
data_processor/core/pipeline.py
```

---

## Config File Candidate Fields

Initial JSON config files should support:

```text
input_path
output_path
profile
constraints_path
report_path
html_report_path
quarantine_candidates_path
quarantine_rows_path
accepted_rows_path
strict_mode
```

---

## Design Rule

Config files should be optional and should not remove support for explicit CLI usage.
