import json
from pathlib import Path

from data_processor.core.pipeline import run_csv_pipeline
from data_processor.validators.constraints import Constraint


def test_run_csv_pipeline_creates_output_file(tmp_path: Path) -> None:
    """
    Verify the CSV pipeline creates a cleaned output file.
    """
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"

    input_path.write_text(
        "Name,Active,Amount,Date\n"
        'Alice,YES,"1,000",2026-01-31\n'
        "Bob,no,25.50,31.01.2026\n",
        encoding="utf-8",
    )

    result = run_csv_pipeline(
        input_path=input_path,
        output_path=output_path,
    )

    assert output_path.exists()
    assert "table" in result
    assert "quality_report" in result
    assert "validation_results" in result
    assert "diagnostic_bundle" in result
    assert "pipeline_status" in result


def test_run_csv_pipeline_quality_report(tmp_path: Path) -> None:
    """
    Verify the pipeline returns a quality report.
    """
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"

    input_path.write_text(
        "Name,Country,Email\n" "Alice,Germany,\n" "Bob,,bob@example.com\n",
        encoding="utf-8",
    )

    result = run_csv_pipeline(
        input_path=input_path,
        output_path=output_path,
    )

    report = result["quality_report"]

    assert report["table_name"] == "input"
    assert report["row_count"] == 2
    assert report["column_count"] == 3
    assert report["missing_values_by_column"]["country"] == 1
    assert report["missing_values_by_column"]["email"] == 1


def test_run_csv_pipeline_exports_cleaned_values(tmp_path: Path) -> None:
    """
    Verify cleaned values are exported.
    """
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"

    input_path.write_text(
        "Name,Active,Amount\n" " Alice ,YES,1000\n" " Bob ,no,25.50\n",
        encoding="utf-8",
    )

    run_csv_pipeline(
        input_path=input_path,
        output_path=output_path,
    )

    content = output_path.read_text(
        encoding="utf-8",
    )

    assert "Alice,true,1000" in content
    assert "Bob,false,25.5" in content


def test_run_csv_pipeline_exports_european_decimal_values(tmp_path: Path) -> None:
    """
    Verify European decimal values are inferred, cast, and exported correctly.
    """
    input_path = tmp_path / "european_decimals.csv"
    output_path = tmp_path / "output.csv"

    input_path.write_text(
        "Customer ID,Amount\n"
        '1,"1.000,50"\n'
        '2,"250,75"\n'
        '3,"5.500,00"\n',
        encoding="utf-8",
    )

    result = run_csv_pipeline(
        input_path=input_path,
        output_path=output_path,
    )

    table = result["table"]
    amount_column = table.schema.get_column("amount")

    assert amount_column is not None
    assert amount_column.inferred_type == "float"

    assert table.rows == [
        {"customer_id": 1, "amount": 1000.5},
        {"customer_id": 2, "amount": 250.75},
        {"customer_id": 3, "amount": 5500.0},
    ]

    content = output_path.read_text(encoding="utf-8")

    assert "1,1000.5" in content
    assert "2,250.75" in content
    assert "3,5500.0" in content


def test_run_csv_pipeline_reports_mixed_type_diagnostics(tmp_path: Path) -> None:
    """
    Verify mixed-type columns are reported in the diagnostic bundle.
    """
    input_path = tmp_path / "mixed_type_column.csv"
    output_path = tmp_path / "output.csv"

    input_path.write_text(
        "Order ID,Amount\n"
        "1,100\n"
        "2,250.75\n"
        "3,unknown\n"
        "4,300\n"
        "5,400\n",
        encoding="utf-8",
    )

    result = run_csv_pipeline(
        input_path=input_path,
        output_path=output_path,
    )

    type_diagnostics = result["diagnostic_bundle"]["type_diagnostics"]

    assert len(type_diagnostics["mixed_type_columns"]) == 1
    mixed_column = type_diagnostics["mixed_type_columns"][0]

    assert mixed_column["column"] == "amount"
    assert mixed_column["dominant_type"] == "float"
    assert mixed_column["invalid_values"] == [
        {
            "row_index": 2,
            "value": "unknown",
            "expected_type": "float",
        }
    ]


def test_run_csv_pipeline_reports_suspicious_rows(tmp_path: Path) -> None:
    """
    Verify suspicious rows are reported without removing rows.
    """
    input_path = tmp_path / "footer_summary_rows.csv"
    output_path = tmp_path / "output.csv"

    input_path.write_text(
        "Order ID,Amount\n"
        "1,100\n"
        "2,250\n"
        "TOTAL,350\n"
        "End of export,\n",
        encoding="utf-8",
    )

    result = run_csv_pipeline(
        input_path=input_path,
        output_path=output_path,
    )

    table = result["table"]
    row_classification = result["diagnostic_bundle"]["row_classification"]

    assert table.row_count() == 4
    assert len(row_classification["suspicious_rows"]) == 2
    assert row_classification["summary"]["summary_row"] == 1
    assert row_classification["summary"]["footer_row"] == 1


def test_run_csv_pipeline_validates_constraints(tmp_path: Path) -> None:
    """
    Verify optional constraints are validated after cleaning and casting.
    """
    input_path = tmp_path / "customers.csv"
    output_path = tmp_path / "output.csv"

    input_path.write_text(
        "Customer ID,Country,Email,Amount\n"
        "1,Germany,alice@example.com,100\n"
        "1,Mars,invalid-email,-5\n"
        "3,France,bob@example.com,250\n",
        encoding="utf-8",
    )

    constraints = [
        Constraint(column_name="customer_id", constraint_type="unique"),
        Constraint(
            column_name="country",
            constraint_type="allowed_values",
            value=["Germany", "France"],
        ),
        Constraint(
            column_name="email",
            constraint_type="regex_pattern",
            value=r"^[^@]+@[^@]+\.[^@]+$",
        ),
        Constraint(column_name="amount", constraint_type="min_value", value=0),
    ]

    result = run_csv_pipeline(
        input_path=input_path,
        output_path=output_path,
        constraints=constraints,
    )

    validation_report = result["diagnostic_bundle"]["validation_report"]

    assert validation_report["failed_count"] == 4
    assert validation_report["has_failures"] is True
    assert validation_report["failures_by_column"] == {
        "customer_id": 1,
        "country": 1,
        "email": 1,
        "amount": 1,
    }
    assert result["validation_results"]


def test_run_csv_pipeline_reports_quarantine_candidates(tmp_path: Path) -> None:
    """
    Verify quarantine candidates are reported without removing rows.
    """
    input_path = tmp_path / "customers.csv"
    output_path = tmp_path / "output.csv"

    input_path.write_text(
        "Customer ID,Country,Email,Amount\n"
        "1,Germany,alice@example.com,100\n"
        "2,Mars,invalid-email,-5\n"
        "TOTAL,,,\n",
        encoding="utf-8",
    )

    constraints = [
        Constraint(
            column_name="country",
            constraint_type="allowed_values",
            value=["Germany", "France"],
        ),
        Constraint(
            column_name="email",
            constraint_type="regex_pattern",
            value=r"^[^@]+@[^@]+\.[^@]+$",
        ),
        Constraint(column_name="amount", constraint_type="min_value", value=0),
    ]

    result = run_csv_pipeline(
        input_path=input_path,
        output_path=output_path,
        constraints=constraints,
    )

    table = result["table"]
    quarantine_candidates = result["diagnostic_bundle"]["quarantine_candidates"]

    assert table.row_count() == 3
    assert quarantine_candidates["candidate_count"] >= 2
    assert quarantine_candidates["summary"]["error"] >= 1
    assert quarantine_candidates["summary"]["warning"] >= 1
    assert output_path.exists()


def test_run_csv_pipeline_exports_quarantine_files(tmp_path: Path) -> None:
    """
    Verify explicit quarantine exports do not change the normal cleaned CSV.
    """
    input_path = tmp_path / "customers.csv"
    output_path = tmp_path / "output.csv"
    quarantine_candidates_path = tmp_path / "reports" / "quarantine_candidates.json"
    quarantine_rows_path = tmp_path / "reports" / "quarantine_rows.csv"
    accepted_rows_path = tmp_path / "reports" / "accepted_rows.csv"

    input_path.write_text(
        "Customer ID,Country,Email,Amount\n"
        "1,Germany,alice@example.com,100\n"
        "2,Mars,invalid-email,-5\n"
        "TOTAL,,,\n",
        encoding="utf-8",
    )

    constraints = [
        Constraint(
            column_name="country",
            constraint_type="allowed_values",
            value=["Germany"],
        ),
        Constraint(
            column_name="email",
            constraint_type="regex_pattern",
            value=r"^[^@]+@[^@]+\.[^@]+$",
        ),
        Constraint(column_name="amount", constraint_type="min_value", value=0),
    ]

    run_csv_pipeline(
        input_path=input_path,
        output_path=output_path,
        quarantine_candidates_path=quarantine_candidates_path,
        quarantine_rows_path=quarantine_rows_path,
        accepted_rows_path=accepted_rows_path,
        constraints=constraints,
    )

    assert output_path.exists()
    assert quarantine_candidates_path.exists()
    assert quarantine_rows_path.exists()
    assert accepted_rows_path.exists()

    normal_output = output_path.read_text(encoding="utf-8")
    quarantine_output = quarantine_rows_path.read_text(encoding="utf-8")
    accepted_output = accepted_rows_path.read_text(encoding="utf-8")
    quarantine_candidates = json.loads(
        quarantine_candidates_path.read_text(encoding="utf-8")
    )

    assert "alice@example.com" in normal_output
    assert "invalid-email" in normal_output
    assert "TOTAL" in normal_output
    assert "invalid-email" in quarantine_output
    assert "TOTAL" in quarantine_output
    assert "alice@example.com" in accepted_output
    assert "invalid-email" not in accepted_output
    assert quarantine_candidates["candidate_count"] >= 2


def test_run_csv_pipeline_returns_non_strict_status_by_default(
    tmp_path: Path,
) -> None:
    """
    Verify default pipeline status remains non-strict and does not fail policy.
    """
    input_path = tmp_path / "customers.csv"
    output_path = tmp_path / "output.csv"

    input_path.write_text(
        "Email\n"
        "invalid-email\n",
        encoding="utf-8",
    )

    constraints = [
        Constraint(
            column_name="email",
            constraint_type="regex_pattern",
            value=r"^[^@]+@[^@]+\.[^@]+$",
        )
    ]

    result = run_csv_pipeline(
        input_path=input_path,
        output_path=output_path,
        constraints=constraints,
    )

    pipeline_status = result["pipeline_status"]

    assert pipeline_status["status"] == "completed_with_warnings"
    assert pipeline_status["strict_mode"] is False
    assert pipeline_status["strict_mode_failed"] is False
    assert output_path.exists()


def test_run_csv_pipeline_returns_failed_policy_in_strict_mode(
    tmp_path: Path,
) -> None:
    """
    Verify strict mode reports failed_policy without blocking export.
    """
    input_path = tmp_path / "customers.csv"
    output_path = tmp_path / "output.csv"

    input_path.write_text(
        "Email\n"
        "invalid-email\n",
        encoding="utf-8",
    )

    constraints = [
        Constraint(
            column_name="email",
            constraint_type="regex_pattern",
            value=r"^[^@]+@[^@]+\.[^@]+$",
        )
    ]

    result = run_csv_pipeline(
        input_path=input_path,
        output_path=output_path,
        constraints=constraints,
        strict_mode=True,
    )

    pipeline_status = result["pipeline_status"]

    assert pipeline_status["status"] == "failed_policy"
    assert pipeline_status["strict_mode"] is True
    assert pipeline_status["strict_mode_failed"] is True
    assert output_path.exists()


def test_run_csv_pipeline_exports_html_report(tmp_path: Path) -> None:
    """
    Verify the pipeline exports a diagnostic HTML report when requested.
    """
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"
    html_report_path = tmp_path / "reports" / "report.html"

    input_path.write_text(
        "Name,Country\n" "Alice,Germany\n" "Bob,France\n",
        encoding="utf-8",
    )

    run_csv_pipeline(
        input_path=input_path,
        output_path=output_path,
        html_report_path=html_report_path,
    )

    assert output_path.exists()
    assert html_report_path.exists()

    html = html_report_path.read_text(encoding="utf-8")

    assert "<!doctype html>" in html
    assert "CSV Diagnostic Report" in html
    assert "Pipeline Status" in html
    assert "Quality Report" in html


def test_run_csv_pipeline_converts_whitespace_only_cells_to_null(
    tmp_path: Path,
) -> None:
    """
    Verify whitespace-only CSV cells become None during pipeline cleaning.
    """
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"

    input_path.write_text(
        "Customer ID,Name,Email\n"
        '1,Alice,"   "\n'
        '2,Bob,"\t"\n',
        encoding="utf-8",
    )

    result = run_csv_pipeline(
        input_path=input_path,
        output_path=output_path,
    )

    table = result["table"]

    assert table.rows[0]["email"] is None
    assert table.rows[1]["email"] is None


def test_run_csv_pipeline_returns_diagnostic_bundle(tmp_path: Path) -> None:
    """
    Verify the pipeline returns a diagnostic bundle.
    """
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"

    input_path.write_text(
        "Name,Country\n" "Alice,Germany\n" "Bob,\n",
        encoding="utf-8",
    )

    result = run_csv_pipeline(
        input_path=input_path,
        output_path=output_path,
    )

    diagnostic_bundle = result["diagnostic_bundle"]

    assert diagnostic_bundle["table_name"] == "input"
    assert diagnostic_bundle["row_count"] == 2
    assert diagnostic_bundle["column_count"] == 2

    assert "quality_report" in diagnostic_bundle
    assert "column_profiles" in diagnostic_bundle
    assert "row_profiles" in diagnostic_bundle
    assert "row_classification" in diagnostic_bundle
    assert "type_diagnostics" in diagnostic_bundle
    assert "validation_report" in diagnostic_bundle
    assert "quarantine_candidates" in diagnostic_bundle


def test_run_csv_pipeline_exports_diagnostic_report(tmp_path: Path) -> None:
    """
    Verify the pipeline exports a diagnostic JSON report when report_path is provided.
    """
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"
    report_path = tmp_path / "report.json"

    input_path.write_text(
        "Name,Country\n" "Alice,Germany\n" "Bob,\n",
        encoding="utf-8",
    )

    run_csv_pipeline(
        input_path=input_path,
        output_path=output_path,
        report_path=report_path,
    )

    assert output_path.exists()
    assert report_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert report["table_name"] == "input"
    assert report["row_count"] == 2
    assert "quality_report" in report
    assert "column_profiles" in report
    assert "row_profiles" in report
    assert "row_classification" in report
    assert "type_diagnostics" in report
    assert "validation_report" in report
    assert "quarantine_candidates" in report
