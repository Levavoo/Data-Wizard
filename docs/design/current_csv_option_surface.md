# Current CSV Option Surface

## Purpose

This document records current CSV pipeline and CLI options before cleaning profile support.

---

## Current Pipeline Options

`run_csv_pipeline()` currently supports:

```text
input_path
output_path
report_path
html_report_path
quarantine_candidates_path
quarantine_rows_path
accepted_rows_path
constraints
strict_mode
```

---

## Current CLI Options

`run_csv_pipeline.py` currently supports:

```text
input_path
output_path
--report-path
--html-report-path
--quarantine-candidates-path
--quarantine-rows-path
--accepted-rows-path
--constraints-path
--strict
```

---

## Profile Candidate Options

Cleaning profiles can initially control:

```text
strict_mode default
recommended output types
profile description
workflow intent
```

Profiles should not automatically invent output paths in this stage.

---

## Design Rule

Profiles must simplify workflow selection without changing existing no-profile behavior.
