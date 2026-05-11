# Number Format Policy

## Purpose

This document defines supported number format policies for numeric normalization.

---

## Supported Policies

```text
auto
us
eu
```

---

## `auto`

Detects likely number format from one value.

Examples:

```text
1.000,50 → EU
250,75 → EU
1,000.50 → US
```

Auto mode is the default.

---

## `us`

Parses US-style numbers.

Examples:

```text
1,000.50 → 1000.5
250.75 → 250.75
```

---

## `eu`

Parses European-style numbers.

Examples:

```text
1.000,50 → 1000.5
250,75 → 250.75
```

---

## Ambiguous Values

Some values are ambiguous when viewed alone.

Examples:

```text
1,234
1.234
```

These may mean different things depending on locale.

Column-level detection should be designed separately.

---

## Architecture Rule

Number format handling belongs in the cleaner/type layer, not in CSV adapters.
