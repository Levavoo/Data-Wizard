# cleaning_profiles.py

## Purpose

`cleaning_profiles.py` defines built-in CSV cleaning profiles.

Profiles are reusable workflow defaults.

They do not run the pipeline or mutate data.

---

## Built-In Profiles

Current profiles:

```text
default
light_touch
migration_audit
strict_crm
```

---

## Profile Fields

Each profile contains:

```text
name
description
strict_mode
recommended_outputs
notes
```

---

## Functions

### `get_builtin_profile(profile_name)`

Returns a built-in profile by name.

Raises `ValueError` for unknown profiles.

---

### `list_builtin_profile_names()`

Returns sorted available profile names.

---

## Design Rules

Profiles must not:

- run the pipeline
- mutate rows
- export files
- generate output paths automatically

Profiles only define reusable defaults.
