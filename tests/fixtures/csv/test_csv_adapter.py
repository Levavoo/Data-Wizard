from pathlib import Path

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


def test_csv_adapter_duplicate_headers_are_unique(tmp_path: Path) -> None:
    """
    Verify duplicate CSV headers are made unique.
    """
    input_path = tmp_path / "duplicate_headers.csv"

    input_path.write_text(
        "customer_id,name,name,country\n" "1,Alice,Alicia,Germany\n",
        encoding="utf-8",
    )

    adapter = CsvAdapter(input_path)

    table = adapter.read()

    assert table.schema.column_names() == [
        "customer_id",
        "name",
        "name_2",
        "country",
    ]

    assert table.rows[0]["name"] == "Alice"
    assert table.rows[0]["name_2"] == "Alicia"


def test_csv_adapter_empty_headers_are_named(tmp_path: Path) -> None:
    """
    Verify empty headers are converted to unnamed columns.
    """
    input_path = tmp_path / "empty_headers.csv"

    input_path.write_text(
        "customer_id,,country\n" "1,Alice,Germany\n",
        encoding="utf-8",
    )

    adapter = CsvAdapter(input_path)

    table = adapter.read()

    assert table.schema.column_names() == [
        "customer_id",
        "unnamed_column",
        "country",
    ]

    assert table.rows[0]["unnamed_column"] == "Alice"


def test_csv_adapter_duplicate_empty_headers_are_unique(tmp_path: Path) -> None:
    """
    Verify duplicate empty headers are made unique.
    """
    input_path = tmp_path / "duplicate_empty_headers.csv"

    input_path.write_text(
        "customer_id,,\n" "1,Alice,Germany\n",
        encoding="utf-8",
    )

    adapter = CsvAdapter(input_path)

    table = adapter.read()

    assert table.schema.column_names() == [
        "customer_id",
        "unnamed_column",
        "unnamed_column_2",
    ]

    assert table.rows[0]["unnamed_column"] == "Alice"
    assert table.rows[0]["unnamed_column_2"] == "Germany"


def test_csv_adapter_short_rows_fill_missing_values(tmp_path: Path) -> None:
    """
    Verify short rows are padded with None values.
    """
    input_path = tmp_path / "short_rows.csv"

    input_path.write_text(
        "customer_id,name,country\n" "1,Alice\n",
        encoding="utf-8",
    )

    adapter = CsvAdapter(input_path)

    table = adapter.read()

    assert table.rows[0]["customer_id"] == "1"
    assert table.rows[0]["name"] == "Alice"
    assert table.rows[0]["country"] is None


def test_csv_adapter_extra_fields_are_ignored(tmp_path: Path) -> None:
    """
    Verify extra row fields beyond headers are ignored for now.
    """
    input_path = tmp_path / "extra_fields.csv"

    input_path.write_text(
        "customer_id,name\n" "1,Alice\n" "2,Bob,Germany\n" "3,Charlie\n",
        encoding="utf-8",
    )

    adapter = CsvAdapter(input_path)

    table = adapter.read()

    assert table.schema.column_names() == [
        "customer_id",
        "name",
    ]

    assert table.rows[1] == {
        "customer_id": "2",
        "name": "Bob",
    }


def test_csv_adapter_stores_parser_metadata(tmp_path: Path) -> None:
    """
    Verify adapter stores parser metadata on the table.
    """
    input_path = tmp_path / "metadata.csv"

    input_path.write_text(
        "customer_id;name\n" "1;Alice\n",
        encoding="utf-8",
    )

    adapter = CsvAdapter(input_path)

    table = adapter.read()

    assert table.metadata["source_format"] == "csv"
    assert table.metadata["encoding"] == "utf-8"
    assert table.metadata["delimiter"] == ";"
    assert table.metadata["header_row_index"] == 0
    assert table.metadata["preamble_rows"] == []


def test_csv_adapter_detects_header_after_preamble(tmp_path: Path) -> None:
    """
    Verify metadata rows before the real header are preserved as preamble rows.
    """
    input_path = tmp_path / "metadata_before_header.csv"

    input_path.write_text(
        "Export generated by System X\n"
        "Generated at: 2026-05-08\n"
        "Department: Sales\n"
        "customer_id,name,country,active,amount\n"
        "1,Alice,Germany,true,100\n"
        "2,Bob,France,false,250.50\n",
        encoding="utf-8",
    )

    adapter = CsvAdapter(input_path)

    table = adapter.read()

    assert table.schema.column_names() == [
        "customer_id",
        "name",
        "country",
        "active",
        "amount",
    ]

    assert table.row_count() == 2

    assert table.rows[0]["customer_id"] == "1"
    assert table.rows[0]["name"] == "Alice"

    assert table.metadata["header_row_index"] == 3
    assert table.metadata["preamble_rows"] == [
        ["Export generated by System X"],
        ["Generated at: 2026-05-08"],
        ["Department: Sales"],
    ]
