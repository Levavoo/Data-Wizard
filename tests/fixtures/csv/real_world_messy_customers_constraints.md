# real_world_messy_customers_constraints.json

## Purpose

Constraint configuration for the heavy real-world messy customer CSV fixture.

Fixture:

```text
tests/fixtures/csv/real_world_messy_customers_heavy.csv
```

Constraint file:

```text
tests/fixtures/csv/real_world_messy_customers_constraints.json
```

---

## Design Goal

These constraints are intentionally realistic but not exhaustive.

They are meant to surface important customer-migration problems without trying to validate every possible semantic rule.

---

## Constraints

### `customer_id` required

Purpose:

```text
customer rows must have an identifier
```

Expected to catch:

```text
empty customer IDs
rows where the first field is missing
some footer/summary rows if parsed into customer_id badly
```

---

### `customer_id` unique

Purpose:

```text
customer IDs should not repeat in a CRM migration
```

Expected to catch:

```text
duplicate customer_id 16
```

---

### `email` required

Purpose:

```text
primary email should exist for this migration scenario
```

Expected to catch:

```text
missing email values
whitespace-only email values after cleaning
rows where email column is empty
```

---

### `email` regex

Pattern:

```text
^[^@]+@[^@]+\.[^@]+$
```

Purpose:

```text
primary email should have a basic email-like structure
```

Expected to catch:

```text
invalid-email
dana[at]example.it
missing or malformed emails if required did not catch them first
```

---

### `email` unique

Purpose:

```text
primary email should not repeat in a customer import
```

Expected to catch:

```text
alice@example.com appearing more than once
```

---

### `country` required

Purpose:

```text
country should exist for customer records
```

Expected to catch:

```text
missing country values
blank country rows
some malformed/footer rows if parsed into customer structure
```

---

### `country` allowed values

Allowed values:

```text
Germany
France
Italy
Czechia
Ireland
USA
Russia
Japan
Belgium
Spain
Norway
```

Purpose:

```text
only expected migration countries should pass this fixture's policy
```

Expected to catch:

```text
Atlantis
blank/missing countries if required does not catch first
summary/footer values if parsed into country
```

---

### `amount` min value 0

Purpose:

```text
amount should not be negative
```

Expected to catch:

```text
negative amount row
```

Potential weakness:

```text
currency, percent, and text amount values may fail type parsing before this constraint is meaningful
```

---

### `score` min value 0

Purpose:

```text
score should not be below 0
```

Expected to catch:

```text
negative score row
```

---

### `score` max value 100

Purpose:

```text
score should not exceed 100
```

Expected to catch:

```text
score above 100 row
```

---

## Intentionally Not Included Yet

These are future candidate constraints and intentionally not part of Stage B:

```text
phone validation
postal code validation by country
signup_date required
signup_date date range
active allowed values
notes safety/spreadsheet injection rule
secondary email validation
country normalization database
```

Reason:

```text
Stage B should define realistic baseline constraints without hiding current type and parsing weaknesses.
```

---

## Expected Usage

The constraint file should be used by later Stage 15 tests and observation runs.

Example future command:

```powershell
python scripts\run_csv_pipeline.py `
    tests\fixtures\csv\real_world_messy_customers_heavy.csv `
    data\processed\real_world_messy_customers_clean.csv `
    --constraints-path tests\fixtures\csv\real_world_messy_customers_constraints.json `
    --report-path data\processed\real_world_messy_customers_report.json `
    --html-report-path data\processed\real_world_messy_customers_report.html `
    --quarantine-candidates-path data\processed\real_world_messy_customers_quarantine_candidates.json `
    --quarantine-rows-path data\processed\real_world_messy_customers_quarantine_rows.csv `
    --accepted-rows-path data\processed\real_world_messy_customers_accepted_rows.csv
```
