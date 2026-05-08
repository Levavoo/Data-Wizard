from data_processor.core.column import Column
from data_processor.core.schema import Schema
from data_processor.core.table import Table
from data_processor.reports.diagnostic_bundle import build_diagnostic_bundle
from data_processor.validators.constraints import ValidationResult


def create_test_table() -> Table:
    """
    Create reusable diagnostic bundle test table.
    """
    schema = Schema(
        columns=[
            Column(name="customer_id", inferred_type="integer"),
            Column(name="name", inferred_type="string"),
            Column(name="country", inferred_type="string"),
        ]
    )

    return Table(
        name="customers",
        schema=schema,
        rows=[
            {
                "customer_id": 1,
                "name": "Alice",
                "country": "Germany",
            },
            {
                "customer_id": 2,
                "name": None,
                "country": "France",
            },
            {
                "customer_id": 1,
                "name": "Alice",
                "country": "Germany",
            },
        ],
    )


def test_build_diagnostic_bundle_contains_top_level_fields() -> None:
    """
    Verify top-level diagnostic bundle fields.
    """
    table = create_test_table()

    bundle = build_diagnostic_bundle(table)

    assert bundle["table_name"] == "customers"
    assert bundle["row_count"] == 3
    assert bundle["column_count"] == 3

    assert "quality_report" in bundle
    assert "column_profiles" in bundle
    assert "row_profiles" in bundle
    assert "validation_report" in bundle


def test_build_diagnostic_bundle_quality_report() -> None:
    """
    Verify quality report is included.
    """
    table = create_test_table()

    bundle = build_diagnostic_bundle(table)

    quality_report = bundle["quality_report"]

    assert quality_report["table_name"] == "customers"
    assert quality_report["row_count"] == 3
    assert quality_report["duplicate_row_count"] == 1


def test_build_diagnostic_bundle_column_profiles() -> None:
    """
    Verify column profiles are included.
    """
    table = create_test_table()

    bundle = build_diagnostic_bundle(table)

    column_profiles = bundle["column_profiles"]

    assert "customer_id" in column_profiles
    assert "name" in column_profiles
    assert "country" in column_profiles

    assert column_profiles["name"]["missing_count"] == 1


def test_build_diagnostic_bundle_row_profiles() -> None:
    """
    Verify row profiles are included.
    """
    table = create_test_table()

    bundle = build_diagnostic_bundle(table)

    row_profiles = bundle["row_profiles"]

    assert len(row_profiles) == 3
    assert row_profiles[1]["missing_count"] == 1
    assert row_profiles[0]["duplicate_candidate"] is True


def test_build_diagnostic_bundle_validation_report() -> None:
    """
    Verify validation report is included when validation results are provided.
    """
    table = create_test_table()

    validation_results = [
        ValidationResult(
            column_name="name",
            constraint_type="required",
            passed=False,
            message="Required value is missing.",
            row_index=1,
            value=None,
        )
    ]

    bundle = build_diagnostic_bundle(
        table=table,
        validation_results=validation_results,
    )

    validation_report = bundle["validation_report"]

    assert validation_report["failed_count"] == 1
    assert validation_report["has_failures"] is True
    assert validation_report["failures_by_column"]["name"] == 1


def test_build_diagnostic_bundle_empty_validation_report() -> None:
    """
    Verify validation report exists even without validation results.
    """
    table = create_test_table()

    bundle = build_diagnostic_bundle(table)

    validation_report = bundle["validation_report"]

    assert validation_report["total_results"] == 0
    assert validation_report["failed_count"] == 0
    assert validation_report["has_failures"] is False


def test_build_diagnostic_bundle_includes_table_metadata() -> None:
    """
    Verify table metadata is included in the diagnostic bundle.
    """
    table = create_test_table()

    table.add_metadata("source_format", "csv")
    table.add_metadata("encoding", "utf-8")
    table.add_metadata("delimiter", ";")

    bundle = build_diagnostic_bundle(table)

    assert bundle["metadata"]["source_format"] == "csv"
    assert bundle["metadata"]["encoding"] == "utf-8"
    assert bundle["metadata"]["delimiter"] == ";"
