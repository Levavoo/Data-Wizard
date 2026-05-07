"""
Text cleaning utilities.

This module provides generic text normalization functions.

Purpose:
- trim surrounding whitespace
- collapse repeated internal whitespace
- optionally normalize casing
- preserve non-text values
"""

import re
from typing import Any

from data_processor.core.table import Table

VALID_CASE_OPTIONS = {
    None,
    "lower",
    "upper",
    "title",
}


def normalize_text(value: Any, case: str | None = None) -> Any:
    """
    Normalize one text value.

    Args:
        value:
            Raw input value.

        case:
            Optional casing mode.
            Supported values: None, "lower", "upper", "title".

    Returns:
        Normalized text value if input is a string,
        otherwise the original value.

    Raises:
        ValueError:
            If an unsupported casing option is provided.
    """
    if case not in VALID_CASE_OPTIONS:
        raise ValueError(
            f"Unsupported case option '{case}'. "
            f"Supported options: {VALID_CASE_OPTIONS}"
        )

    if value is None:
        return None

    if not isinstance(value, str):
        return value

    normalized_value = value.strip()
    normalized_value = re.sub(r"\s+", " ", normalized_value)

    if case == "lower":
        return normalized_value.lower()

    if case == "upper":
        return normalized_value.upper()

    if case == "title":
        return normalized_value.title()

    return normalized_value


def clean_table_text(table: Table, case: str | None = None) -> None:
    """
    Normalize all text values in a table.

    This function mutates table rows in place.

    Args:
        table:
            Internal dataset table.

        case:
            Optional casing mode.
            Supported values: None, "lower", "upper", "title".
    """
    for row in table.rows:
        for column_name, value in row.items():
            row[column_name] = normalize_text(value=value, case=case)
