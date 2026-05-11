from datetime import date
from datetime import datetime

from data_processor.cleaners.dates import (
    clean_table_dates,
    normalize_date,
    normalize_date_or_datetime,
    normalize_datetime,
)
from data_processor.core.column import Column
from data_processor.core.schema import Schema
from data_processor.core.table import Table


def test_normalize_iso_date() -> None:
    """
    Verify ISO date strings become date objects.
    """
    result = normalize_date("2026-01-31")

    assert result == date(2026, 1, 31)


def test_normalize_european_date() -> None:
    """
    Verify European-style dates are parsed.
    """
    result = normalize_date("31.01.2026")

    assert result == date(2026, 1, 31)


def test_normalize_slash_date() -> None:
    """
    Verify slash-separated dates are parsed.
    """
    result = normalize_date("2026/01/31")

    assert result == date(2026, 1, 31)


def test_normalize_datetime() -> None:
    """
    Verify datetime strings become datetime objects.
    """
    result = normalize_datetime("2026-01-31 14:30:00")

    assert result == datetime(2026, 1, 31, 14, 30, 0)


def test_normalize_iso_datetime() -> None:
    """
    Verify ISO datetime strings are parsed.
    """
    result = normalize_datetime("2026-01-31T14:30:00")

    assert result == datetime(2026, 1, 31, 14, 30, 0)


def test_normalize_date_or_datetime_prefers_datetime() -> None:
    """
    Verify datetime parsing is prioritized.
    """
    result = normalize_date_or_datetime("2026-01-31 14:30:00")

    assert isinstance(result, datetime)


def test_preserve_invalid_values() -> None:
    """
    Verify invalid date values remain unchanged.
    """
    assert normalize_date("Alice") == "Alice"
    assert normalize_datetime("not-a-date") == "not-a-date"


def test_preserve_none() -> None:
    """
    Verify None values remain unchanged.
    """
    assert normalize_date(None) is None
    assert normalize_datetime(None) is None


def test_preserve_existing_date_objects() -> None:
    """
    Verify existing date objects remain unchanged.
    """
    existing_date = date(2026, 1, 31)

    assert normalize_date(existing_date) == existing_date


def test_preserve_existing_datetime_objects() -> None:
    """
    Verify existing datetime objects remain unchanged.
    """
    existing_datetime = datetime(2026, 1, 31, 14, 30, 0)

    assert normalize_datetime(existing_datetime) == existing_datetime


def test_clean_table_dates() -> None:
    """
    Verify date normalization across an entire table.
    """
    schema = Schema(
        columns=[
            Column(name="created_at"),
            Column(name="birth_date"),
            Column(name="name"),
        ]
    )

    table = Table(
        name="customers",
        schema=schema,
        rows=[
            {
                "created_at": "2026-01-31 14:30:00",
                "birth_date": "31.01.2026",
                "name": "Alice",
            },
            {
                "created_at": "2026-02-01T10:15:00",
                "birth_date": "2026/02/01",
                "name": "Bob",
            },
        ],
    )

    clean_table_dates(table)

    assert isinstance(
        table.rows[0]["created_at"],
        datetime,
    )

    assert isinstance(
        table.rows[0]["birth_date"],
        date,
    )

    assert isinstance(
        table.rows[1]["created_at"],
        datetime,
    )

    assert isinstance(
        table.rows[1]["birth_date"],
        date,
    )

    assert table.rows[0]["name"] == "Alice"
    assert table.rows[1]["name"] == "Bob"
