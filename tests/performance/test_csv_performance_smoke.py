from pathlib import Path

from scripts.performance.generate_csv_performance_fixture import (
    generate_csv_performance_fixture,
)
from scripts.performance.run_csv_performance_baseline import parse_arguments
from scripts.performance.run_csv_performance_baseline import run_baseline


def test_generate_csv_performance_fixture_creates_small_file(tmp_path: Path) -> None:
    """
    Verify the performance fixture generator creates deterministic small output.
    """
    output_path = tmp_path / "fixture.csv"

    result_path = generate_csv_performance_fixture(
        output_path=output_path,
        row_count=10,
        dirty_every=5,
    )

    content = output_path.read_text(encoding="utf-8")

    assert result_path == output_path
    assert output_path.exists()
    assert "customer_id,name,email" in content.splitlines()[0]
    assert "Customer 1" in content
    assert "invalid-email" in content


def test_csv_performance_baseline_runner_writes_metrics(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify the baseline runner can produce metrics for a tiny fixture.

    This test does not enforce runtime thresholds.
    """
    fixture_path = tmp_path / "fixture.csv"
    output_path = tmp_path / "clean.csv"
    metrics_path = tmp_path / "metrics.json"

    monkeypatch.setattr(
        "sys.argv",
        [
            "run_csv_performance_baseline.py",
            "--rows",
            "10",
            "--fixture-path",
            str(fixture_path),
            "--output-path",
            str(output_path),
            "--metrics-path",
            str(metrics_path),
            "--json-report",
        ],
    )

    args = parse_arguments()
    metrics = run_baseline(args)

    assert fixture_path.exists()
    assert output_path.exists()
    assert metrics_path.exists()
    assert metrics["row_count"] == 10
    assert metrics["column_count"] == 11
    assert metrics["runtime_seconds"] >= 0
    assert metrics["rows_per_second"] >= 0
    assert metrics["outputs"]["clean_csv"] is True
    assert metrics["outputs"]["json_report"] is True
    assert metrics["artifact_sizes"]["json_report_bytes"] is not None
