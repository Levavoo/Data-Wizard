Stage 04.04 — Number Cleaner

raw numeric strings
→ normalized numeric values

"100"
→ 100

"100.50"
→ 100.5

" 1,000 "
→ 1000

"1_000"
→ 1000

None
→ None

Important Design Decision

Separate:

integer normalization
float normalization
generic number normalization

Initial Scope

Support:

- integers
- floats
- surrounding whitespace
- commas
- underscores
- existing numeric types
- None preservation

Do NOT support yet:

- locale-aware numbers
- currency symbols
- percentages
- scientific notation
- decimal precision control
- accounting formats
  
Files To Create
New-Item data_processor\cleaners\numbers.py
New-Item data_processor\cleaners\numbers.md

New-Item tests\test_numbers.py
New-Item tests\test_numbers.md

normalize_integer()
normalize_float()
normalize_number()
clean_table_numbers()


Pipeline Position

Recommended order:

Parsing
→ Null Cleaning
→ Text Cleaning
→ Boolean Cleaning
→ Number Cleaning
→ Type Inference
→ Validation

Number cleaner IS allowed to cast values.