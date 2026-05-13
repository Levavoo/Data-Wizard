"""
Parse diagnostics model.

Parser diagnostics describe structural observations found while reading a source
file. They do not clean, validate, or transform data.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ParseDiagnostics:
    """
    Structured parser diagnostics.
    """

    header_row_index: int = 0
    preamble_row_count: int = 0
    rows_with_extra_fields: list[int] = field(default_factory=list)
    extra_field_count: int = 0
    rows_with_missing_fields: list[int] = field(default_factory=list)
    missing_field_count: int = 0
    duplicate_headers: list[str] = field(default_factory=list)
    empty_headers: list[int] = field(default_factory=list)
    delimiter: str | None = None
    encoding: str | None = None
    detection: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def add_extra_fields(self, row_index: int, count: int) -> None:
        """Record extra values found in a source row."""
        if count <= 0:
            return

        self.rows_with_extra_fields.append(row_index)
        self.extra_field_count += count

    def add_missing_fields(self, row_index: int, count: int) -> None:
        """Record missing values caused by a short source row."""
        if count <= 0:
            return

        self.rows_with_missing_fields.append(row_index)
        self.missing_field_count += count

    def add_warning(self, warning: str) -> None:
        """Record a parser warning."""
        self.warnings.append(warning)

    def to_dict(self) -> dict[str, Any]:
        """Convert diagnostics to a serializable dictionary."""
        return {
            "header_row_index": self.header_row_index,
            "preamble_row_count": self.preamble_row_count,
            "rows_with_extra_fields": self.rows_with_extra_fields,
            "extra_field_count": self.extra_field_count,
            "rows_with_missing_fields": self.rows_with_missing_fields,
            "missing_field_count": self.missing_field_count,
            "duplicate_headers": self.duplicate_headers,
            "empty_headers": self.empty_headers,
            "delimiter": self.delimiter,
            "encoding": self.encoding,
            "detection": self.detection,
            "warnings": self.warnings,
        }
