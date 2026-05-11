from data_processor.cleaners.text import (
    clean_table_text,
    normalize_text,
)
from data_processor.core.column import Column
from data_processor.core.schema import Schema
from data_processor.core.table import Table


def test_trim_whitespace() -> None:
    """
    Verify surrounding whitespace is removed.
    """
    assert normalize_text(" Alice ") == "Alice"


def test_collapse_repeated_whitespace() -> None:
    """
    Verify repeated internal whitespace is collapsed.
    """
    assert normalize_text("hello     world") == "hello world"


def test_lowercase_normalization() -> None:
    """
    Verify lowercase normalization.
    """
    assert normalize_text("GERMANY", case="lower") == "germany"


def test_uppercase_normalization() -> None:
    """
    Verify uppercase normalization.
    """
    assert normalize_text("de", case="upper") == "DE"


def test_titlecase_normalization() -> None:
    """
    Verify title case normalization.
    """
    assert normalize_text("john doe", case="title") == "John Doe"


def test_preserve_none() -> None:
    """
    Verify None values are preserved.
    """
    assert normalize_text(None) is None


def test_preserve_non_string_values() -> None:
    """
    Verify non-string values remain unchanged.
    """
    assert normalize_text(123) == 123
    assert normalize_text(True) is True


def test_invalid_case_option() -> None:
    """
    Verify invalid case options raise ValueError.
    """
    try:
        normalize_text("Alice", case="invalid")

    except ValueError:
        assert True
        return

    assert False, "Expected ValueError was not raised."


def test_clean_table_text() -> None:
    """
    Verify text normalization across an entire table.
    """
    schema = Schema(
        columns=[
            Column(name="name"),
            Column(name="country"),
        ]
    )

    table = Table(
        name="customers",
        schema=schema,
        rows=[
            {
                "name": " Alice ",
                "country": " GERMANY ",
            },
            {
                "name": " Bob ",
                "country": " france ",
            },
        ],
    )

    clean_table_text(table, case="lower")

    assert table.rows[0]["name"] == "alice"
    assert table.rows[0]["country"] == "germany"

    assert table.rows[1]["name"] == "bob"
    assert table.rows[1]["country"] == "france"
