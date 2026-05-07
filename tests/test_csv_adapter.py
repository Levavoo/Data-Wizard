from data_processor.adapters.csv_adapter import CsvAdapter
from data_processor.core.table import Table


def test_csv_adapter_returns_table() -> None:
    """
    Verify that the CSV adapter returns a Table object.
    """
    adapter = CsvAdapter("examples/sample_dirty.csv")

    table = adapter.read()

    assert isinstance(table, Table)


def test_csv_adapter_row_count() -> None:
    """
    Verify row count is parsed correctly.
    """
    adapter = CsvAdapter("examples/sample_dirty.csv")

    table = adapter.read()

    assert table.row_count() == 4


def test_csv_adapter_column_count() -> None:
    """
    Verify schema column count.
    """
    adapter = CsvAdapter("examples/sample_dirty.csv")

    table = adapter.read()

    assert table.column_count() == 4


def test_csv_adapter_normalized_headers() -> None:
    """
    Verify headers are normalized correctly.
    """
    adapter = CsvAdapter("examples/sample_dirty.csv")

    table = adapter.read()

    expected_headers = [
        "customer_id",
        "name",
        "country",
        "active",
    ]

    assert table.schema.column_names() == expected_headers


def test_csv_adapter_preserves_raw_values() -> None:
    """
    Verify values remain raw strings initially.
    """
    adapter = CsvAdapter("examples/sample_dirty.csv")

    table = adapter.read()

    first_row = table.rows[0]

    assert first_row["customer_id"] == "1"
    assert first_row["name"] == "Alice"
    assert first_row["country"] == "Germany"
    assert first_row["active"] == "YES"