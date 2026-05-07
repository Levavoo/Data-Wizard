"""
Core column model.

This module defines the Column class used by the internal table model.
It does not contain format-specific parsing, cleaning, validation, or export logic.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Column:
    """
    Represents one column in the canonical internal table model.

    Attributes:
        name:
            Standardized internal column name.

        original_name:
            Original column name from the source file.

        inferred_type:
            Detected or assigned logical type.
            Examples: string, integer, float, boolean, date, datetime, null.

        nullable:
            Whether the column may contain null/missing values.

        metadata:
            Extra information about the column.
            This can store parser notes, source position, quality stats, or future flags.
    """

    name: str
    original_name: str | None = None
    inferred_type: str = "unknown"
    nullable: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """
        Normalize the column after creation.
        """
        self.name = self.name.strip()

        if self.original_name is not None:
            self.original_name = self.original_name.strip()

    def display_name(self) -> str:
        """
        Return the best human-readable column name.

        Returns:
            The original column name if available, otherwise the internal name.
        """
        return self.original_name or self.name

    def set_type(self, inferred_type: str) -> None:
        """
        Update the inferred column type.

        Args:
            inferred_type:
                New logical type for the column.
        """
        self.inferred_type = inferred_type.strip().lower()

    def add_metadata(self, key: str, value: Any) -> None:
        """
        Add or update one metadata value.

        Args:
            key:
                Metadata key.

            value:
                Metadata value.
        """
        self.metadata[key] = value

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the column definition to a dictionary.

        Useful for reports, schema export, debugging, and tests.

        Returns:
            Dictionary representation of the column.
        """
        return {
            "name": self.name,
            "original_name": self.original_name,
            "inferred_type": self.inferred_type,
            "nullable": self.nullable,
            "metadata": self.metadata,
        }
