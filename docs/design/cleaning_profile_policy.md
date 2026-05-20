# Cleaning Profile Policy

## Purpose

Cleaning profiles define reusable CSV workflow defaults.

They help users select a workflow intention without remembering every individual CLI option.

---

## Initial Profile Scope

Initial profiles can define:

```text
name
description
strict_mode
recommended_outputs
notes
```

---

## Out Of Initial Scope

The first profile implementation does not control:

```text
null policy
number policy
encoding policy
delimiter policy
row classification policy
custom strict policy
```

These fields are future candidates.

---

## Override Policy

Explicit CLI options override profile defaults.

Example:

```text
--profile strict_crm --no-strict
```

means:

```text
use the strict_crm workflow defaults, but disable strict mode explicitly
```

---

## Output Path Policy

Profiles can recommend output types but do not generate output paths in this stage.

Reason:

```text
automatic path generation should be handled by the future config-file pipeline stage
```

---

## Safety Policy

Profiles must not:

- remove rows automatically
- mutate data by themselves
- hide diagnostics
- silently create files without explicit paths

---

## Future Profile Fields

Possible future fields:

```text
null_policy
number_policy
encoding_policy
delimiter_policy
strict_policy
quarantine_policy
output_path_template
```
