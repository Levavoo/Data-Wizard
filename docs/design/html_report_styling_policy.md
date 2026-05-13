# HTML Report Styling Policy

## Purpose

This document defines styling rules for the static HTML diagnostic report.

---

## Current Policy

The HTML report should use:

```text
static inline CSS
no JavaScript
no external assets
browser-readable layout
print-friendly layout
```

---

## Why Inline CSS

Inline CSS keeps the report self-contained.

A single `.html` file can be opened, shared, archived, or attached without extra assets.

---

## Accessibility Goals

Initial goals:

```text
plain readable fonts
high contrast text
tables with clear borders
sections with clear headings
preformatted blocks for nested data
```

---

## Print Goals

The report should be printable from the browser.

Current print behavior:

```text
reduced page margins
avoid page breaks inside sections where possible
```

---

## Out Of Scope

Current HTML reports do not use:

```text
JavaScript
external CSS frameworks
external images
interactive charts
remote assets
```
