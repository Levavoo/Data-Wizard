"""
Command-line entry point for the JSON pipeline.
"""

import argparse
from pathlib import Path

from data_processor.core.json_pipeline import run_json_pipeline
from data_processor.validators.constraint_config import load_constraints_from_file


def parse_arguments() -> argparse.Namespace:
    """
    Parse CLI arguments.
    """
    parser = argparse.ArgumentParser(description="Run the JSON data pipeline.")
    parser.add_argument("input_path", type=Path, help="Source JSON file path.")
    parser.add_argument("output_path", type=Path, help="Clean CSV output path.")
    parser.add_argument("--constraints-path", type=Path, default=None)
    parser.add_argument("--report-path", type=Path, default=None)
    parser.add_argument("--html-report-path", type=Path, default=None)
    parser.add_argument("--quarantine-candidates-path", type=Path, default=None)
    parser.add_argument("--quarantine-rows-path", type=Path, default=None)
    parser.add_argument("--accepted-rows-path", type=Path, default=None)
    parser.add_argument("--strict", action="store_true")

    return parser.parse_args()


def main() -> int:
    """
    CLI entry point.
    """
    args = parse_arguments()
    constraints = []

    if args.constraints_path is not None:
        constraints = load_constraints_from_file(args.constraints_path)

    result = run_json_pipeline(
        input_path=args.input_path,
        output_path=args.output_path,
        report_path=args.report_path,
        html_report_path=args.html_report_path,
        quarantine_candidates_path=args.quarantine_candidates_path,
        quarantine_rows_path=args.quarantine_rows_path,
        accepted_rows_path=args.accepted_rows_path,
        constraints=constraints,
        strict_mode=args.strict,
    )

    pipeline_status = result["pipeline_status"]

    print("JSON pipeline completed.")
    print(f"Input: {args.input_path}")
    print(f"Output: {args.output_path}")
    print(f"Status: {pipeline_status['status']}")

    if args.report_path is not None:
        print(f"JSON report: {args.report_path}")

    if args.html_report_path is not None:
        print(f"HTML report: {args.html_report_path}")

    if args.quarantine_candidates_path is not None:
        print(f"Quarantine candidates: {args.quarantine_candidates_path}")

    if args.quarantine_rows_path is not None:
        print(f"Quarantine rows: {args.quarantine_rows_path}")

    if args.accepted_rows_path is not None:
        print(f"Accepted rows: {args.accepted_rows_path}")

    return 1 if pipeline_status.get("strict_failed") else 0


if __name__ == "__main__":
    raise SystemExit(main())
