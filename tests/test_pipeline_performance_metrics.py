from pathlib import Path

from data_processor.core.pipeline import run_csv_pipeline


def test_pipeline_omits_performance_metrics_by_default(tmp_path: Path) -> None:
    """
    Verify existing pipeline behavior does not include timing metrics by default.
    """
    input_path = tmp_path / "customers.csv"
    output_path = tmp_path / "clean.csv"

    input_path.write_text("name,email\nAlice,alice@example.com\n", encoding="utf-8")

    result = run_csv_pipeline(
        input_path=input_path,
        output_path=output_path,
    )

    assert output_path.exists()
    assert "performance_metrics" not in result


def test_pipeline_returns_performance_metrics_when_requested(tmp_path: Path) -> None:
    """
    Verify optional pipeline timings are returned when requested.
    """
    input_path = tmp_path / "customers.csv"
    output_path = tmp_path / "clean.csv"

    input_path.write_text("name,email\nAlice,alice@example.com\n", encoding="utf-8")

    result = run_csv_pipeline(
        input_path=input_path,
        output_path=output_path,
        collect_step_timings=True,
    )

    metrics = result["performance_metrics"]

    assert output_path.exists()
    assert metrics["adapter_read_seconds"] >= 0
    assert metrics["cleaning_seconds"] >= 0
    assert metrics["type_inference_first_pass_seconds"] >= 0
    assert metrics["type_casting_seconds"] >= 0
    assert metrics["type_inference_second_pass_seconds"] >= 0
    assert metrics["validation_seconds"] >= 0
    assert metrics["quality_report_seconds"] >= 0
    assert metrics["diagnostic_bundle_seconds"] >= 0
    assert metrics["pipeline_status_seconds"] >= 0
    assert metrics["clean_csv_export_seconds"] >= 0
