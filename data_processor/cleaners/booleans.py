"""
Boolean cleaning utilities.

This module normalizes boolean-like values into Python bool values.

Purpose:
- standardize inconsistent boolean representations
- simplify filtering and validation
- create deterministic boolean handling
"""

from typing import Any

from data_processor.core.table import Table

TRUE_VALUES = {
    "true",
    "yes",
    "y",
    "1",
    "on",
}


FALSE_VALUES = {
    "false",
    "no",
    "n",
    "0",
    "off",
}


def normalize_boolean(value: Any) -> Any:
    """
    Normalize one boolean-like value.

    Args:
        value:
            Raw input value.

    Returns:
        True, False, or the original value.
    """
    if value is None:
        return None

    if isinstance(value, bool):
        return value

    if not isinstance(value, str):
        return value

    cleaned_value = value.strip().lower()

    if cleaned_value in TRUE_VALUES:
        return True

    if cleaned_value in FALSE_VALUES:
        return False

    return value


def clean_table_booleans(table: Table) -> None:
    """
    Normalize boolean-like values across an entire table.

    This function mutates table rows in place.

    Args:
        table:
            Internal dataset table.
    """
    for row in table.rows:
        for column_name, value in row.items():
            row[column_name] = normalize_boolean(value)
