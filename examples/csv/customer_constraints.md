# customer_constraints.json

## Purpose

This file provides example validation rules for the customer migration sample CSV.

It is designed to work with:

```text
examples/csv/customer_migration_sample.csv
```

---

## File

```text
examples/csv/customer_constraints.json
```

---

## Constraints

### Required customer ID

```json
{
  "column": "customer_id",
  "type": "required"
}
```

Checks that each row has a customer ID.

---

### Unique customer ID

```json
{
  "column": "customer_id",
  "type": "unique"
}
```

Checks that customer IDs are not duplicated.

---

### Allowed countries

```json
{
  "column": "country",
  "type": "allowed_values",
  "values": ["Germany", "France", "Spain"]
}
```

Checks that countries belong to the supported list.

---

### Email pattern

```json
{
  "column": "email",
  "type": "regex",
  "pattern": "^[^@]+@[^@]+\\.[^@]+$"
}
```

Checks that email values look like email addresses.

---

### Minimum amount

```json
{
  "column": "amount",
  "type": "min_value",
  "value": 0
}
```

Checks that amount values are not negative.

---

## Important Note

Constraint validation is report-only.

Failed validation rules do not block CSV export by default.
