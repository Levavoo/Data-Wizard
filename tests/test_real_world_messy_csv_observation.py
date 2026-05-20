import json
from pathlib import Path

from data_processor.core.pipeline import run_csv_pipeline
from data_processor.validators.constraint_config import load_constraints_from_config


HEAVY_FIXTURE_PATH = Path("tests/fixtures/csv/real_world_messy_customers_heavy.csv")
CONSTRAINTS_PATH = Path("tests/fixtures/csv/real_world_messy_customers_constraints.json")


def test_real_world_messy_csv_baseline_observation(tmp_path: Path) -> None:
    """
    Run the heavy messy CSV fixture through the current pipeline.

    This is a broad baseline observation test. It intentionally avoids exact row
    counts because the fixture contains malformed and ambiguous real-world data.
    """
    output_path = tmp_path / "real_world_messy_customers_clean.csv"
    report_path = tmp_path / "real_world_messy_customers_report.json"
    html_report_path = tmp_path / "real_world_messy_customers_report.html"
    quarantine_candidates_path = (
        tmp_path / "real_world_messy_customers_quarantine_candidates.json"
    )
    quarantine_rows_path = tmp_path / "real_world_messy_customers_quarantine_rows.csv"
    accepted_rows_path = tmp_path / "real_world_messy_customers_accepted_rows.csv"

    constraints_config = json.loads(CONSTRAINTS_PATH.read_text(encoding="utf-8"))
    constraints = load_constraints_from_config(constraints_config)

    result = run_csv_pipeline(
        input_path=HEAVY_FIXTURE_PATH,
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

    parse_diagnostics = diagnostic_bundle["parse_diagnostics"]
    validation_report = diagnostic_bundle["validation_report"]
    quarantine_candidates = diagnostic_bundle["quarantine_candidates"]

    assert parse_diagnostics["detection"]
    assert parse_diagnostics["header_row_index"] > 0
    assert parse_diagnostics["preamble_row_count"] > 0
    assert parse_diagnostics["delimiter"] == ";"
    assert parse_diagnostics["encoding"] == "utf-8-sig"

    assert validation_report["has_failures"] is True
    assert validation_report["failed_count"] > 0
    assert quarantine_candidates["candidate_count"] > 0
    assert pipeline_status["status"] in {
        "completed",
        "completed_with_warnings",
        "completed_with_errors",
    }

    exported_report = json.loads(report_path.read_text(encoding="utf-8"))
    exported_quarantine_candidates = json.loads(
        quarantine_candidates_path.read_text(encoding="utf-8")
    )
    html_report = html_report_path.read_text(encoding="utf-8")
    quarantine_rows = quarantine_rows_path.read_text(encoding="utf-8")
    accepted_rows = accepted_rows_path.read_text(encoding="utf-8")

    assert exported_report["table_name"] == "real_world_messy_customers_heavy"
    assert "parse_diagnostics" in exported_report
    assert "validation_report" in exported_report
    assert "quarantine_candidates" in exported_report
    assert exported_quarantine_candidates["candidate_count"] > 0
    assert "CSV Diagnostic Report" in html_report
    assert "Pipeline Status" in html_report
    assert "Quarantine Candidates" in html_report
    assert quarantine_rows.strip()
    assert accepted_rows.strip()
