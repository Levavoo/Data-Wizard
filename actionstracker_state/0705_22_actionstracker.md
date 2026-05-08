New-Item data_processor\analysis\column_profile.py
New-Item data_processor\analysis\column_profile.md

New-Item tests\test_column_profile.py
New-Item tests\test_column_profile.md

ruff check `
    data_processor\analysis\column_profile.py `
    tests\test_column_profile.py

black `
    data_processor\analysis\column_profile.py `
    tests\test_column_profile.py

pytest tests\test_column_profile.py
pytest