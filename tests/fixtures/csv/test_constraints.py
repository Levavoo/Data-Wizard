from data_processor.core.column import Column
from data_processor.core.schema import Schema
from data_processor.core.table import Table
from data_processor.validators.constraints import (
    Constraint,
    ValidationResult,
    validate_allowed_values,
    validate_column_constraint,
    validate_max_value,
    validate_min_value,
    validate_regex_pattern,
    validate_required,
    validate_table_constraints,
    validate_unique,
)


def create_test_table() -> Table:
    """
    Create reusable constraint test table.
    """
    schema = Schema(
        columns=[
            Column(name="customer_id"),
            Column(name="name"),
            Column(name="age"),
            Column(name="country"),
            Column(name="email"),
        ]
    )

    return Table(
        name="customers",
        schema=schema,
        rows=[
            {
                "customer_id": 1,
                "name": "Alice",
                "age": 25,
                "country": "Germany",
                "email": "alice@example.com",
            },
            {
                "customer_id": 2,
                "name": None,
                "age": 15,
                "country": "France",
                "email": "invalid-email",
            },
            {
                "customer_id": 1,
                "name": "Charlie",
                "age": 130,
                "country": "Mars",
                "email": "charlie@example.com",
            },
        ],
    )


def test_validation_result_to_dict() -> None:
    """
    Verify ValidationResult serialization.
    """
    result = ValidationResult(
        column_name="age",
        constraint_type="min_value",
        passed=False,
        message="Too small",
        row_index=1,
        value=15,
    )

    result_dict = result.to_dict()

    assert result_dict["column_name"] == "age"

    assert result_dict["constraint_type"] == "min_value"

    assert result_dict["passed"] is False

    assert result_dict["row_index"] == 1


def test_validate_required() -> None:
    """
    Verify required constraint validation.
    """
    table = create_test_table()

    constraint = Constraint(
        column_name="name",
        constraint_type="required",
    )

    results = validate_required(
        table=table,
        constraint=constraint,
    )

    failed_results = [result for result in results if not result.passed]

    assert len(failed_results) == 1

    assert failed_results[0].row_index == 1


def test_validate_unique() -> None:
    """
    Verify unique constraint validation.
    """
    table = create_test_table()

    constraint = Constraint(
        column_name="customer_id",
        constraint_type="unique",
    )

    results = validate_unique(
        table=table,
        constraint=constraint,
    )

    failed_results = [result for result in results if not result.passed]

    assert len(failed_results) == 1

    assert failed_results[0].value == 1


def test_validate_min_value() -> None:
    """
    Verify minimum value validation.
    """
    table = create_test_table()

    constraint = Constraint(
        column_name="age",
        constraint_type="min_value",
        value=18,
    )

    results = validate_min_value(
        table=table,
        constraint=constraint,
    )

    failed_results = [result for result in results if not result.passed]

    assert len(failed_results) == 1

    assert failed_results[0].value == 15


def test_validate_max_value() -> None:
    """
    Verify maximum value validation.
    """
    table = create_test_table()

    constraint = Constraint(
        column_name="age",
        constraint_type="max_value",
        value=120,
    )

    results = validate_max_value(
        table=table,
        constraint=constraint,
    )

    failed_results = [result for result in results if not result.passed]

    assert len(failed_results) == 1

    assert failed_results[0].value == 130


def test_validate_allowed_values() -> None:
    """
    Verify allowed values validation.
    """
    table = create_test_table()

    constraint = Constraint(
        column_name="country",
        constraint_type="allowed_values",
        value=[
            "Germany",
            "France",
        ],
    )

    results = validate_allowed_values(
        table=table,
        constraint=constraint,
    )

    failed_results = [result for result in results if not result.passed]

    assert len(failed_results) == 1

    assert failed_results[0].value == "Mars"


def test_validate_regex_pattern() -> None:
    """
    Verify regex validation.
    """
    table = create_test_table()

    constraint = Constraint(
        column_name="email",
        constraint_type="regex_pattern",
        value=r"^[^@]+@[^@]+\.[^@]+$",
    )

    results = validate_regex_pattern(
        table=table,
        constraint=constraint,
    )

    failed_results = [result for result in results if not result.passed]

    assert len(failed_results) == 1

    assert failed_results[0].value == "invalid-email"


def test_validate_column_constraint_dispatch() -> None:
    """
    Verify constraint dispatching.
    """
    table = create_test_table()

    constraint = Constraint(
        column_name="name",
        constraint_type="required",
    )

    results = validate_column_constraint(
        table=table,
        constraint=constraint,
    )

    assert isinstance(results, list)

    assert len(results) >= 1


def test_validate_unknown_constraint() -> None:
    """
    Verify unsupported constraints fail.
    """
    table = create_test_table()

    constraint = Constraint(
        column_name="name",
        constraint_type="unknown_constraint",
    )

    results = validate_column_constraint(
        table=table,
        constraint=constraint,
    )

    assert len(results) == 1

    assert results[0].passed is False


def test_validate_table_constraints() -> None:
    """
    Verify multiple constraints are applied.
    """
    table = create_test_table()

    constraints = [
        Constraint(
            column_name="name",
            constraint_type="required",
        ),
        Constraint(
            column_name="customer_id",
            constraint_type="unique",
        ),
    ]

    results = validate_table_constraints(
        table=table,
        constraints=constraints,
    )

    failed_results = [result for result in results if not result.passed]

    assert len(failed_results) == 2
