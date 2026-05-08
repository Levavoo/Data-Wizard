Stage 04.02 — Text Cleaner

raw text values
→ normalized text values

" Alice "
→ "Alice"

"GERMANY"
→ "germany"

"   hello   world   "
→ "hello world"

This cleaner should focus only on generic text normalization.

NOT:

- category mapping
- translation
- semantic normalization
- spell correction
  
New-Item data_processor\cleaners\text.py
New-Item data_processor\cleaners\text.md

New-Item tests\test_text.py
New-Item tests\test_text.md

Implement:

- trim whitespace
- collapse repeated whitespace
- lowercase option
- uppercase option
- preserve None values
- table-wide cleaning

Do NOT implement yet:

- unicode normalization
- transliteration
- locale-aware casing
- fuzzy matching

Architectural Rule

Text cleaner modifies values.

Example:

" Germany "
→ "Germany"

This is different from inference modules.

normalize_text()
clean_table_text()

Important Design Decision

Make casing configurable.

Example:

normalize_text(value, case="lower")
normalize_text(value, case="upper")
normalize_text(value, case=None)

Pipeline Position
CSV
→ Table
→ Null Cleaning
→ Text Cleaning
→ Type Inference
→ Validation


New-Item tests\test_text.py
New-Item tests\test_text.md

ruff check data_processor\cleaners\text.py tests\test_text.py

black data_processor\cleaners\text.py tests\test_text.py

pytest tests\test_text.py


git add .
git commit -m "Stage 04 cleaners Null Text"