Next important foundational step:

Row Profiling

This complements column profiling and becomes critical later for:

validation
quarantine
anomaly detection
migration diagnostics
repair workflows

Create:

New-Item data_processor\analysis\row_profile.py
New-Item data_processor\analysis\row_profile.md

Goal:

analyze row quality
without modifying rows

Recommended first features:

missing_count
missing_ratio
empty_row
duplicate_candidate
column_count
non_null_count

This will later support:

invalid-row quarantine
repair suggestions
confidence scoring
outlier detection

New-Item data_processor\analysis\row_profile.py
New-Item data_processor\analysis\row_profile.md

New-Item tests\test_row_profile.py
New-Item tests\test_row_profile.md

ruff check `
    data_processor\analysis\row_profile.py `
    tests\test_row_profile.py

black `
    data_processor\analysis\row_profile.py `
    tests\test_row_profile.py

pytest tests\test_row_profile.py
pytest