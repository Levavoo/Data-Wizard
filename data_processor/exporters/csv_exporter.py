"""
CSV exporter.

This module writes the internal Table model to a CSV file.

Purpose:
- export cleaned datasets
- preserve schema column order
- write UTF-8 CSV output
- create output directories when needed
"""

import csv
from datetime import date
from datetime import datetime
from pathlib import Path
from typing import Any

from data_processor.core.table import Table


def export_table_to_csv(
    table: Table,
    output_path: str | Path,
    encoding: str = "utf-8",
) -> None:
    """
    Export a Table to a CSV file.

    Args:
        table:
            Internal dataset table.

        output_path:
            Target CSV output path.

        encoding:
            Output file encoding.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    headers = table.schema.column_names()

    with path.open(
        mode="w",
        encoding=encoding,
        newline="",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=headers,
            extrasaction="ignore",
        )

        writer.writeheader()

        for row in table.rows:
            writer.writerow(
                {
                    column_name: serialize_csv_value(row.get(column_name))
                    for column_name in headers
                }
            )


def serialize_csv_value(value: Any) -> str:
    """
    Convert a Python value into a CSV-safe string.

    Args:
        value:
            Python value from a table row.

    Returns:
        String representation safe for CSV output.
    """
    if value is None:
        return ""

    if isinstance(value, bool):
        return "true" if value else "false"

    if isinstance(value, datetime):
        return value.isoformat(sep=" ")

    if isinstance(value, date):
        return value.isoformat()

    return str(value)
