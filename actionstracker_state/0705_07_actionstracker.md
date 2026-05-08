Stage 04

data_processor/cleaners/nulls.py
data_processor/cleaners/nulls.md

raw null-like values
→ standardized Python None

""       → None
"null"   → None
"None"   → None
"n/a"    → None
" NA "   → None
"Alice"  → "Alice"

Cleaner rule:

Cleaners may modify values.
Inference only detects types.

Recommended implementation order for Stage 04:

1. nulls.py
2. text.py
3. booleans.py
4. numbers.py
5. dates.py


data_processor/cleaners/nulls.py
data_processor/cleaners/nulls.md
tests/test_nulls.py
tests/test_nulls.md

New-Item data_processor\cleaners\nulls.py
New-Item data_processor\cleaners\nulls.md
New-Item tests\test_nulls.py
New-Item tests\test_nulls.md

ruff check data_processor\cleaners\nulls.py tests\test_nulls.py
black data_processor\cleaners\nulls.py tests\test_nulls.py
pytest tests\test_nulls.py

OR 

pytest tests\test_nulls.py -v
tests/test_nulls.py::test_normalize_empty_string PASSED                                                                       [ 16%]
tests/test_nulls.py::test_normalize_null_string PASSED                                                                        [ 33%]
tests/test_nulls.py::test_normalize_na_values PASSED                                                                          [ 50%]
tests/test_nulls.py::test_preserve_regular_values PASSED                                                                      [ 66%]
tests/test_nulls.py::test_preserve_non_string_values PASSED                                                                   [ 83%]
tests/test_nulls.py::test_clean_table_nulls PASSED                                                                            [100%]
