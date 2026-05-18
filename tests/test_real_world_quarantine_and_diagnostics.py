import json
from pathlib import Path

from data_processor.core.pipeline import run_csv_pipeline
from data_processor.validators.constraint_config import load_constraints_from_config


HEAVY_FIXTURE_PATH = Path("tests/fixtures/csv/real_world_messy_customers_heavy.csv")
CONSTRAINTS_PATH = Path("tests/fixtures/csv/real_world_messy_customers_constraints.json")


def _load_constraints() -> list:
    constraints_config = json.loads(CONSTRAINTS_PATH.read_text(encoding="utf-8"))
    return load_constraints_from_config(constraints_config)


def _run_fixture_with_exports(tmp_path: Path) -> dict:
    output_path = tmp_path / "real_world_messy_customers_clean.csv"
    report_path = tmp_path / "real_world_messy_customers_report.json"
    html_report_path = tmp_path / "real_world_messy_customers_report.html"
    quarantine_candidates_path = (
        tmp_path / "real_world_messy_customers_quarantine_candidates.json"
    )
    quarantine_rows_path = tmp_path / "real_world_messy_customers_quarantine_rows.csv"
    accepted_rows_path = tmp_path / "real_world_messy_customers_accepted_rows.csv"

    result = run_csv_pipeline(
        input_path=HEAVY_FIXTURE_PATH,
        output_path=output_path,
        report_path=report_path,
        html_report_path=html_report_path,
        quarantine_candidates_path=quarantine_candidates_path,
        quarantine_rows_path=quarantine_rows_path,
        accepted_rows_path=accepted_rows_path,
        constraints=_load_constraints(),
    )

    result["output_paths"] = {
        "output": output_path,
        "report": report_path,
        "html_report": html_report_path,
        "quarantine_candidates": quarantine_candidates_path,
        "quarantine_rows": quarantine_rows_path,
        "accepted_rows": accepted_rows_path,
    }

    return result


def test_real_world_validation_and_type_diagnostics_are_present(
    tmp_path: Path,
) -> None:
    """
    Verify the heavy fixture produces validation and type diagnostics.
    """
    result = _run_fixture_with_exports(tmp_path)
    diagnostic_bundle = result["diagnostic_bundle"]

    validation_report = diagnostic_bundle["validation_report"]
    type_diagnostics = diagnostic_bundle["type_diagnostics"]

    assert validation_report["has_failures"] is True
    assert validation_report["failed_count"] > 0
    assert type_diagnostics["columns"]

    diagnostic_columns = {
        column_diagnostic["column"] for column_diagnostic in type_diagnostics["columns"]
    }

    assert "amount" in diagnostic_columns
    assert "score" in diagnostic_columns


def test_real_world_row_classification_finds_suspicious_rows(
    tmp_path: Path,
) -> None:
    """
    Verify suspicious rows are surfaced for review.
    """
    result = _run_fixture_with_exports(tmp_path)
    row_classification = result["diagnostic_bundle"]["row_classification"]

    assert len(row_classification["suspicious_rows"]) > 0

    suspicious_text = json.dumps(
        row_classification["suspicious_rows"],
        ensure_ascii=False,
    )

    assert "TOTAL" in suspicious_text or "Grand Total" in suspicious_text


def test_real_world_quarantine_candidates_are_exported(
    tmp_path: Path,
) -> None:
    """
    Verify quarantine candidate report exists and includes representative issues.
    """
    result = _run_fixture_with_exports(tmp_path)
    output_paths = result["output_paths"]
    quarantine_candidates = result["diagnostic_bundle"]["quarantine_candidates"]

    assert quarantine_candidates["candidate_count"] > 0
    assert quarantine_candidates["summary"]["error"] > 0
    assert output_paths["quarantine_candidates"].exists()

    exported_quarantine = json.loads(
        output_paths["quarantine_candidates"].read_text(encoding="utf-8")
    )

    assert exported_quarantine["candidate_count"] == quarantine_candidates["candidate_count"]
    assert exported_quarantine["summary"]["error"] > 0


def test_real_world_quarantine_and_accepted_row_exports_are_written(
    tmp_path: Path,
) -> None:
    """
    Verify quarantine and accepted row split exports are produced.

    For this intentionally heavy fixture, it is acceptable for the accepted rows
    export to contain only the header when every parsed row is considered a
    quarantine candidate.
    """
    result = _run_fixture_with_exports(tmp_path)
    output_paths = result["output_paths"]

    assert output_paths["quarantine_rows"].exists()
    assert output_paths["accepted_rows"].exists()

    quarantine_rows = output_paths["quarantine_rows"].read_text(encoding="utf-8")
    accepted_rows = output_paths["accepted_rows"].read_text(encoding="utf-8")

    assert quarantine_rows.strip()
    assert accepted_rows.strip()
    assert "customer_id" in quarantine_rows.splitlines()[0]
    assert "customer_id" in accepted_rows.splitlines()[0]
    assert "Alice Smith" in quarantine_rows


def test_real_world_reports_include_diagnostic_sections(tmp_path: Path) -> None:
    """
    Verify JSON and HTML reports contain the expected diagnostic sections.
    """
    result = _run_fixture_with_exports(tmp_path)
    output_paths = result["output_paths"]

    exported_report = json.loads(output_paths["report"].read_text(encoding="utf-8"))
    html_report = output_paths["html_report"].read_text(encoding="utf-8")

    assert "parse_diagnostics" in exported_report
    assert "validation_report" in exported_report
    assert "row_classification" in exported_report
    assert "type_diagnostics" in exported_report
    assert "quarantine_candidates" in exported_report
    assert "CSV Diagnostic Report" in html_report
    assert "Pipeline Status" in html_report
    assert "Quarantine Candidates" in html_report
