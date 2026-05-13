# CLI Exit Codes

## Purpose

This document defines CSV pipeline CLI exit codes.

---

## Current Exit Codes

```text
0 = successful execution
1 = execution error
2 = strict policy failure
```

---

## Exit Code 0

Used when the command executes successfully.

This includes non-strict runs where diagnostics report validation failures, quarantine candidates, or warnings.

---

## Exit Code 1

Used when the command itself cannot complete successfully.

Examples:

```text
input file is missing
constraint file is invalid JSON
unexpected exception occurs
```

---

## Exit Code 2

Used when strict mode is enabled and serious policy failures are reported.

Examples:

```text
validation failures exist
error-level quarantine candidates exist
```

Important:

```text
Exit code 2 means processing completed but strict policy failed.
```

---

## Deferred Exit Codes

Possible future codes:

```text
3 = invalid CLI/config input
4 = input file/access error
```

These are not implemented yet.
