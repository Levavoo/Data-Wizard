"""
Number cleaning utilities.

This module normalizes numeric string values into Python int or float values.

Purpose:
- standardize numeric values
- support controlled numeric casting
- preserve invalid or unrelated values unchanged
"""

from typing import Any

from data_processor.core.table import Table

SUPPORTED_NUMBER_FORMATS = {
    "auto",
    "us",
    "eu",
}


def normalize_integer(value: Any, number_format: str = "auto") -> Any:
    """
    Normalize one integer-like value.

    Args:
        value:
            Raw input value.

        number_format:
            Number format policy. Supported values: "auto", "us", "eu".

    Returns:
        Integer value if conversion succeeds,
        otherwise the original value.
    """
    if value is None:
        return None

    if isinstance(value, bool):
        return value

    if isinstance(value, int):
        return value

    if not isinstance(value, str):
        return value

    cleaned_value = _clean_numeric_string(
        value=value,
        number_format=number_format,
    )

    if not cleaned_value:
        return value

    try:
        return int(cleaned_value)

    except ValueError:
        return value


def normalize_float(value: Any, number_format: str = "auto") -> Any:
    """
    Normalize one float-like value.

    Args:
        value:
            Raw input value.

        number_format:
            Number format policy. Supported values: "auto", "us", "eu".

    Returns:
        Float value if conversion succeeds,
        otherwise the original value.
    """
    if value is None:
        return None

    if isinstance(value, bool):
        return value

    if isinstance(value, float):
        return value

    if isinstance(value, int):
        return float(value)

    if not isinstance(value, str):
        return value

    cleaned_value = _clean_numeric_string(
        value=value,
        number_format=number_format,
    )

    if not cleaned_value:
        return value

    try:
        return float(cleaned_value)

    except ValueError:
        return value


def normalize_number(value: Any, number_format: str = "auto") -> Any:
    """
    Normalize one numeric-like value.

    Integers are preferred when possible.
    Floats are used when integer conversion fails.

    Args:
        value:
            Raw input value.

        number_format:
            Number format policy. Supported values: "auto", "us", "eu".

    Returns:
        int, float, or the original value.
    """
    integer_value = normalize_integer(
        value=value,
        number_format=number_format,
    )

    if integer_value != value or isinstance(value, int):
        return integer_value

    return normalize_float(
        value=value,
        number_format=number_format,
    )


def clean_table_numbers(table: Table, number_format: str = "auto") -> None:
    """
    Normalize numeric-like values across an entire table.

    This function mutates table rows in place.

    Args:
        table:
            Internal dataset table.

        number_format:
            Number format policy. Supported values: "auto", "us", "eu".
    """
    for row in table.rows:
        for column_name, value in row.items():
            row[column_name] = normalize_number(
                value=value,
                number_format=number_format,
            )


def _clean_numeric_string(value: str, number_format: str = "auto") -> str:
    """
    Prepare a numeric string for parsing.

    Args:
        value:
            Raw string value.

        number_format:
            Number format policy. Supported values: "auto", "us", "eu".

    Returns:
        Cleaned numeric string.

    Raises:
        ValueError:
            If number_format is unsupported.
    """
    if number_format not in SUPPORTED_NUMBER_FORMATS:
        raise ValueError(
            f"Unsupported number format '{number_format}'. "
            f"Supported formats: {SUPPORTED_NUMBER_FORMATS}"
        )

    stripped_value = value.strip().replace("_", "")

    if number_format == "us":
        return _clean_us_numeric_string(stripped_value)

    if number_format == "eu":
        return _clean_eu_numeric_string(stripped_value)

    detected_format = _detect_number_format(stripped_value)

    if detected_format == "eu":
        return _clean_eu_numeric_string(stripped_value)

    return _clean_us_numeric_string(stripped_value)


def _detect_number_format(value: str) -> str:
    """
    Detect likely number format for one numeric string.

    Args:
        value:
            Stripped numeric string.

    Returns:
        "us" or "eu".
    """
    comma_position = value.rfind(",")
    dot_position = value.rfind(".")

    if comma_position == -1:
        return "us"

    if dot_position == -1:
        decimal_part = value[comma_position + 1 :]

        if 0 < len(decimal_part) <= 2 and decimal_part.isdigit():
            return "eu"

        return "us"

    if comma_position > dot_position:
        return "eu"

    return "us"


def _clean_us_numeric_string(value: str) -> str:
    """
    Clean a US-style numeric string.

    Example:
        1,000.50 -> 1000.50
    """
    return value.replace(",", "")


def _clean_eu_numeric_string(value: str) -> str:
    """
    Clean a European-style numeric string.

    Example:
        1.000,50 -> 1000.50
    """
    return value.replace(".", "").replace(",", ".")
