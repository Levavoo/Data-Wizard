import pytest

from data_processor.validators.constraint_config import load_constraints_from_config


def test_load_required_constraint_from_config() -> None:
    config = [
        {
            "column": "customer_id",
            "type": "required",
        }
    ]

    constraints = load_constraints_from_config(config)

    assert len(constraints) == 1
    assert constraints[0].column_name == "customer_id"
    assert constraints[0].constraint_type == "required"
    assert constraints[0].value is None


def test_load_allowed_values_constraint_from_config() -> None:
    config = [
        {
            "column": "country",
            "type": "allowed_values",
            "values": ["Germany", "France"],
        }
    ]

    constraints = load_constraints_from_config(config)

    assert constraints[0].column_name == "country"
    assert constraints[0].constraint_type == "allowed_values"
    assert constraints[0].value == ["Germany", "France"]


def test_load_regex_alias_constraint_from_config() -> None:
    config = [
        {
            "column": "email",
            "type": "regex",
            "pattern": r"^[^@]+@[^@]+\.[^@]+$",
        }
    ]

    constraints = load_constraints_from_config(config)

    assert constraints[0].column_name == "email"
    assert constraints[0].constraint_type == "regex_pattern"
    assert constraints[0].value == r"^[^@]+@[^@]+\.[^@]+$"


def test_load_min_and_max_value_constraints_from_config() -> None:
    config = [
        {
            "column": "amount",
            "type": "min_value",
            "value": 0,
        },
        {
            "column": "amount",
            "type": "max_value",
            "value": 1000,
        },
    ]

    constraints = load_constraints_from_config(config)

    assert constraints[0].constraint_type == "min_value"
    assert constraints[0].value == 0
    assert constraints[1].constraint_type == "max_value"
    assert constraints[1].value == 1000


def test_load_constraints_requires_list_config() -> None:
    with pytest.raises(ValueError, match="must be a list"):
        load_constraints_from_config({"column": "id", "type": "required"})  # type: ignore[arg-type]


def test_load_constraints_rejects_missing_column() -> None:
    config = [{"type": "required"}]

    with pytest.raises(ValueError, match="column"):
        load_constraints_from_config(config)


def test_load_constraints_rejects_missing_type() -> None:
    config = [{"column": "customer_id"}]

    with pytest.raises(ValueError, match="type"):
        load_constraints_from_config(config)


def test_load_constraints_rejects_unsupported_type() -> None:
    config = [{"column": "customer_id", "type": "foreign_key"}]

    with pytest.raises(ValueError, match="Unsupported constraint type"):
        load_constraints_from_config(config)


def test_load_constraints_requires_value_fields() -> None:
    config = [{"column": "email", "type": "regex"}]

    with pytest.raises(ValueError, match="requires field"):
        load_constraints_from_config(config)
