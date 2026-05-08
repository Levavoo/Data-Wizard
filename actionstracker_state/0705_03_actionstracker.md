CSV file
→ parse safely
→ convert into internal Table

New-Item data_processor\adapters\base_adapter.py
New-Item data_processor\adapters\base_adapter.md

New-Item data_processor\adapters\csv_adapter.py
New-Item data_processor\adapters\csv_adapter.md

- check file existence
- detect encoding fallback
- detect delimiter
- parse CSV
- normalize headers minimally
- create Columns
- create Table
- return Table
  
NOT responsible for:

- cleaning values
- validation
- schema inference
- transformations
- exporting

Recommended CSV Adapter Flow
CSV file
→ detect encoding
→ open file safely
→ detect delimiter
→ parse rows
→ normalize headers
→ create Schema
→ create Table
→ return Table

Do NOT use pandas here.

Reason:

You are building a controlled canonical cleaning engine.

Using pandas too early causes:

CSV
→ pandas assumptions
→ implicit type coercion
→ hidden null handling
→ hidden datetime parsing
→ hidden normalization

You lose control over the cleaning pipeline.

Use standard library first:

csv
pathlib
typing

Recommended Initial CSV Scope

Support:

UTF-8
UTF-8-SIG
fallback cp1252
comma delimiter
semicolon delimiter
quoted values
basic malformed-file errors


CSV:

Customer ID,Name,Country
1,Alice,Germany
2,Bob,France

Should become:

Table(
    name="customers",
    schema=Schema(
        columns=[
            Column(name="customer_id"),
            Column(name="name"),
            Column(name="country")
        ]
    ),
    rows=[
        {
            "customer_id": "1",
            "name": "Alice",
            "country": "Germany"
        },
        {
            "customer_id": "2",
            "name": "Bob",
            "country": "France"
        }
    ]
)

ALL VALUES STAY AS RAW STRINGS INITIALLY