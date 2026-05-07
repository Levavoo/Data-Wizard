from data_processor.cleaners.booleans import (
    clean_table_booleans,
    normalize_boolean,
)
from data_processor.core.column import Column
from data_processor.core.schema import Schema
from data_processor.core.table import Table


def test_normalize_true_values() -> None:
    """
    Verify true-like values become True.
    """
    assert normalize_boolean("true") is True
    assert normalize_boolean("YES") is True
    assert normalize_boolean(" y ") is True
    assert normalize_boolean("1") is True
    assert normalize_boolean("ON") is True


def test_normalize_false_values() -> None:
    """
    Verify false-like values become False.
    """
    assert normalize_boolean("false") is False
    assert normalize_boolean("NO") is False
    assert normalize_boolean(" n ") is False
    assert normalize_boolean("0") is False
    assert normalize_boolean("OFF") is False


def test_preserve_none() -> None:
    """
    Verify None values remain unchanged.
    """
    assert normalize_boolean(None) is None


def test_preserve_existing_boolean_values() -> None:
    """
    Verify existing bool values remain unchanged.
    """
    assert normalize_boolean(True) is True
    assert normalize_boolean(False) is False


def test_preserve_non_boolean_strings() -> None:
    """
    Verify unrelated strings remain unchanged.
    """
    assert normalize_boolean("Alice") == "Alice"
    assert normalize_boolean("Germany") == "Germany"


def test_preserve_non_string_values() -> None:
    """
    Verify non-string values remain unchanged.
    """
    assert normalize_boolean(123) == 123
    assert normalize_boolean(45.6) == 45.6


def test_clean_table_booleans() -> None:
    """
    Verify boolean normalization across an entire table.
    """
    schema = Schema(
        columns=[
            Column(name="active"),
            Column(name="verified"),
            Column(name="name"),
        ]
    )

    table = Table(
        name="customers",
        schema=schema,
        rows=[
            {
                "active": "YES",
                "verified": "0",
                "name": "Alice",
            },
            {
                "active": "false",
                "verified": "ON",
                "name": "Bob",
            },
        ],
    )

    clean_table_booleans(table)

    assert table.rows[0]["active"] is True
    assert table.rows[0]["verified"] is False

    assert table.rows[1]["active"] is False
    assert table.rows[1]["verified"] is True

    assert table.rows[0]["name"] == "Alice"
    assert table.rows[1]["name"] == "Bob"
