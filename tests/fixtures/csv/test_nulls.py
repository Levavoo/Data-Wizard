from data_processor.cleaners.nulls import (
    clean_table_nulls,
    normalize_null,
)
from data_processor.core.column import Column
from data_processor.core.schema import Schema
from data_processor.core.table import Table


def test_normalize_empty_string() -> None:
    """
    Verify empty strings become None.
    """
    assert normalize_null("") is None


def test_normalize_null_string() -> None:
    """
    Verify textual null values become None.
    """
    assert normalize_null("null") is None
    assert normalize_null("NULL") is None
    assert normalize_null(" None ") is None


def test_normalize_na_values() -> None:
    """
    Verify NA-style values become None.
    """
    assert normalize_null("n/a") is None
    assert normalize_null("NA") is None
    assert normalize_null(" nan ") is None


def test_preserve_regular_values() -> None:
    """
    Verify normal values remain unchanged.
    """
    assert normalize_null("Alice") == "Alice"
    assert normalize_null("Germany") == "Germany"


def test_preserve_non_string_values() -> None:
    """
    Verify non-string values are preserved.
    """
    assert normalize_null(123) == 123
    assert normalize_null(True) is True


def test_clean_table_nulls() -> None:
    """
    Verify null normalization across an entire table.
    """
    schema = Schema(
        columns=[
            Column(name="name"),
            Column(name="country"),
            Column(name="email"),
        ]
    )

    table = Table(
        name="customers",
        schema=schema,
        rows=[
            {
                "name": "Alice",
                "country": "",
                "email": "N/A",
            },
            {
                "name": "Bob",
                "country": "Germany",
                "email": "bob@example.com",
            },
        ],
    )

    clean_table_nulls(table)

    assert table.rows[0]["country"] is None
    assert table.rows[0]["email"] is None

    assert table.rows[1]["country"] == "Germany"
    assert table.rows[1]["email"] == "bob@example.com"
