"""
Type inference utilities.

This module infers logical column types from raw table values.

Important:
- inference only detects likely types
- values are NOT converted here
- adapters should still return raw strings
"""

from datetime import datetime

from data_processor.core.table import Table

NULL_VALUES = {
    "",
    "null",
    "none",
    "n/a",
    "na",
}


BOOLEAN_VALUES = {
    "true",
    "false",
    "yes",
    "no",
    "y",
    "n",
    "1",
    "0",
}


DATE_FORMATS = (
    "%Y-%m-%d",
    "%d.%m.%Y",
    "%Y/%m/%d",
)


DATETIME_FORMATS = (
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M:%S",
)


def infer_table_types(table: Table) -> None:
    """
    Infer and assign types for all table columns.

    Args:
        table:
            Internal dataset table.
    """
    for column in table.schema.columns:
        values = [row.get(column.name) for row in table.rows]

        inferred_type = infer_column_type(values)

        column.set_type(inferred_type)


def infer_column_type(values: list[object]) -> str:
    """
    Infer the most likely logical type for one column.

    Args:
        values:
            Raw column values.

    Returns:
        Logical type name.
    """
    non_null_values = [value for value in values if not is_null(value)]

    if not non_null_values:
        return "null"

    if all(is_boolean(value) for value in non_null_values):
        return "boolean"

    if all(is_integer(value) for value in non_null_values):
        return "integer"

    if all(is_float(value) for value in non_null_values):
        return "float"

    if all(is_datetime(value) for value in non_null_values):
        return "datetime"

    if all(is_date(value) for value in non_null_values):
        return "date"

    return "string"


def is_null(value: object) -> bool:
    """
    Check whether a value represents null/missing data.

    Args:
        value:
            Raw value.

    Returns:
        True if value should be considered null.
    """
    if value is None:
        return True

    if not isinstance(value, str):
        return False

    return value.strip().lower() in NULL_VALUES


def is_boolean(value: object) -> bool:
    """
    Check whether a value represents a boolean.

    Args:
        value:
            Raw value.

    Returns:
        True if value matches known boolean values.
    """
    if not isinstance(value, str):
        return False

    return value.strip().lower() in BOOLEAN_VALUES


def is_integer(value: object) -> bool:
    """
    Check whether a value represents an integer.

    Args:
        value:
            Raw value.

    Returns:
        True if integer parsing succeeds.
    """
    if not isinstance(value, str):
        return False

    try:
        int(value.strip())
        return True

    except ValueError:
        return False


def is_float(value: object) -> bool:
    """
    Check whether a value represents a float.

    Args:
        value:
            Raw value.

    Returns:
        True if float parsing succeeds.
    """
    if not isinstance(value, str):
        return False

    try:
        float(value.strip())
        return True

    except ValueError:
        return False


def is_date(value: object) -> bool:
    """
    Check whether a value matches supported date formats.

    Args:
        value:
            Raw value.

    Returns:
        True if parsing succeeds.
    """
    if not isinstance(value, str):
        return False

    cleaned_value = value.strip()

    for date_format in DATE_FORMATS:
        try:
            datetime.strptime(cleaned_value, date_format)
            return True

        except ValueError:
            continue

    return False


def is_datetime(value: object) -> bool:
    """
    Check whether a value matches supported datetime formats.

    Args:
        value:
            Raw value.

    Returns:
        True if parsing succeeds.
    """
    if not isinstance(value, str):
        return False

    cleaned_value = value.strip()

    for datetime_format in DATETIME_FORMATS:
        try:
            datetime.strptime(cleaned_value, datetime_format)
            return True

        except ValueError:
            continue

    return False
