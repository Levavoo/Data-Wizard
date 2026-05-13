from data_processor.core.column import Column
from data_processor.core.schema import Schema
from data_processor.core.table import Table
from data_processor.reports.quarantine_row_selection import get_quarantine_row_indexes
from data_processor.reports.quarantine_row_selection import select_accepted_rows
from data_processor.reports.quarantine_row_selection import select_quarantine_rows


def create_table() -> Table:
    schema = Schema(
        columns=[
            Column(name="customer_id"),
            Column(name="email"),
        ]
    )

    return Table(
        name="customers",
        schema=schema,
        rows=[
            {"customer_id": 1, "email": "alice@example.com"},
            {"customer_id": 2, "email": "invalid-email"},
            {"customer_id": 3, "email": "bob@example.com"},
        ],
        metadata={"source_format": "csv"},
    )


def test_get_quarantine_row_indexes() -> None:
    quarantine_candidates = {
        "candidates": [
            {"row_index": 1},
            {"row_index": 2},
            {"row_index": "bad"},
            {},
        ]
    }

    assert get_quarantine_row_indexes(quarantine_candidates) == {1, 2}


def test_select_quarantine_rows() -> None:
    table = create_table()
    quarantine_candidates = {"candidates": [{"row_index": 1}]}

    result = select_quarantine_rows(
        table=table,
        quarantine_candidates=quarantine_candidates,
    )

    assert result.name == "customers_quarantine_rows"
    assert result.schema is table.schema
    assert result.metadata == table.metadata
    assert result.rows == [
        {"customer_id": 2, "email": "invalid-email"},
    ]


def test_select_accepted_rows() -> None:
    table = create_table()
    quarantine_candidates = {"candidates": [{"row_index": 1}]}

    result = select_accepted_rows(
        table=table,
        quarantine_candidates=quarantine_candidates,
    )

    assert result.name == "customers_accepted_rows"
    assert result.schema is table.schema
    assert result.rows == [
        {"customer_id": 1, "email": "alice@example.com"},
        {"customer_id": 3, "email": "bob@example.com"},
    ]


def test_empty_candidates_return_all_accepted_rows() -> None:
    table = create_table()
    quarantine_candidates = {"candidates": []}

    quarantine_rows = select_quarantine_rows(table, quarantine_candidates)
    accepted_rows = select_accepted_rows(table, quarantine_candidates)

    assert quarantine_rows.rows == []
    assert accepted_rows.rows == table.rows


def test_row_selection_does_not_mutate_original_table() -> None:
    table = create_table()
    original_rows = [row.copy() for row in table.rows]
    quarantine_candidates = {"candidates": [{"row_index": 1}]}

    select_quarantine_rows(table, quarantine_candidates)
    select_accepted_rows(table, quarantine_candidates)

    assert table.rows == original_rows
