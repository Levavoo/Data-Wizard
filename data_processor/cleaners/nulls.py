"""
Null value cleaning utilities.

This module standardizes null-like values into Python None.

Purpose:
- normalize inconsistent missing-value representations
- simplify later validation and processing
- create deterministic null handling
"""

from typing import Any

from data_processor.core.table import Table

NULL_VALUES = {
    "",
    "null",
    "none",
    "n/a",
    "na",
    "nan",
    "-",
}


def normalize_null(value: Any) -> Any:
    """
    Normalize one value into a standard null representation.

    Args:
        value:
            Raw input value.

    Returns:
        None if the value represents null,
        otherwise the original value.
    """
    if value is None:
        return None

    if not isinstance(value, str):
        return value

    cleaned_value = value.strip().lower()

    if cleaned_value in NULL_VALUES:
        return None

    return value


def clean_table_nulls(table: Table) -> None:
    """
    Normalize null-like values across an entire table.

    This function mutates table rows in place.

    Args:
        table:
            Internal dataset table.
    """
    for row in table.rows:
        for column_name, value in row.items():
            row[column_name] = normalize_null(value)
