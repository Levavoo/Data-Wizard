from data_processor.adapters.json_parse_diagnostics import JsonParseDiagnostics


def test_json_parse_diagnostics_serializes_defaults() -> None:
    diagnostics = JsonParseDiagnostics(root_type="list")

    assert diagnostics.to_dict() == {
        "root_type": "list",
        "record_count": 0,
        "column_count": 0,
        "missing_key_counts": {},
        "nested_value_columns": [],
        "array_value_columns": [],
        "invalid_record_indexes": [],
        "warnings": [],
    }


def test_json_parse_diagnostics_records_warnings_and_columns() -> None:
    diagnostics = JsonParseDiagnostics(root_type="list")

    diagnostics.add_warning("Nested values were converted to JSON strings.")
    diagnostics.add_nested_value_column("address")
    diagnostics.add_nested_value_column("address")
    diagnostics.add_array_value_column("tags")
    diagnostics.add_array_value_column("tags")
    diagnostics.add_invalid_record_index(2)

    result = diagnostics.to_dict()

    assert result["warnings"] == ["Nested values were converted to JSON strings."]
    assert result["nested_value_columns"] == ["address"]
    assert result["array_value_columns"] == ["tags"]
    assert result["invalid_record_indexes"] == [2]
