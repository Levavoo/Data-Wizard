"""
Command-line runner for the CSV cleaning pipeline.

This script allows the CSV pipeline to be executed from PowerShell.

Example:
    python scripts/run_csv_pipeline.py data/raw/input.csv data/processed/output.csv

With report:
    python scripts/run_csv_pipeline.py data/raw/input.csv data/processed/output.csv --report-path data/processed/report.json

With constraints:
    python scripts/run_csv_pipeline.py data/raw/input.csv data/processed/output.csv --constraints-path data/raw/constraints.json

With strict mode:
    python scripts/run_csv_pipeline.py data/raw/input.csv data/processed/output.csv --constraints-path data/raw/constraints.json --strict
"""

import argparse
import json
import sys
from pathlib import Path
from pprint import pprint

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from data_processor.core.pipeline import run_csv_pipeline
from data_processor.reports.pipeline_status import exit_code_from_pipeline_status
from data_processor.validators.constraint_config import load_constraints_from_config
from data_processor.validators.constraints import Constraint

EXECUTION_ERROR_EXIT_CODE = 1


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed argument namespace.
    """
    parser = argparse.ArgumentParser(description="Run the CSV cleaning pipeline.")

    parser.add_argument(
        "input_path",
        type=Path,
        help="Path to the input CSV file.",
    )

    parser.add_argument(
        "output_path",
        type=Path,
        help="Path where the cleaned CSV should be written.",
    )

    parser.add_argument(
        "--report-path",
        type=Path,
        default=None,
        help="Optional path where the diagnostic JSON report should be written.",
    )

    parser.add_argument(
        "--constraints-path",
        type=Path,
        default=None,
        help="Optional JSON file containing validation constraints.",
    )

    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 2 when strict policy failures are reported.",
    )

    return parser.parse_args()


def load_constraints_from_path(path: Path | None) -> list[Constraint]:
    """
    Load validation constraints from a JSON file.

    Args:
        path:
            Optional constraints JSON path.

    Returns:
        List of Constraint objects.
    """
    if path is None:
        return []

    with path.open(mode="r", encoding="utf-8") as constraints_file:
        config = json.load(constraints_file)

    return load_constraints_from_config(config)


def main() -> int:
    """
    Run the CSV pipeline from command-line arguments.

    Returns:
        Process exit code.
    """
    args = parse_arguments()

    try:
        constraints = load_constraints_from_path(args.constraints_path)

        result = run_csv_pipeline(
            input_path=args.input_path,
            output_path=args.output_path,
            report_path=args.report_path,
            constraints=constraints,
            strict_mode=args.strict,
        )
    except Exception as error:
        print("CSV pipeline failed.", file=sys.stderr)
        print(str(error), file=sys.stderr)
        return EXECUTION_ERROR_EXIT_CODE

    print("CSV pipeline completed.")
    print()
    print(f"Input file: {args.input_path}")
    print(f"Output file: {args.output_path}")

    if args.report_path is not None:
        print(f"Diagnostic report: {args.report_path}")

    if args.constraints_path is not None:
        print(f"Constraints file: {args.constraints_path}")

    print(f"Strict mode: {args.strict}")

    print()
    print("Pipeline status:")
    pprint(result["pipeline_status"])

    print()
    print("Quality report:")
    pprint(result["quality_report"])

    print()
    print("Validation report:")
    pprint(result["diagnostic_bundle"]["validation_report"])

    return exit_code_from_pipeline_status(result["pipeline_status"])


if __name__ == "__main__":
    raise SystemExit(main())
