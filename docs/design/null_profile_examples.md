# Null Profile Examples

## Purpose

This document gives examples for future null-token cleaning profiles.

Profiles should make null handling explicit and reusable.

---

## Strict Migration Profile

Use when preparing data for a strict import where placeholder-like values should usually become missing values.

```python
{
    "name": "strict_migration",
    "extra_null_tokens": [
        "unknown",
        "missing",
        "not provided"
    ]
}
```

Expected behavior:

```text
unknown → None
missing → None
not provided → None
```

---

## Survey Profile

Use when survey answers such as `unknown` may be meaningful responses.

```python
{
    "name": "survey",
    "preserve_tokens": ["unknown"],
    "extra_null_tokens": ["not answered", "skipped"]
}
```

Expected behavior:

```text
unknown → "unknown"
not answered → None
skipped → None
```

---

## CRM Migration Profile

Use when customer contact fields often use placeholder values.

```python
{
    "name": "crm_migration",
    "columns": {
        "email": {
            "extra_null_tokens": ["unknown", "missing", "not provided"]
        },
        "phone": {
            "extra_null_tokens": ["unknown", "missing", "not provided"]
        },
        "status": {
            "preserve_tokens": ["unknown"]
        }
    }
}
```

Expected behavior:

```text
email = unknown → None
phone = missing → None
status = unknown → "unknown"
```

---

## ERP Import Profile

Use when importing operational data where placeholders differ by field.

```python
{
    "name": "erp_import",
    "columns": {
        "supplier_id": {
            "extra_null_tokens": ["missing", "not assigned"]
        },
        "item_status": {
            "preserve_tokens": ["unknown", "missing"]
        }
    }
}
```

---

## Financial Import Profile

Use when numeric columns should treat placeholder values as missing but category columns should preserve labels.

```python
{
    "name": "financial_import",
    "columns": {
        "amount": {
            "extra_null_tokens": ["missing", "unknown", "not available"]
        },
        "currency": {
            "preserve_tokens": ["unknown"]
        }
    }
}
```

---

## Notes

These profiles are design examples only.

They are not implemented yet.
