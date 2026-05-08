"""
Command-line runner for the CSV cleaning pipeline.

This script allows the CSV pipeline to be executed from PowerShell.

Example:
    python scripts/run_csv_pipeline.py data/raw/input.csv data/processed/output.csv

With report:
    python scripts/run_csv_pipeline.py data/raw/input.csv data/processed/output.csv --report-path data/processed/report.json
"""

import argparse
import sys
from pathlib import Path
from pprint import pprint

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from data_processor.core.pipeline import run_csv_pipeline


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

    return parser.parse_args()


def main() -> None:
    """
    Run the CSV pipeline from command-line arguments.
    """
    args = parse_arguments()

    result = run_csv_pipeline(
        input_path=args.input_path,
        output_path=args.output_path,
        report_path=args.report_path,
    )

    print("CSV pipeline completed.")
    print()
    print(f"Input file: {args.input_path}")
    print(f"Output file: {args.output_path}")

    if args.report_path is not None:
        print(f"Diagnostic report: {args.report_path}")

    print()
    print("Quality report:")
    pprint(result["quality_report"])


if __name__ == "__main__":
    main()
