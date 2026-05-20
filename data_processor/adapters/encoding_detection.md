# encoding_detection.py

## Purpose

`encoding_detection.py` detects a readable text encoding for CSV input files.

It is dependency-free and conservative.

---

## Main Function

### `detect_text_encoding(path, candidates=None, sample_size=8192)`

Returns detection diagnostics.

---

## Default Candidate Order

```text
utf-8-sig
utf-8
cp1252
latin-1
```

---

## Returned Diagnostics

```text
selected_encoding
candidate_results
confidence
reason
```

---

## Confidence Labels

```text
high
medium
low
```

---

## Design Rules

This module must not:

- parse CSV rows
- clean data
- mutate files
- rely on external libraries

It only detects a readable text encoding and returns diagnostics.
