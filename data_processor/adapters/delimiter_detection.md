# delimiter_detection.py

## Purpose

`delimiter_detection.py` detects a likely delimiter from a CSV text sample.

It is dependency-free and conservative.

---

## Main Function

### `detect_delimiter(text_sample, candidates=None)`

Returns delimiter detection diagnostics.

---

## Default Candidates

```text
,
;
\t
|
```

---

## Returned Diagnostics

```text
selected_delimiter
candidate_scores
confidence
reason
```

---

## Scoring Approach

Candidates are scored by:

```text
whether they produce multi-field rows
consistent row counts
average field count
occurrence count
```

---

## Fallback Policy

If detection is ambiguous or no candidate is viable, the detector falls back to comma.

---

## Design Rules

This module must not:

- read files directly
- parse final CSV rows
- clean values
- mutate data
- rely on external libraries
