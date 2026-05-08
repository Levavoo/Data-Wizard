Table
→ inspect raw string values
→ infer likely column type
→ update schema columns

New-Item data_processor\inference\type_inference.py
New-Item data_processor\inference\type_inference.md

New-Item tests\test_type_inference.py
New-Item tests\test_type_inference.md

1. type_inference.py
2. type_inference.md
3. test_type_inference.py
4. test_type_inference.md

Initial supported types:

null
boolean
integer
float
date
datetime
string

Important rule:

Type inference detects likely types.
It does not convert values yet.
So:

"123" → inferred as integer

but the stored row value remains:

"123"


New-Item tests\test_type_inference.py
New-Item tests\test_type_inference.md

ruff check data_processor\inference\type_inference.py tests\test_type_inference.py
black data_processor\inference\type_inference.py tests\test_type_inference.py
pytest