import json
from pathlib import Path

from data_processor.core.pipeline import run_csv_pipeline
from data_processor.validators.constraint_config import load_constraints_from_config
from scripts.run_csv_pipeline import main


EXAMPLE_CSV_PATH = Path("examples/csv/customer_migration_sample.csv")
EXAMPLE_CONSTRAINTS_PATH = Path("examples/csv/customer_constraints.json")


def test_example_customer_migration_workflow(tmp_path: Path) -> None:
    """
    Verify the documented customer migration example works end to end.
    """
    output_path = tmp_path / "customer_migration_clean.csv"
    report_path = tmp_path / "customer_migration_report.json"
    html_report_path = tmp_path / "customer_migration_report.html"
    quarantine_candidates_path = tmp_path / "quarantine_candidates.json"
    quarantine_rows_path = tmp_path / "quarantine_rows.csv"
    accepted_rows_path = tmp_path / "accepted_rows.csv"

    constraints_config = json.loads(
        EXAMPLE_CONSTRAINTS_PATH.read_text(encoding="utf-8")
    )
    constraints = load_constraints_from_config(constraints_config)

    result = run_csv_pipeline(
        input_path=EXAMPLE_CSV_PATH,
        output_path=output_path,
        report_path=report_path,
        html_report_path=html_report_path,
        quarantine_candidates_path=quarantine_candidates_path,
        quarantine_rows_path=quarantine_rows_path,
        accepted_rows_path=accepted_rows_path,
        constraints=constraints,
    )

    assert output_path.exists()
    assert report_path.exists()
    assert html_report_path.exists()
    assert quarantine_candidates_path.exists()
    assert quarantine_rows_path.exists()
    assert accepted_rows_path.exists()

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
    exported_quarantine_candidates = json.loads(
        quarantine_candidates_path.read_text(encoding="utf-8")
    )
    html_report = html_report_path.read_text(encoding="utf-8")
    quarantine_rows = quarantine_rows_path.read_text(encoding="utf-8")
    accepted_rows = accepted_rows_path.read_text(encoding="utf-8")

    assert exported_report["table_name"] == "customer_migration_sample"
    assert "validation_report" in exported_report
    assert "row_classification" in exported_report
    assert "quarantine_candidates" in exported_report
    assert exported_quarantine_candidates["candidate_count"] > 0
    assert "CSV Diagnostic Report" in html_report
    assert "Pipeline Status" in html_report
    assert "Quarantine Candidates" in html_report
    assert "invalid-email" in quarantine_rows
    assert "TOTAL" in quarantine_rows
    assert "alice@example.com" in accepted_rows


def test_example_customer_migration_workflow_with_profile(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify the documented example can run through the CLI with a profile.
    """
    output_path = tmp_path / "profile_customer_migration_clean.csv"
    report_path = tmp_path / "profile_customer_migration_report.json"

    monkeypatch.setattr(
        "sys.argv",
        [
            "run_csv_pipeline.py",
            str(EXAMPLE_CSV_PATH),
            str(output_path),
            "--profile",
            "migration_audit",
            "--constraints-path",
            str(EXAMPLE_CONSTRAINTS_PATH),
            "--report-path",
            str(report_path),
        ],
    )

    exit_code = main()

    assert exit_code == 0
    assert output_path.exists()
    assert report_path.exists()

    exported_report = json.loads(report_path.read_text(encoding="utf-8"))

    assert exported_report["table_name"] == "customer_migration_sample"
    assert "quarantine_candidates" in exported_report
