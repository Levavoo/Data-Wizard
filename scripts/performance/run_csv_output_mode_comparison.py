"""
Compare CSV pipeline output mode performance.

This script is opt-in and generates performance artifacts under data/performance.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.performance.run_csv_performance_baseline import parse_arguments as _parse_baseline_arguments
from scripts.performance.run_csv_performance_baseline import run_baseline

DEFAULT_ROWS = 1_000
DEFAULT_OUTPUT_DIR = Path("data/performance/output_modes")

SCENARIOS = {
    "clean_only": {
        "json_report": False,
        "html_report": False,
        "quarantine_exports": False,
    },
    "json_report": {
        "json_report": True,
        "html_report": False,
        "quarantine_exports": False,
    },
    "html_report": {
        "json_report": False,
        "html_report": True,
        "quarantine_exports": False,
    },
    "quarantine_exports": {
        "json_report": False,
        "html_report": False,
        "quarantine_exports": True,
    },
    "full_outputs": {
        "json_report": True,
        "html_report": True,
        "quarantine_exports": True,
    },
}


def parse_arguments() -> argparse.Namespace:
    """
    Parse CLI arguments.
    """
    parser = argparse.ArgumentParser(
        description="Compare CSV pipeline output mode performance."
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=DEFAULT_ROWS,
        help="Number of generated fixture rows per scenario.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Output directory for generated fixtures, outputs, and metrics.",
    )
    parser.add_argument(
        "--delimiter",
        default=",",
        help="Fixture delimiter.",
    )
    parser.add_argument(
        "--bom",
        action="store_true",
        help="Generate UTF-8 BOM fixtures.",
    )
    parser.add_argument(
        "--dirty-every",
        type=int,
        default=25,
        help="Inject controlled dirty values every N rows. Use 0 to disable.",
    )

    return parser.parse_args()


def run_output_mode_comparison(args: argparse.Namespace) -> dict[str, Any]:
    """
    Run all output mode scenarios and return comparison metrics.
    """
    args.output_dir.mkdir(parents=True, exist_ok=True)
    scenario_metrics = []

    for scenario_name, options in SCENARIOS.items():
        baseline_args = _build_baseline_args(args, scenario_name, options)
        metrics = run_baseline(baseline_args)
        metrics["scenario"] = scenario_name
        scenario_metrics.append(metrics)

    comparison = {
        "row_count": args.rows,
        "scenario_count": len(scenario_metrics),
        "scenarios": scenario_metrics,
    }

    comparison_path = args.output_dir / "output_mode_comparison.json"
    comparison_path.write_text(
        json.dumps(comparison, indent=2),
        encoding="utf-8",
    )

    comparison["comparison_path"] = str(comparison_path)
    return comparison


def _build_baseline_args(
    args: argparse.Namespace,
    scenario_name: str,
    options: dict[str, bool],
) -> argparse.Namespace:
    """
    Build baseline runner arguments for one scenario.
    """
    scenario_dir = args.output_dir / scenario_name

    baseline_argv = [
        "run_csv_performance_baseline.py",
        "--rows",
        str(args.rows),
        "--fixture-path",
        str(scenario_dir / "fixture.csv"),
        "--output-path",
        str(scenario_dir / "clean.csv"),
        "--metrics-path",
        str(scenario_dir / "metrics.json"),
        "--delimiter",
        args.delimiter,
        "--dirty-every",
        str(args.dirty_every),
    ]

    if args.bom:
        baseline_argv.append("--bom")

    if options["json_report"]:
        baseline_argv.append("--json-report")

    if options["html_report"]:
        baseline_argv.append("--html-report")

    if options["quarantine_exports"]:
        baseline_argv.append("--quarantine-exports")

    original_argv = sys.argv
    try:
        sys.argv = baseline_argv
        return _parse_baseline_arguments()
    finally:
        sys.argv = original_argv


def print_summary(comparison: dict[str, Any]) -> None:
    """
    Print readable comparison summary.
    """
    print("CSV output mode performance comparison completed.")
    print(f"Rows: {comparison['row_count']}")
    print(f"Scenarios: {comparison['scenario_count']}")

    for metrics in comparison["scenarios"]:
        print(
            f"- {metrics['scenario']}: "
            f"{metrics['runtime_seconds']:.4f}s, "
            f"{metrics['rows_per_second']:.2f} rows/s"
        )

    print(f"Comparison path: {comparison['comparison_path']}")


def main() -> int:
    """
    CLI entry point.
    """
    args = parse_arguments()
    comparison = run_output_mode_comparison(args)
    print_summary(comparison)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
