from data_processor.cleaners.numbers import (
    clean_table_numbers,
    normalize_float,
    normalize_integer,
    normalize_number,
)
from data_processor.core.column import Column
from data_processor.core.schema import Schema
from data_processor.core.table import Table


def test_normalize_integer_basic() -> None:
    """
    Verify integer-like strings become int.
    """
    assert normalize_integer("100") == 100
    assert normalize_integer(" 42 ") == 42


def test_normalize_integer_with_commas() -> None:
    """
    Verify commas are removed before integer parsing.
    """
    assert normalize_integer("1,000") == 1000


def test_normalize_integer_with_underscores() -> None:
    """
    Verify underscores are removed before integer parsing.
    """
    assert normalize_integer("1_000") == 1000


def test_normalize_float_basic() -> None:
    """
    Verify float-like strings become float.
    """
    assert normalize_float("100.5") == 100.5
    assert normalize_float(" 42.25 ") == 42.25


def test_normalize_float_with_commas() -> None:
    """
    Verify commas are removed before float parsing.
    """
    assert normalize_float("1,000.50") == 1000.5


def test_normalize_number_prefers_integer() -> None:
    """
    Verify integer conversion is preferred.
    """
    assert normalize_number("100") == 100


def test_normalize_number_uses_float_when_needed() -> None:
    """
    Verify float conversion is used when integer fails.
    """
    assert normalize_number("100.25") == 100.25


def test_preserve_invalid_values() -> None:
    """
    Verify invalid numeric values remain unchanged.
    """
    assert normalize_number("Alice") == "Alice"
    assert normalize_number("100 EUR") == "100 EUR"


def test_preserve_none() -> None:
    """
    Verify None values remain unchanged.
    """
    assert normalize_number(None) is None


def test_preserve_booleans() -> None:
    """
    Verify bool values remain unchanged.
    """
    assert normalize_number(True) is True
    assert normalize_number(False) is False


def test_clean_table_numbers() -> None:
    """
    Verify number normalization across an entire table.
    """
    schema = Schema(
        columns=[
            Column(name="quantity"),
            Column(name="price"),
            Column(name="name"),
        ]
    )

    table = Table(
        name="products",
        schema=schema,
        rows=[
            {
                "quantity": "1,000",
                "price": "25.50",
                "name": "Widget",
            },
            {
                "quantity": "250",
                "price": "100",
                "name": "Tool",
            },
        ],
    )

    clean_table_numbers(table)

    assert table.rows[0]["quantity"] == 1000
    assert table.rows[0]["price"] == 25.5

    assert table.rows[1]["quantity"] == 250
    assert table.rows[1]["price"] == 100

    assert table.rows[0]["name"] == "Widget"
    assert table.rows[1]["name"] == "Tool"
