import json
from pathlib import Path

from data_processor.core.json_pipeline import run_json_pipeline
from data_processor.validators.constraints import Constraint


def test_json_pipeline_writes_clean_csv(tmp_path: Path) -> None:
    output_path = tmp_path / "customers_clean.csv"

    result = run_json_pipeline(
        input_path="tests/fixtures/json/simple_customers.json",
        output_path=output_path,
    )

    assert output_path.exists()
    assert result["table"].metadata["source_format"] == "json"
    assert result["diagnostic_bundle"]["parse_diagnostics"]["record_count"] == 2
    assert "Alice" in output_path.read_text(encoding="utf-8")


def test_json_pipeline_applies_constraints_and_exports_report(tmp_path: Path) -> None:
    output_path = tmp_path / "customers_clean.csv"
    report_path = tmp_path / "customers_report.json"

    result = run_json_pipeline(
        input_path="tests/fixtures/json/missing_keys_customers.json",
        output_path=output_path,
        report_path=report_path,
        constraints=[Constraint(column_name="email", constraint_type="required")],
    )

    assert output_path.exists()
    assert report_path.exists()
    assert result["diagnostic_bundle"]["validation_report"]["has_failures"] is True

    exported_report = json.loads(report_path.read_text(encoding="utf-8"))

    assert exported_report["metadata"]["source_format"] == "json"
    assert exported_report["parse_diagnostics"]["missing_key_counts"]["email"] == 1


def test_json_pipeline_can_collect_step_timings(tmp_path: Path) -> None:
    output_path = tmp_path / "customers_clean.csv"

    result = run_json_pipeline(
        input_path="tests/fixtures/json/simple_customers.json",
        output_path=output_path,
        collect_step_timings=True,
    )

    assert result["performance_metrics"]["adapter_read_seconds"] >= 0
    assert result["performance_metrics"]["clean_csv_export_seconds"] >= 0
