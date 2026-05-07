"""
Core schema model.

Defines the Schema class used by the canonical internal table model.
A schema describes the structure of a dataset through its columns.
"""

from dataclasses import dataclass, field
from typing import Any

from data_processor.core.column import Column


@dataclass
class Schema:
    """
    Represents the schema of a dataset.

    Attributes:
        columns:
            Ordered list of dataset columns.

        metadata:
            Additional schema-related information.
    """

    columns: list[Column] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_column(self, column: Column) -> None:
        """
        Add a column to the schema.

        Args:
            column:
                Column object to add.
        """
        self.columns.append(column)

    def get_column(self, name: str) -> Column | None:
        """
        Find a column by internal name.

        Args:
            name:
                Internal column name.

        Returns:
            Matching Column object or None.
        """
        normalized_name = name.strip().lower()

        for column in self.columns:
            if column.name.lower() == normalized_name:
                return column

        return None

    def has_column(self, name: str) -> bool:
        """
        Check whether a column exists.

        Args:
            name:
                Internal column name.

        Returns:
            True if found, otherwise False.
        """
        return self.get_column(name) is not None

    def remove_column(self, name: str) -> bool:
        """
        Remove a column from the schema.

        Args:
            name:
                Internal column name.

        Returns:
            True if removed successfully, otherwise False.
        """
        column = self.get_column(name)

        if column is None:
            return False

        self.columns.remove(column)
        return True

    def column_names(self) -> list[str]:
        """
        Return all internal column names.

        Returns:
            List of column names.
        """
        return [column.name for column in self.columns]

    def add_metadata(self, key: str, value: Any) -> None:
        """
        Add or update schema metadata.

        Args:
            key:
                Metadata key.

            value:
                Metadata value.
        """
        self.metadata[key] = value

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the schema into a serializable dictionary.

        Returns:
            Dictionary representation of the schema.
        """
        return {
            "columns": [column.to_dict() for column in self.columns],
            "metadata": self.metadata,
        }
