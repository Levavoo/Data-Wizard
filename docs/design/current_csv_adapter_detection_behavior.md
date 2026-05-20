# Current CSV Adapter Detection Behavior

## Purpose

This document records the CSV adapter behavior before dedicated encoding and delimiter detection utilities.

---

## Current Encoding Behavior

The adapter currently tries a small built-in encoding list:

```text
utf-8
utf-8-sig
cp1252
```

It returns the first encoding that can read a small sample.

---

## Current Delimiter Behavior

The adapter currently uses `csv.Sniffer().sniff()` over a sample with delimiter candidates:

```text
,
;
\t
|
```

If sniffing fails, it falls back to comma.

---

## Current Diagnostics

Parse diagnostics currently include:

```text
delimiter
encoding
header row index
preamble row count
extra/missing field counts
duplicate headers
empty headers
warnings
```

---

## Gap

Current behavior records selected encoding and delimiter, but does not expose detailed detection diagnostics such as:

```text
candidate results
confidence
reason
override usage
ambiguity handling
```

---

## Design Goal

Dedicated detection utilities should make detection behavior explicit, testable, configurable, and reportable.
