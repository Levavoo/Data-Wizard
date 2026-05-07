"""
Core table model.

Defines the canonical internal dataset representation used throughout
the data cleaning pipeline.

All supported formats (CSV, Excel, JSON, etc.) should be converted into
this structure before cleaning, validation, transformation, or export.
"""

from dataclasses import dataclass, field
from typing import Any

from data_processor.core.schema import Schema


@dataclass
class Table:
    """
    Canonical internal table representation.

    Attributes:
        name:
            Human-readable dataset name.

        schema:
            Dataset schema definition.

        rows:
            List of row dictionaries.

        metadata:
            Additional dataset metadata.
    """

    name: str
    schema: Schema = field(default_factory=Schema)
    rows: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_row(self, row: dict[str, Any]) -> None:
        """
        Add one row to the dataset.

        Args:
            row:
                Dictionary representing one dataset row.
        """
        self.rows.append(row)

    def add_rows(self, rows: list[dict[str, Any]]) -> None:
        """
        Add multiple rows to the dataset.

        Args:
            rows:
                List of row dictionaries.
        """
        self.rows.extend(rows)

    def row_count(self) -> int:
        """
        Return total number of rows.

        Returns:
            Number of dataset rows.
        """
        return len(self.rows)

    def column_count(self) -> int:
        """
        Return total number of columns.

        Returns:
            Number of schema columns.
        """
        return len(self.schema.columns)

    def is_empty(self) -> bool:
        """
        Check whether the dataset contains rows.

        Returns:
            True if empty, otherwise False.
        """
        return self.row_count() == 0

    def add_metadata(self, key: str, value: Any) -> None:
        """
        Add or update dataset metadata.

        Args:
            key:
                Metadata key.

            value:
                Metadata value.
        """
        self.metadata[key] = value

    def head(self, limit: int = 5) -> list[dict[str, Any]]:
        """
        Return the first rows of the dataset.

        Args:
            limit:
                Maximum number of rows to return.

        Returns:
            List of row dictionaries.
        """
        return self.rows[:limit]

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the table into a serializable dictionary.

        Useful for:
        - debugging
        - reports
        - testing
        - JSON export

        Returns:
            Dictionary representation of the table.
        """
        return {
            "name": self.name,
            "schema": self.schema.to_dict(),
            "rows": self.rows,
            "metadata": self.metadata,
        }
