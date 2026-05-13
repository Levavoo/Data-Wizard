# Quarantine Export Modes

## Purpose

This document defines explicit quarantine export modes and safety rules.

---

## Default Mode

Default mode remains:

```text
report only
```

Meaning:

```text
cleaned CSV includes all rows
quarantine candidates appear in diagnostic reports
no separate quarantine exports are written
```

---

## Candidate JSON Export

Output:

```text
quarantine_candidates.json
```

Purpose:

```text
machine-readable candidate review file
```

Contains:

```text
candidate_count
summary
candidates
```

---

## Quarantine Rows CSV Export

Output:

```text
quarantine_rows.csv
```

Purpose:

```text
human-review CSV containing only candidate rows
```

Important:

```text
this does not remove rows from the normal cleaned CSV
```

---

## Accepted Rows CSV Export

Output:

```text
accepted_rows.csv
```

Purpose:

```text
explicit split output containing rows not listed as quarantine candidates
```

Important:

```text
this is an additional output, not a replacement for the default cleaned CSV
```

---

## Safety Rules

```text
quarantine export must be explicit
normal cleaned CSV behavior must not change
row indexes must be preserved in candidate JSON
row selection must not mutate the original table
strict mode behavior must not change
```
