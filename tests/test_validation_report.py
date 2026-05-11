from data_processor.validators.constraints import ValidationResult
from data_processor.validators.validation_report import (
    failed_rows,
    failures_by_column,
    failures_by_constraint,
    generate_validation_report,
)


def create_validation_results() -> list[ValidationResult]:
    """
    Create reusable validation results.
    """
    return [
        ValidationResult(
            column_name="customer_id",
            constraint_type="required",
            passed=True,
            message="Required constraint passed.",
        ),
        ValidationResult(
            column_name="age",
            constraint_type="min_value",
            passed=False,
            message="Value is below minimum: 18",
            row_index=1,
            value=15,
        ),
        ValidationResult(
            column_name="age",
            constraint_type="max_value",
            passed=False,
            message="Value is above maximum: 120",
            row_index=2,
            value=130,
        ),
        ValidationResult(
            column_name="email",
            constraint_type="regex_pattern",
            passed=False,
            message="Value does not match regex pattern.",
            row_index=1,
            value="invalid-email",
        ),
    ]


def test_failures_by_column() -> None:
    """
    Verify failures are grouped by column.
    """
    results = [result for result in create_validation_results() if not result.passed]

    summary = failures_by_column(results)

    assert summary["age"] == 2
    assert summary["email"] == 1


def test_failures_by_constraint() -> None:
    """
    Verify failures are grouped by constraint type.
    """
    results = [result for result in create_validation_results() if not result.passed]

    summary = failures_by_constraint(results)

    assert summary["min_value"] == 1
    assert summary["max_value"] == 1
    assert summary["regex_pattern"] == 1


def test_failed_rows() -> None:
    """
    Verify failed row indexes are unique and sorted.
    """
    results = [result for result in create_validation_results() if not result.passed]

    summary = failed_rows(results)

    assert summary == [1, 2]


def test_generate_validation_report() -> None:
    """
    Verify complete validation report generation.
    """
    results = create_validation_results()

    report = generate_validation_report(results)

    assert report["total_results"] == 4
    assert report["passed_count"] == 1
    assert report["failed_count"] == 3
    assert report["has_failures"] is True

    assert report["failures_by_column"]["age"] == 2
    assert report["failures_by_constraint"]["regex_pattern"] == 1
    assert report["failed_rows"] == [1, 2]

    assert len(report["failed_results"]) == 3


def test_generate_validation_report_without_failures() -> None:
    """
    Verify report behavior when all validations pass.
    """
    results = [
        ValidationResult(
            column_name="customer_id",
            constraint_type="required",
            passed=True,
            message="Required constraint passed.",
        )
    ]

    report = generate_validation_report(results)

    assert report["total_results"] == 1
    assert report["passed_count"] == 1
    assert report["failed_count"] == 0
    assert report["has_failures"] is False
    assert report["failures_by_column"] == {}
    assert report["failures_by_constraint"] == {}
    assert report["failed_rows"] == []
    assert report["failed_results"] == []
