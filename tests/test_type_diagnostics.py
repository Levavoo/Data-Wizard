from data_processor.core.column import Column
from data_processor.core.schema import Schema
from data_processor.core.table import Table
from data_processor.inference.type_diagnostics import analyze_column_type_evidence
from data_processor.inference.type_diagnostics import analyze_table_type_evidence
from data_processor.inference.type_inference import infer_column_type


def test_current_mixed_type_inference_falls_back_to_string() -> None:
    """
    Verify current strict inference falls back to string for mixed columns.
    """
    values = ["100", "250.75", "unknown", "300"]

    assert infer_column_type(values) == "string"


def test_analyze_column_type_evidence_detects_mixed_numeric_column() -> None:
    """
    Verify mostly numeric mixed columns report invalid values.
    """
    values = ["100", "250.75", "unknown", "300", "400"]

    diagnostics = analyze_column_type_evidence(
        values=values,
        column_name="amount",
    )

    assert diagnostics["column"] == "amount"
    assert diagnostics["dominant_type"] == "float"
    assert diagnostics["total_values"] == 5
    assert diagnostics["non_null_count"] == 5
    assert diagnostics["null_count"] == 0
    assert diagnostics["valid_count"] == 4
    assert diagnostics["invalid_count"] == 1
    assert diagnostics["is_mixed_type"] is True
    assert diagnostics["invalid_values"] == [
        {
            "row_index": 2,
            "value": "unknown",
            "expected_type": "float",
        }
    ]


def test_analyze_column_type_evidence_ignores_null_values() -> None:
    """
    Verify null values do not count as invalid mixed-type values.
    """
    values = ["100", None, "250.75", "", "300"]

    diagnostics = analyze_column_type_evidence(
        values=values,
        column_name="amount",
    )

    assert diagnostics["dominant_type"] == "float"
    assert diagnostics["non_null_count"] == 3
    assert diagnostics["null_count"] == 2
    assert diagnostics["valid_count"] == 3
    assert diagnostics["invalid_count"] == 0
    assert diagnostics["is_mixed_type"] is False


def test_analyze_column_type_evidence_respects_threshold() -> None:
    """
    Verify no dominant type is selected when threshold is not met.
    """
    values = ["100", "abc", "def", "ghi"]

    diagnostics = analyze_column_type_evidence(
        values=values,
        column_name="mixed",
    )

    assert diagnostics["dominant_type"] is None
    assert diagnostics["is_mixed_type"] is False
    assert diagnostics["invalid_values"] == []


def test_analyze_column_type_evidence_detects_mixed_boolean_column() -> None:
    """
    Verify mostly boolean mixed columns report invalid values.
    """
    values = ["true", "false", "yes", "maybe", "no"]

    diagnostics = analyze_column_type_evidence(
        values=values,
        column_name="active",
    )

    assert diagnostics["dominant_type"] == "boolean"
    assert diagnostics["valid_count"] == 4
    assert diagnostics["invalid_count"] == 1
    assert diagnostics["invalid_values"] == [
        {
            "row_index": 3,
            "value": "maybe",
            "expected_type": "boolean",
        }
    ]


def test_analyze_table_type_evidence_reports_mixed_type_columns() -> None:
    """
    Verify table-level diagnostics collect mixed-type columns.
    """
    schema = Schema(
        columns=[
            Column(name="amount"),
            Column(name="country"),
        ]
    )

    table = Table(
        name="orders",
        schema=schema,
        rows=[
            {"amount": "100", "country": "Germany"},
            {"amount": "250.75", "country": "France"},
            {"amount": "unknown", "country": "Spain"},
            {"amount": "300", "country": "Italy"},
            {"amount": "400", "country": "Poland"},
        ],
    )

    diagnostics = analyze_table_type_evidence(table)

    assert len(diagnostics["columns"]) == 2
    assert len(diagnostics["mixed_type_columns"]) == 1
    assert diagnostics["mixed_type_columns"][0]["column"] == "amount"
    assert diagnostics["mixed_type_columns"][0]["dominant_type"] == "float"
