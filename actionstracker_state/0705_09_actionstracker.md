Stage 04.03 — Boolean Cleaner

raw boolean-like values
→ Python bool

"yes"   → True
"Y"     → True
"1"     → True
"no"    → False
"N"     → False
"0"     → False
None    → None
"Alice" → "Alice"

New-Item data_processor\cleaners\booleans.py
New-Item data_processor\cleaners\booleans.md

New-Item tests\test_booleans.py
New-Item tests\test_booleans.md

Recommended order:

1. booleans.py
2. booleans.md
3. test_booleans.py
4. test_booleans.md
5. run module tests
6. run full test suite

Pipeline position:

Parsing
→ Null Cleaning
→ Text Cleaning
→ Boolean Cleaning
→ Type Inference
→ Validation

New-Item tests\test_booleans.py
New-Item tests\test_booleans.md

ruff check data_processor\cleaners\booleans.py tests\test_booleans.py

black data_processor\cleaners\booleans.py tests\test_booleans.py

pytest tests\test_booleans.py

pytest

git add .

git commit -m "Implement boolean cleaning module"

git push