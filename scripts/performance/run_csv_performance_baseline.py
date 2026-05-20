"""
Run CSV pipeline baseline performance measurements.

This script is opt-in and should not be part of normal correctness tests.
Generated metrics are artifacts and should not be committed by default.
"""

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data_processor.core.pipeline import run_csv_pipeline
from scripts.performance.generate_csv_performance_fixture import (
    generate_csv_performance_fixture,
)

DEFAULT_ROWS = 1_000
DEFAULT_FIXTURE_PATH = Path("data/performance/csv_performance_fixture.csv")
DEFAULT_OUTPUT_PATH = Path("data/performance/csv_performance_clean.csv")
DEFAULT_METRICS_PATH = Path("data/performance/csv_performance_baseline.json")


def parse_arguments() -> argparse.Namespace:
    """
    Parse CLI arguments.
    """
    parser = argparse.ArgumentParser(
        description="Run CSV pipeline baseline performance measurements."
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=DEFAULT_ROWS,
        help="Number of generated fixture rows.",
    )
    parser.add_argument(
        "--fixture-path",
        type=Path,
        default=DEFAULT_FIXTURE_PATH,
        help="Generated fixture path.",
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Clean CSV output path.",
    )
    parser.add_argument(
        "--metrics-path",
        type=Path,
        default=DEFAULT_METRICS_PATH,
        help="Metrics JSON output path.",
    )
    parser.add_argument(
        "--delimiter",
        default=",",
        help="Fixture delimiter.",
    )
    parser.add_argument(
        "--bom",
        action="store_true",
        help="Generate UTF-8 BOM fixture.",
    )
    parser.add_argument(
        "--dirty-every",
        type=int,
        default=25,
        help="Inject controlled dirty values every N rows. Use 0 to disable.",
    )
    parser.add_argument(
        "--json-report",
        action="store_true",
        help="Generate JSON diagnostic report during the run.",
    )
    parser.add_argument(
        "--html-report",
        action="store_true",
        help="Generate HTML diagnostic report during the run.",
    )
    parser.add_argument(
        "--quarantine-exports",
        action="store_true",
        help="Generate quarantine candidate, quarantine rows, and accepted rows outputs.",
    )

    return parser.parse_args()


def run_baseline(args: argparse.Namespace) -> dict[str, Any]:
    """
    Generate fixture, run pipeline, and collect metrics.
    """
    args.fixture_path.parent.mkdir(parents=True, exist_ok=True)
    args.output_path.parent.mkdir(parents=True, exist_ok=True)
    args.metrics_path.parent.mkdir(parents=True, exist_ok=True)

    generate_csv_performance_fixture(
        output_path=args.fixture_path,
        row_count=args.rows,
        delimiter=args.delimiter,
        include_bom=args.bom,
        dirty_every=args.dirty_every,
    )

    report_path = _sibling_path(args.output_path, "_report.json") if args.json_report else None
    html_report_path = (
        _sibling_path(args.output_path, "_report.html") if args.html_report else None
    )
    quarantine_candidates_path = None
    quarantine_rows_path = None
    accepted_rows_path = None

    if args.quarantine_exports:
        quarantine_candidates_path = _sibling_path(
            args.output_path,
            "_quarantine_candidates.json",
        )
        quarantine_rows_path = _sibling_path(args.output_path, "_quarantine_rows.csv")
        accepted_rows_path = _sibling_path(args.output_path, "_accepted_rows.csv")

    started_at = time.perf_counter()
    result = run_csv_pipeline(
        input_path=args.fixture_path,
        output_path=args.output_path,
        report_path=report_path,
        html_report_path=html_report_path,
        quarantine_candidates_path=quarantine_candidates_path,
        quarantine_rows_path=quarantine_rows_path,
        accepted_rows_path=accepted_rows_path,
    )
    runtime_seconds = time.perf_counter() - started_at

    metrics = _build_metrics(
        args=args,
        result=result,
        runtime_seconds=runtime_seconds,
        report_path=report_path,
        html_report_path=html_report_path,
        quarantine_candidates_path=quarantine_candidates_path,
        quarantine_rows_path=quarantine_rows_path,
        accepted_rows_path=accepted_rows_path,
    )

    args.metrics_path.write_text(
        json.dumps(metrics, indent=2),
        encoding="utf-8",
    )

    return metrics


def _sibling_path(path: Path, suffix: str) -> Path:
    """
    Build an output artifact path next to the clean CSV output.
    """
    return path.with_name(f"{path.stem}{suffix}")


def _build_metrics(
    args: argparse.Namespace,
    result: dict[str, Any],
    runtime_seconds: float,
    report_path: Path | None,
    html_report_path: Path | None,
    quarantine_candidates_path: Path | None,
    quarantine_rows_path: Path | None,
    accepted_rows_path: Path | None,
) -> dict[str, Any]:
    """
    Build serializable metrics.
    """
    table = result["table"]
    row_count = len(table.rows)
    column_count = len(table.schema.column_names())
    rows_per_second = row_count / runtime_seconds if runtime_seconds else 0

    return {
        "scenario": _scenario_name(args),
        "row_count": row_count,
        "column_count": column_count,
        "input_file_size_bytes": _file_size(args.fixture_path),
        "output_file_size_bytes": _file_size(args.output_path),
        "runtime_seconds": runtime_seconds,
        "rows_per_second": rows_per_second,
        "pipeline_status": result["pipeline_status"]["status"],
        "outputs": {
            "clean_csv": True,
            "json_report": report_path is not None,
            "html_report": html_report_path is not None,
            "quarantine_exports": quarantine_candidates_path is not None,
        },
        "artifact_sizes": {
            "json_report_bytes": _file_size(report_path),
            "html_report_bytes": _file_size(html_report_path),
            "quarantine_candidates_bytes": _file_size(quarantine_candidates_path),
            "quarantine_rows_bytes": _file_size(quarantine_rows_path),
            "accepted_rows_bytes": _file_size(accepted_rows_path),
        },
        "fixture": {
            "path": str(args.fixture_path),
            "requested_rows": args.rows,
            "delimiter": args.delimiter,
            "bom": args.bom,
            "dirty_every": args.dirty_every,
        },
    }


def _scenario_name(args: argparse.Namespace) -> str:
    """
    Build a readable scenario name.
    """
    outputs = ["clean"]

    if args.json_report:
        outputs.append("json")

    if args.html_report:
        outputs.append("html")

    if args.quarantine_exports:
        outputs.append("quarantine")

    return f"rows_{args.rows}_{'_'.join(outputs)}"


def _file_size(path: Path | None) -> int | None:
    """
    Return file size if path exists.
    """
    if path is None or not path.exists():
        return None

    return path.stat().st_size


def print_summary(metrics: dict[str, Any], metrics_path: Path) -> None:
    """
    Print a readable metrics summary.
    """
    print("CSV performance baseline completed.")
    print(f"Scenario: {metrics['scenario']}")
    print(f"Rows: {metrics['row_count']}")
    print(f"Columns: {metrics['column_count']}")
    print(f"Runtime seconds: {metrics['runtime_seconds']:.4f}")
    print(f"Rows per second: {metrics['rows_per_second']:.2f}")
    print(f"Pipeline status: {metrics['pipeline_status']}")
    print(f"Metrics path: {metrics_path}")


def main() -> int:
    """
    CLI entry point.
    """
    args = parse_arguments()
    metrics = run_baseline(args)
    print_summary(metrics, args.metrics_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
