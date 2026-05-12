"""
Constraint configuration loader.

This module converts machine-readable constraint configuration dictionaries into
Constraint objects used by the validation engine.
"""

from typing import Any

from data_processor.validators.constraints import Constraint

CONSTRAINT_VALUE_KEYS = {
    "min_value": "value",
    "max_value": "value",
    "allowed_values": "values",
    "regex_pattern": "pattern",
    "regex": "pattern",
}

CONSTRAINT_TYPE_ALIASES = {
    "regex": "regex_pattern",
}

SUPPORTED_CONSTRAINT_TYPES = {
    "required",
    "unique",
    "min_value",
    "max_value",
    "allowed_values",
    "regex_pattern",
    "regex",
}


def load_constraints_from_config(config: list[dict[str, Any]]) -> list[Constraint]:
    """
    Convert constraint config dictionaries into Constraint objects.

    Args:
        config:
            List of constraint dictionaries.

    Returns:
        List of Constraint objects.

    Raises:
        ValueError:
            If the config is invalid.
    """
    if not isinstance(config, list):
        raise ValueError("Constraint config must be a list of dictionaries.")

    return [_load_constraint(item) for item in config]


def _load_constraint(item: dict[str, Any]) -> Constraint:
    """
    Convert one constraint config dictionary into a Constraint object.
    """
    if not isinstance(item, dict):
        raise ValueError("Each constraint config entry must be a dictionary.")

    column_name = item.get("column") or item.get("column_name")
    constraint_type = item.get("type") or item.get("constraint_type")

    if not column_name:
        raise ValueError("Constraint config entry is missing required field: column")

    if not constraint_type:
        raise ValueError("Constraint config entry is missing required field: type")

    normalized_type = str(constraint_type).strip().lower()

    if normalized_type not in SUPPORTED_CONSTRAINT_TYPES:
        raise ValueError(f"Unsupported constraint type: {constraint_type}")

    normalized_type = CONSTRAINT_TYPE_ALIASES.get(normalized_type, normalized_type)

    value = _extract_constraint_value(
        item=item,
        constraint_type=normalized_type,
    )

    return Constraint(
        column_name=str(column_name),
        constraint_type=normalized_type,
        value=value,
    )


def _extract_constraint_value(
    item: dict[str, Any],
    constraint_type: str,
) -> Any:
    """
    Extract the value field needed for one constraint type.
    """
    value_key = CONSTRAINT_VALUE_KEYS.get(constraint_type)

    if value_key is None:
        return None

    if value_key not in item:
        raise ValueError(
            f"Constraint type '{constraint_type}' requires field: {value_key}"
        )

    return item[value_key]
