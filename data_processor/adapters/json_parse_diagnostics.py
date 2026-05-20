"""
JSON parse diagnostics.

This module stores structural diagnostics collected by the JSON adapter.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class JsonParseDiagnostics:
    """
    Diagnostics for JSON source parsing.
    """

    root_type: str
    record_count: int = 0
    column_count: int = 0
    missing_key_counts: dict[str, int] = field(default_factory=dict)
    nested_value_columns: list[str] = field(default_factory=list)
    array_value_columns: list[str] = field(default_factory=list)
    invalid_record_indexes: list[int] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_warning(self, warning: str) -> None:
        """
        Add one warning message.
        """
        self.warnings.append(warning)

    def add_nested_value_column(self, column_name: str) -> None:
        """
        Record a column that contains nested object values.
        """
        if column_name not in self.nested_value_columns:
            self.nested_value_columns.append(column_name)

    def add_array_value_column(self, column_name: str) -> None:
        """
        Record a column that contains array values.
        """
        if column_name not in self.array_value_columns:
            self.array_value_columns.append(column_name)

    def add_invalid_record_index(self, index: int) -> None:
        """
        Record a list item index that is not an object.
        """
        self.invalid_record_indexes.append(index)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert diagnostics into a serializable dictionary.
        """
        return {
            "root_type": self.root_type,
            "record_count": self.record_count,
            "column_count": self.column_count,
            "missing_key_counts": self.missing_key_counts,
            "nested_value_columns": self.nested_value_columns,
            "array_value_columns": self.array_value_columns,
            "invalid_record_indexes": self.invalid_record_indexes,
            "warnings": self.warnings,
        }
