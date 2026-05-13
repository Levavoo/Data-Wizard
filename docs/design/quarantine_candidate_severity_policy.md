# Quarantine Candidate Severity Policy

## Purpose

This document defines deterministic severity levels for quarantine candidates.

---

## Severity Levels

Current levels:

```text
info
warning
error
```

---

## Initial Mapping

```text
validation failure → error
mixed-type invalid value → warning
suspicious row classification → warning
```

---

## Error Severity

Use `error` when a row violates explicit validation rules.

Examples:

```text
invalid required value
duplicate ID
invalid email
unsupported allowed value
amount below minimum
```

---

## Warning Severity

Use `warning` when a row may require review but does not directly violate a configured constraint.

Examples:

```text
summary row
footer row
garbage row
mixed-type invalid value
```

---

## Info Severity

Reserved for future low-priority review signals.

No current candidate source maps to `info`.

---

## Candidate Severity Rule

A candidate can have multiple reasons.

The candidate severity is the highest severity among its reasons.

Order:

```text
error > warning > info
```

---

## Export Policy

Severity does not block CSV export by default.

Export blocking is deferred to future strict mode work.
