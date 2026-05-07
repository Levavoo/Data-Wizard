"""
Number cleaning utilities.

This module normalizes numeric string values into Python int or float values.

Purpose:
- standardize numeric values
- support controlled numeric casting
- preserve invalid or unrelated values unchanged
"""

from typing import Any

from data_processor.core.table import Table


def normalize_integer(value: Any) -> Any:
    """
    Normalize one integer-like value.

    Args:
        value:
            Raw input value.

    Returns:
        Integer value if conversion succeeds,
        otherwise the original value.
    """
    if value is None:
        return None

    if isinstance(value, bool):
        return value

    if isinstance(value, int):
        return value

    if not isinstance(value, str):
        return value

    cleaned_value = _clean_numeric_string(value)

    if not cleaned_value:
        return value

    try:
        return int(cleaned_value)

    except ValueError:
        return value


def normalize_float(value: Any) -> Any:
    """
    Normalize one float-like value.

    Args:
        value:
            Raw input value.

    Returns:
        Float value if conversion succeeds,
        otherwise the original value.
    """
    if value is None:
        return None

    if isinstance(value, bool):
        return value

    if isinstance(value, float):
        return value

    if isinstance(value, int):
        return float(value)

    if not isinstance(value, str):
        return value

    cleaned_value = _clean_numeric_string(value)

    if not cleaned_value:
        return value

    try:
        return float(cleaned_value)

    except ValueError:
        return value


def normalize_number(value: Any) -> Any:
    """
    Normalize one numeric-like value.

    Integers are preferred when possible.
    Floats are used when integer conversion fails.

    Args:
        value:
            Raw input value.

    Returns:
        int, float, or the original value.
    """
    integer_value = normalize_integer(value)

    if integer_value != value or isinstance(value, int):
        return integer_value

    return normalize_float(value)


def clean_table_numbers(table: Table) -> None:
    """
    Normalize numeric-like values across an entire table.

    This function mutates table rows in place.

    Args:
        table:
            Internal dataset table.
    """
    for row in table.rows:
        for column_name, value in row.items():
            row[column_name] = normalize_number(value)


def _clean_numeric_string(value: str) -> str:
    """
    Prepare a numeric string for parsing.

    Args:
        value:
            Raw string value.

    Returns:
        Cleaned numeric string.
    """
    return value.strip().replace(",", "").replace("_", "")
