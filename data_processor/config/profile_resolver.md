# profile_resolver.py

## Purpose

`profile_resolver.py` combines a built-in profile and explicit overrides into one resolved option dictionary.

It belongs to the configuration layer.

Architecture:

```text
profile name + overrides
→ profile resolver
→ resolved options
```

---

## Main Function

### `resolve_profile_options(profile_name, overrides=None)`

Returns resolved profile options.

If `profile_name` is `None`, the `default` profile is used.

---

## Override Policy

Explicit override values replace profile defaults.

Override values set to `None` are ignored.

---

## Returned Fields

Current fields:

```text
profile_name
profile_description
strict_mode
recommended_outputs
profile_notes
```

---

## Design Rules

This module must not:

- run the pipeline
- write files
- mutate data
- load external config files

External config files are deferred to Stage 13.
