from pathlib import Path

import pytest

from data_processor.adapters.json_adapter import JsonAdapter


def test_json_adapter_reads_simple_customers_fixture() -> None:
    adapter = JsonAdapter("tests/fixtures/json/simple_customers.json")

    table = adapter.read()

    assert table.name == "simple_customers"
    assert table.schema.column_names() == [
        "customer_id",
        "name",
        "email",
        "amount",
        "active",
    ]
    assert table.row_count() == 2
    assert table.rows[0]["name"] == "Alice"
    assert table.rows[0]["active"] is True
    assert table.metadata["source_format"] == "json"
    assert table.metadata["parse_diagnostics"]["record_count"] == 2


def test_json_adapter_unions_keys_and_fills_missing_values() -> None:
    adapter = JsonAdapter("tests/fixtures/json/missing_keys_customers.json")

    table = adapter.read()

    assert table.schema.column_names() == [
        "customer_id",
        "name",
        "email",
        "amount",
        "active",
    ]
    assert table.rows[1]["email"] is None
    assert table.rows[1]["amount"] is None
    assert table.rows[2]["name"] is None
    assert table.metadata["parse_diagnostics"]["missing_key_counts"]["email"] == 1
    assert table.metadata["parse_diagnostics"]["missing_key_counts"]["name"] == 1


def test_json_adapter_stringifies_nested_values_and_reports_columns() -> None:
    adapter = JsonAdapter("tests/fixtures/json/nested_values_customers.json")

    table = adapter.read()
    diagnostics = table.metadata["parse_diagnostics"]

    assert table.rows[0]["address"] == '{"city":"Berlin","postal_code":"10115"}'
    assert table.rows[0]["tags"] == '["vip","newsletter"]'
    assert diagnostics["nested_value_columns"] == ["address"]
    assert diagnostics["array_value_columns"] == ["tags"]
    assert "Nested object values were converted to JSON strings." in diagnostics["warnings"]
    assert "Array values were converted to JSON strings." in diagnostics["warnings"]


def test_json_adapter_rejects_root_object() -> None:
    adapter = JsonAdapter("tests/fixtures/json/invalid_root_object.json")

    with pytest.raises(ValueError, match="JSON root must be a list of objects"):
        adapter.read()


def test_json_adapter_rejects_mixed_list_values() -> None:
    adapter = JsonAdapter("tests/fixtures/json/mixed_list_values.json")

    with pytest.raises(ValueError, match="Invalid record indexes"):
        adapter.read()


def test_json_adapter_rejects_wrong_extension(tmp_path: Path) -> None:
    path = tmp_path / "data.txt"
    path.write_text("[]", encoding="utf-8")

    adapter = JsonAdapter(path)

    with pytest.raises(ValueError, match="Unsupported file extension"):
        adapter.read()
