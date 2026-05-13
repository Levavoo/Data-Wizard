import json
from pathlib import Path

from data_processor.core.pipeline import run_csv_pipeline
from data_processor.validators.constraint_config import load_constraints_from_config


EXAMPLE_CSV_PATH = Path("examples/csv/customer_migration_sample.csv")
EXAMPLE_CONSTRAINTS_PATH = Path("examples/csv/customer_constraints.json")


def test_example_customer_migration_workflow(tmp_path: Path) -> None:
    """
    Verify the documented customer migration example works end to end.
    """
    output_path = tmp_path / "customer_migration_clean.csv"
    report_path = tmp_path / "customer_migration_report.json"
    html_report_path = tmp_path / "customer_migration_report.html"

    constraints_config = json.loads(
        EXAMPLE_CONSTRAINTS_PATH.read_text(encoding="utf-8")
    )
    constraints = load_constraints_from_config(constraints_config)

    result = run_csv_pipeline(
        input_path=EXAMPLE_CSV_PATH,
        output_path=output_path,
        report_path=report_path,
        html_report_path=html_report_path,
        constraints=constraints,
    )

    assert output_path.exists()
    assert report_path.exists()
    assert html_report_path.exists()

    diagnostic_bundle = result["diagnostic_bundle"]
    pipeline_status = result["pipeline_status"]

    assert "parse_diagnostics" in diagnostic_bundle
    assert "quality_report" in diagnostic_bundle
    assert "column_profiles" in diagnostic_bundle
    assert "row_profiles" in diagnostic_bundle
    assert "row_classification" in diagnostic_bundle
    assert "type_diagnostics" in diagnostic_bundle
    assert "validation_report" in diagnostic_bundle
    assert "quarantine_candidates" in diagnostic_bundle

    validation_report = diagnostic_bundle["validation_report"]
    row_classification = diagnostic_bundle["row_classification"]
    quarantine_candidates = diagnostic_bundle["quarantine_candidates"]

    assert validation_report["has_failures"] is True
    assert validation_report["failed_count"] > 0
    assert len(row_classification["suspicious_rows"]) >= 2
    assert quarantine_candidates["candidate_count"] > 0
    assert quarantine_candidates["summary"]["error"] > 0
    assert quarantine_candidates["summary"]["warning"] > 0
    assert pipeline_status["status"] == "completed_with_warnings"
    assert pipeline_status["strict_mode"] is False
    assert pipeline_status["strict_mode_failed"] is False

    exported_report = json.loads(report_path.read_text(encoding="utf-8"))
    html_report = html_report_path.read_text(encoding="utf-8")

    assert exported_report["table_name"] == "customer_migration_sample"
    assert "validation_report" in exported_report
    assert "row_classification" in exported_report
    assert "quarantine_candidates" in exported_report
    assert "CSV Diagnostic Report" in html_report
    assert "Pipeline Status" in html_report
    assert "Quarantine Candidates" in html_report
