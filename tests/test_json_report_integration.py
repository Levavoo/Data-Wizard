import json
from pathlib import Path

from data_processor.core.json_pipeline import run_json_pipeline


def test_json_report_export_contains_json_parse_diagnostics(tmp_path: Path) -> None:
    output_path = tmp_path / "customers_clean.csv"
    report_path = tmp_path / "customers_report.json"

    run_json_pipeline(
        input_path="tests/fixtures/json/nested_values_customers.json",
        output_path=output_path,
        report_path=report_path,
    )

    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert report["metadata"]["source_format"] == "json"
    assert report["parse_diagnostics"]["root_type"] == "list"
    assert report["parse_diagnostics"]["record_count"] == 2
    assert report["parse_diagnostics"]["nested_value_columns"] == ["address"]
    assert report["parse_diagnostics"]["array_value_columns"] == ["tags"]


def test_json_html_report_mentions_parse_diagnostics(tmp_path: Path) -> None:
    output_path = tmp_path / "customers_clean.csv"
    html_report_path = tmp_path / "customers_report.html"

    run_json_pipeline(
        input_path="tests/fixtures/json/nested_values_customers.json",
        output_path=output_path,
        html_report_path=html_report_path,
    )

    html_report = html_report_path.read_text(encoding="utf-8")

    assert "CSV Diagnostic Report" in html_report
    assert "Parse Diagnostics" in html_report
    assert "json" in html_report
