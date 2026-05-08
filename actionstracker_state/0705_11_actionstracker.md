data_processor/cleaners/numbers.py
data_processor/cleaners/numbers.md

New-Item tests\test_numbers.py
New-Item tests\test_numbers.md

ruff check data_processor\cleaners\numbers.py tests\test_numbers.py

black data_processor\cleaners\numbers.py tests\test_numbers.py

pytest tests\test_numbers.py

pytest