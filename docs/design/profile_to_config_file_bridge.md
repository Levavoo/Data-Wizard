# Profile to Config File Bridge

## Purpose

This document explains how built-in cleaning profiles relate to future config-file pipeline execution.

---

## Current Stage

Stage 12 adds built-in profiles.

Current profile source:

```text
Python built-in definitions
```

Current CLI usage:

```text
--profile migration_audit
```

---

## Next Stage

Stage 13 is expected to add config-file pipeline execution.

Expected future usage:

```text
python scripts/run_csv_pipeline.py --config configs/customer_migration.json
```

---

## Future Relationship

A config file may eventually reference a profile:

```json
{
  "profile": "migration_audit",
  "input_path": "data/raw/customers.csv",
  "output_path": "data/processed/customers_clean.csv"
}
```

Then explicit config values can override profile defaults.

---

## Design Rule

Built-in profiles are a first step.

External profile files and full pipeline config files are deferred to Stage 13.
