"""
Date and datetime cleaning utilities.

This module normalizes date-like and datetime-like string values into
Python date and datetime objects.

Purpose:
- standardize date handling
- support controlled datetime parsing
- preserve invalid or unrelated values unchanged
"""

from datetime import date
from datetime import datetime
from typing import Any

from data_processor.core.table import Table

DATE_FORMATS = (
    "%Y-%m-%d",
    "%d.%m.%Y",
    "%Y/%m/%d",
)


DATETIME_FORMATS = (
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M:%S",
)


def normalize_date(value: Any) -> Any:
    """
    Normalize one date-like value.

    Args:
        value:
            Raw input value.

    Returns:
        Python date object if parsing succeeds,
        otherwise the original value.
    """
    if value is None:
        return None

    if isinstance(value, date) and not isinstance(value, datetime):
        return value

    if not isinstance(value, str):
        return value

    cleaned_value = value.strip()

    for date_format in DATE_FORMATS:
        try:
            parsed_date = datetime.strptime(
                cleaned_value,
                date_format,
            )

            return parsed_date.date()

        except ValueError:
            continue

    return value


def normalize_datetime(value: Any) -> Any:
    """
    Normalize one datetime-like value.

    Args:
        value:
            Raw input value.

    Returns:
        Python datetime object if parsing succeeds,
        otherwise the original value.
    """
    if value is None:
        return None

    if isinstance(value, datetime):
        return value

    if not isinstance(value, str):
        return value

    cleaned_value = value.strip()

    for datetime_format in DATETIME_FORMATS:
        try:
            return datetime.strptime(
                cleaned_value,
                datetime_format,
            )

        except ValueError:
            continue

    return value


def normalize_date_or_datetime(value: Any) -> Any:
    """
    Normalize one value into either date or datetime.

    Datetime parsing is attempted first.

    Args:
        value:
            Raw input value.

    Returns:
        date, datetime, or original value.
    """
    datetime_value = normalize_datetime(value)

    if datetime_value != value or isinstance(value, datetime):
        return datetime_value

    return normalize_date(value)


def clean_table_dates(table: Table) -> None:
    """
    Normalize date-like and datetime-like values across an entire table.

    This function mutates table rows in place.

    Args:
        table:
            Internal dataset table.
    """
    for row in table.rows:
        for column_name, value in row.items():
            row[column_name] = normalize_date_or_datetime(value)
