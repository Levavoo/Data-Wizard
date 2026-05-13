from pathlib import Path

from data_processor.adapters.csv_adapter import CsvAdapter


def test_csv_adapter_detects_semicolon_delimiter(tmp_path: Path) -> None:
    input_path = tmp_path / "semicolon.csv"
    input_path.write_text(
        "customer_id;name;country\n1;Alice;Germany\n",
        encoding="utf-8",
    )

    table = CsvAdapter(input_path).read()

    assert table.schema.column_names() == ["customer_id", "name", "country"]
    assert table.rows[0]["name"] == "Alice"
    assert table.metadata["delimiter"] == ";"
    assert table.metadata["parse_diagnostics"]["detection"]["delimiter"][
        "selected_delimiter"
    ] == ";"


def test_csv_adapter_uses_explicit_delimiter_override(tmp_path: Path) -> None:
    input_path = tmp_path / "pipe.csv"
    input_path.write_text(
        "customer_id|name|country\n1|Alice|Germany\n",
        encoding="utf-8",
    )

    table = CsvAdapter(input_path, delimiter="|").read()

    assert table.schema.column_names() == ["customer_id", "name", "country"]
    assert table.metadata["delimiter"] == "|"
    assert table.metadata["parse_diagnostics"]["detection"]["delimiter"][
        "confidence"
    ] == "override"


def test_csv_adapter_handles_utf8_bom_header(tmp_path: Path) -> None:
    input_path = tmp_path / "bom.csv"
    input_path.write_text(
        "customer_id,name\n1,Alice\n",
        encoding="utf-8-sig",
    )

    table = CsvAdapter(input_path).read()

    assert table.schema.column_names() == ["customer_id", "name"]
    assert table.metadata["encoding"] == "utf-8-sig"
    assert table.metadata["parse_diagnostics"]["detection"]["encoding"][
        "selected_encoding"
    ] == "utf-8-sig"


def test_csv_adapter_uses_explicit_encoding_override(tmp_path: Path) -> None:
    input_path = tmp_path / "cp1252.csv"
    input_path.write_bytes("name,city\nAlice,Düsseldorf – West\n".encode("cp1252"))

    table = CsvAdapter(input_path, encoding="cp1252").read()

    assert table.rows[0]["city"] == "Düsseldorf – West"
    assert table.metadata["encoding"] == "cp1252"
    assert table.metadata["parse_diagnostics"]["detection"]["encoding"][
        "confidence"
    ] == "override"


def test_csv_adapter_uses_defaults_when_auto_detect_is_disabled(tmp_path: Path) -> None:
    input_path = tmp_path / "comma.csv"
    input_path.write_text("name,city\nAlice,Berlin\n", encoding="utf-8")

    table = CsvAdapter(input_path, auto_detect=False).read()

    detection = table.metadata["parse_diagnostics"]["detection"]

    assert table.metadata["encoding"] == "utf-8"
    assert table.metadata["delimiter"] == ","
    assert detection["encoding"]["confidence"] == "default"
    assert detection["delimiter"]["confidence"] == "default"
