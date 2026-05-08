"""
Constraint validation utilities.

This module validates table values against reusable constraint definitions.

Purpose:
- validate required values
- validate uniqueness
- validate min/max values
- validate allowed values
- validate regex patterns
- return structured validation results
"""

import re
from dataclasses import dataclass
from typing import Any

from data_processor.core.table import Table


@dataclass
class Constraint:
    """
    Defines a validation rule for one column.

    Attributes:
        column_name:
            Column to validate.

        constraint_type:
            Type of validation rule.

        value:
            Optional constraint value.
    """

    column_name: str
    constraint_type: str
    value: Any = None


@dataclass
class ValidationResult:
    """
    Represents one validation result.

    Attributes:
        column_name:
            Column that was validated.

        constraint_type:
            Constraint that was checked.

        passed:
            Whether validation passed.

        message:
            Human-readable validation message.

        row_index:
            Optional row index for row-level failures.

        value:
            Optional offending value.
    """

    column_name: str
    constraint_type: str
    passed: bool
    message: str
    row_index: int | None = None
    value: Any = None

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the validation result to a dictionary.

        Returns:
            Dictionary representation.
        """
        return {
            "column_name": self.column_name,
            "constraint_type": self.constraint_type,
            "passed": self.passed,
            "message": self.message,
            "row_index": self.row_index,
            "value": self.value,
        }


def validate_table_constraints(
    table: Table,
    constraints: list[Constraint],
) -> list[ValidationResult]:
    """
    Validate a table against multiple constraints.

    Args:
        table:
            Internal dataset table.

        constraints:
            List of constraints to apply.

    Returns:
        List of validation results.
    """
    results: list[ValidationResult] = []

    for constraint in constraints:
        results.extend(
            validate_column_constraint(
                table=table,
                constraint=constraint,
            )
        )

    return results


def validate_column_constraint(
    table: Table,
    constraint: Constraint,
) -> list[ValidationResult]:
    """
    Validate one column constraint.

    Args:
        table:
            Internal dataset table.

        constraint:
            Constraint to validate.

    Returns:
        List of validation results.
    """
    constraint_type = constraint.constraint_type.strip().lower()

    if constraint_type == "required":
        return validate_required(table, constraint)

    if constraint_type == "unique":
        return validate_unique(table, constraint)

    if constraint_type == "min_value":
        return validate_min_value(table, constraint)

    if constraint_type == "max_value":
        return validate_max_value(table, constraint)

    if constraint_type == "allowed_values":
        return validate_allowed_values(table, constraint)

    if constraint_type == "regex_pattern":
        return validate_regex_pattern(table, constraint)

    return [
        ValidationResult(
            column_name=constraint.column_name,
            constraint_type=constraint.constraint_type,
            passed=False,
            message=f"Unsupported constraint type: {constraint.constraint_type}",
        )
    ]


def validate_required(
    table: Table,
    constraint: Constraint,
) -> list[ValidationResult]:
    """
    Validate that a column has no missing values.

    Args:
        table:
            Internal dataset table.

        constraint:
            Required constraint.

    Returns:
        List of validation results.
    """
    results: list[ValidationResult] = []

    for row_index, row in enumerate(table.rows):
        value = row.get(constraint.column_name)

        if value is None:
            results.append(
                ValidationResult(
                    column_name=constraint.column_name,
                    constraint_type="required",
                    passed=False,
                    message="Required value is missing.",
                    row_index=row_index,
                    value=value,
                )
            )

    if not results:
        return [
            ValidationResult(
                column_name=constraint.column_name,
                constraint_type="required",
                passed=True,
                message="Required constraint passed.",
            )
        ]

    return results


def validate_unique(
    table: Table,
    constraint: Constraint,
) -> list[ValidationResult]:
    """
    Validate that non-null column values are unique.

    Args:
        table:
            Internal dataset table.

        constraint:
            Unique constraint.

    Returns:
        List of validation results.
    """
    seen_values: dict[Any, int] = {}
    results: list[ValidationResult] = []

    for row_index, row in enumerate(table.rows):
        value = row.get(constraint.column_name)

        if value is None:
            continue

        if value in seen_values:
            results.append(
                ValidationResult(
                    column_name=constraint.column_name,
                    constraint_type="unique",
                    passed=False,
                    message="Duplicate value found.",
                    row_index=row_index,
                    value=value,
                )
            )

        else:
            seen_values[value] = row_index

    if not results:
        return [
            ValidationResult(
                column_name=constraint.column_name,
                constraint_type="unique",
                passed=True,
                message="Unique constraint passed.",
            )
        ]

    return results


def validate_min_value(
    table: Table,
    constraint: Constraint,
) -> list[ValidationResult]:
    """
    Validate that values are greater than or equal to a minimum.

    Args:
        table:
            Internal dataset table.

        constraint:
            Min value constraint.

    Returns:
        List of validation results.
    """
    results: list[ValidationResult] = []

    for row_index, row in enumerate(table.rows):
        value = row.get(constraint.column_name)

        if value is None:
            continue

        try:
            if value < constraint.value:
                results.append(
                    ValidationResult(
                        column_name=constraint.column_name,
                        constraint_type="min_value",
                        passed=False,
                        message=f"Value is below minimum: {constraint.value}",
                        row_index=row_index,
                        value=value,
                    )
                )

        except TypeError:
            results.append(
                ValidationResult(
                    column_name=constraint.column_name,
                    constraint_type="min_value",
                    passed=False,
                    message="Value cannot be compared with minimum.",
                    row_index=row_index,
                    value=value,
                )
            )

    if not results:
        return [
            ValidationResult(
                column_name=constraint.column_name,
                constraint_type="min_value",
                passed=True,
                message="Minimum value constraint passed.",
            )
        ]

    return results


def validate_max_value(
    table: Table,
    constraint: Constraint,
) -> list[ValidationResult]:
    """
    Validate that values are less than or equal to a maximum.

    Args:
        table:
            Internal dataset table.

        constraint:
            Max value constraint.

    Returns:
        List of validation results.
    """
    results: list[ValidationResult] = []

    for row_index, row in enumerate(table.rows):
        value = row.get(constraint.column_name)

        if value is None:
            continue

        try:
            if value > constraint.value:
                results.append(
                    ValidationResult(
                        column_name=constraint.column_name,
                        constraint_type="max_value",
                        passed=False,
                        message=f"Value is above maximum: {constraint.value}",
                        row_index=row_index,
                        value=value,
                    )
                )

        except TypeError:
            results.append(
                ValidationResult(
                    column_name=constraint.column_name,
                    constraint_type="max_value",
                    passed=False,
                    message="Value cannot be compared with maximum.",
                    row_index=row_index,
                    value=value,
                )
            )

    if not results:
        return [
            ValidationResult(
                column_name=constraint.column_name,
                constraint_type="max_value",
                passed=True,
                message="Maximum value constraint passed.",
            )
        ]

    return results


def validate_allowed_values(
    table: Table,
    constraint: Constraint,
) -> list[ValidationResult]:
    """
    Validate that values belong to an allowed set.

    Args:
        table:
            Internal dataset table.

        constraint:
            Allowed values constraint.

    Returns:
        List of validation results.
    """
    allowed_values = set(constraint.value)
    results: list[ValidationResult] = []

    for row_index, row in enumerate(table.rows):
        value = row.get(constraint.column_name)

        if value is None:
            continue

        if value not in allowed_values:
            results.append(
                ValidationResult(
                    column_name=constraint.column_name,
                    constraint_type="allowed_values",
                    passed=False,
                    message="Value is not in allowed values.",
                    row_index=row_index,
                    value=value,
                )
            )

    if not results:
        return [
            ValidationResult(
                column_name=constraint.column_name,
                constraint_type="allowed_values",
                passed=True,
                message="Allowed values constraint passed.",
            )
        ]

    return results


def validate_regex_pattern(
    table: Table,
    constraint: Constraint,
) -> list[ValidationResult]:
    """
    Validate that string values match a regex pattern.

    Args:
        table:
            Internal dataset table.

        constraint:
            Regex pattern constraint.

    Returns:
        List of validation results.
    """
    pattern = re.compile(str(constraint.value))
    results: list[ValidationResult] = []

    for row_index, row in enumerate(table.rows):
        value = row.get(constraint.column_name)

        if value is None:
            continue

        if not isinstance(value, str):
            results.append(
                ValidationResult(
                    column_name=constraint.column_name,
                    constraint_type="regex_pattern",
                    passed=False,
                    message="Value is not a string.",
                    row_index=row_index,
                    value=value,
                )
            )
            continue

        if pattern.fullmatch(value) is None:
            results.append(
                ValidationResult(
                    column_name=constraint.column_name,
                    constraint_type="regex_pattern",
                    passed=False,
                    message="Value does not match regex pattern.",
                    row_index=row_index,
                    value=value,
                )
            )

    if not results:
        return [
            ValidationResult(
                column_name=constraint.column_name,
                constraint_type="regex_pattern",
                passed=True,
                message="Regex pattern constraint passed.",
            )
        ]

    return results
