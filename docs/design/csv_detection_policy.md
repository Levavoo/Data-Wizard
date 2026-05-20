# CSV Detection Policy

## Purpose

This document defines conservative encoding and delimiter detection policy.

---

## Encoding Policy

Default candidate order:

```text
utf-8-sig
utf-8
cp1252
latin-1
```

Policy:

```text
explicit encoding overrides detection
UTF-8 compatible encodings are preferred
UTF-8 BOM should be handled safely
fallback encodings are limited and documented
latin-1 is last because it accepts nearly any byte sequence
```

---

## Delimiter Policy

Default delimiter candidates:

```text
,
;
\t
|
```

Policy:

```text
explicit delimiter overrides detection
consistent row field counts are preferred
delimiters producing only one field are weak candidates
ambiguous detection falls back to comma
fallback behavior is reported
```

---

## Override Precedence

```text
CLI explicit value
→ config explicit value
→ auto-detection
→ safe fallback
```

---

## Safety Rules

Detection must not:

```text
remove rows
repair malformed rows silently
change cleaning semantics
hide ambiguity
require external dependencies
```

---

## Diagnostics Rule

Detection should report:

```text
selected value
candidate results or scores
confidence
reason
overrides used
```
