"""
Command-line runner for the CSV cleaning pipeline.

This script allows the CSV pipeline to be executed from PowerShell.

Example:
    python scripts/run_csv_pipeline.py data/raw/input.csv data/processed/output.csv
"""

import argparse
from pathlib import Path
from pprint import pprint

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

    return parser.parse_args()


def main() -> None:
    """
    Run the CSV pipeline from command-line arguments.
    """
    args = parse_arguments()

    result = run_csv_pipeline(
        input_path=args.input_path,
        output_path=args.output_path,
    )

    print("CSV pipeline completed.")
    print()
    print(f"Input file: {args.input_path}")
    print(f"Output file: {args.output_path}")
    print()
    print("Quality report:")
    pprint(result["quality_report"])


if __name__ == "__main__":
    main()
