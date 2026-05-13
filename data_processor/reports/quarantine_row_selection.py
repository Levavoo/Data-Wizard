"""
Quarantine row selection utilities.

This module selects quarantine and accepted rows from a table using existing
quarantine candidate row indexes. It does not mutate the original table.
"""

from typing import Any

from data_processor.core.table import Table


def get_quarantine_row_indexes(
    quarantine_candidates: dict[str, Any],
) -> set[int]:
    """
    Extract quarantine candidate row indexes.

    Args:
        quarantine_candidates:
            Quarantine candidate report dictionary.

    Returns:
        Set of zero-based row indexes.
    """
    row_indexes = set()

    for candidate in quarantine_candidates.get("candidates", []):
        row_index = candidate.get("row_index")

        if isinstance(row_index, int):
            row_indexes.add(row_index)

    return row_indexes


def select_quarantine_rows(
    table: Table,
    quarantine_candidates: dict[str, Any],
) -> Table:
    """
    Select rows listed as quarantine candidates.

    Args:
        table:
            Source table.

        quarantine_candidates:
            Quarantine candidate report dictionary.

    Returns:
        New table containing only quarantine candidate rows.
    """
    quarantine_indexes = get_quarantine_row_indexes(quarantine_candidates)
    rows = [
        row.copy()
        for row_index, row in enumerate(table.rows)
        if row_index in quarantine_indexes
    ]

    return _copy_table_with_rows(
        source_table=table,
        rows=rows,
        name_suffix="quarantine_rows",
    )


def select_accepted_rows(
    table: Table,
    quarantine_candidates: dict[str, Any],
) -> Table:
    """
    Select rows not listed as quarantine candidates.

    Args:
        table:
            Source table.

        quarantine_candidates:
            Quarantine candidate report dictionary.

    Returns:
        New table containing only accepted rows.
    """
    quarantine_indexes = get_quarantine_row_indexes(quarantine_candidates)
    rows = [
        row.copy()
        for row_index, row in enumerate(table.rows)
        if row_index not in quarantine_indexes
    ]

    return _copy_table_with_rows(
        source_table=table,
        rows=rows,
        name_suffix="accepted_rows",
    )


def _copy_table_with_rows(
    source_table: Table,
    rows: list[dict[str, Any]],
    name_suffix: str,
) -> Table:
    """
    Create a new table that reuses schema and metadata with copied rows.
    """
    return Table(
        name=f"{source_table.name}_{name_suffix}",
        schema=source_table.schema,
        rows=rows,
        metadata=source_table.metadata.copy(),
    )
