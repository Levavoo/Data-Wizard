from data_processor.core.column import Column
from data_processor.core.schema import Schema
from data_processor.core.table import Table
from data_processor.inference.schema_inference import (
    infer_column_metadata,
    infer_schema_metadata,
)


def test_infer_column_metadata_counts() -> None:
    """
    Verify total and missing counts are inferred correctly.
    """
    schema = Schema(
        columns=[
            Column(name="country"),
        ]
    )

    table = Table(
        name="customers",
        schema=schema,
        rows=[
            {"country": "Germany"},
            {"country": "France"},
            {"country": None},
            {"country": "Germany"},
        ],
    )

    metadata = infer_column_metadata(
        table=table,
        column=schema.columns[0],
    )

    assert metadata["total_count"] == 4
    assert metadata["missing_count"] == 1


def test_infer_column_metadata_unique_count() -> None:
    """
    Verify unique non-null values are counted correctly.
    """
    schema = Schema(
        columns=[
            Column(name="country"),
        ]
    )

    table = Table(
        name="customers",
        schema=schema,
        rows=[
            {"country": "Germany"},
            {"country": "France"},
            {"country": "Germany"},
            {"country": None},
        ],
    )

    metadata = infer_column_metadata(
        table=table,
        column=schema.columns[0],
    )

    assert metadata["unique_count"] == 2


def test_infer_column_metadata_nullable() -> None:
    """
    Verify nullable detection.
    """
    schema = Schema(
        columns=[
            Column(name="country"),
        ]
    )

    table = Table(
        name="customers",
        schema=schema,
        rows=[
            {"country": "Germany"},
            {"country": None},
        ],
    )

    metadata = infer_column_metadata(
        table=table,
        column=schema.columns[0],
    )

    assert metadata["nullable"] is True


def test_infer_column_metadata_sample_values() -> None:
    """
    Verify sample values are collected correctly.
    """
    schema = Schema(
        columns=[
            Column(name="country"),
        ]
    )

    table = Table(
        name="customers",
        schema=schema,
        rows=[
            {"country": "Germany"},
            {"country": "France"},
            {"country": "Italy"},
            {"country": "Germany"},
        ],
    )

    metadata = infer_column_metadata(
        table=table,
        column=schema.columns[0],
        sample_size=2,
    )

    assert metadata["sample_values"] == [
        "Germany",
        "France",
    ]


def test_infer_schema_metadata_updates_columns() -> None:
    """
    Verify schema columns are enriched with metadata.
    """
    schema = Schema(
        columns=[
            Column(name="country"),
            Column(name="active"),
        ]
    )

    table = Table(
        name="customers",
        schema=schema,
        rows=[
            {
                "country": "Germany",
                "active": True,
            },
            {
                "country": None,
                "active": False,
            },
        ],
    )

    infer_schema_metadata(table)

    country_column = table.schema.get_column("country")
    active_column = table.schema.get_column("active")

    assert country_column is not None
    assert active_column is not None

    assert country_column.metadata["missing_count"] == 1
    assert country_column.nullable is True

    assert active_column.metadata["missing_count"] == 0
    assert active_column.nullable is False


def test_sample_values_are_unique() -> None:
    """
    Verify duplicate sample values are not repeated.
    """
    schema = Schema(
        columns=[
            Column(name="country"),
        ]
    )

    table = Table(
        name="customers",
        schema=schema,
        rows=[
            {"country": "Germany"},
            {"country": "Germany"},
            {"country": "France"},
        ],
    )

    metadata = infer_column_metadata(
        table=table,
        column=schema.columns[0],
    )

    assert metadata["sample_values"] == [
        "Germany",
        "France",
    ]
