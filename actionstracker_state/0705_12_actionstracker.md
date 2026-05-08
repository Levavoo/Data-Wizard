Stage 04.05 — Date Cleaner

New-Item data_processor\cleaners\dates.py
New-Item data_processor\cleaners\dates.md

raw date strings
→ Python date/datetime objects

2026-01-31
31.01.2026
2026/01/31
2026-01-31 14:30:00
2026-01-31T14:30:00

normalize_date()
normalize_datetime()
normalize_date_or_datetime()
clean_table_dates()

New-Item tests\test_dates.py
New-Item tests\test_dates.md

ruff check data_processor\cleaners\dates.py tests\test_dates.py

black data_processor\cleaners\dates.py tests\test_dates.py

pytest tests\test_dates.py

pytest

git add .

git commit -m "Implement date cleaning module"