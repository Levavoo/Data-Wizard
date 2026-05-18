"""
Generate deterministic CSV fixtures for performance testing.

Generated files are performance artifacts and should not be committed by default.
"""

import argparse
import csv
from pathlib import Path

DEFAULT_OUTPUT_PATH = Path("data/performance/csv_performance_fixture.csv")
DEFAULT_ROW_COUNT = 1_000
DEFAULT_DELIMITER = ","

COUNTRIES = [
    "Germany",
    "France",
    "Italy",
    "Spain",
    "Norway",
    "Japan",
    "USA",
]


def parse_arguments() -> argparse.Namespace:
    """
    Parse CLI arguments.
    """
    parser = argparse.ArgumentParser(
        description="Generate deterministic CSV fixtures for performance testing."
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=DEFAULT_ROW_COUNT,
        help="Number of data rows to generate.",
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Output CSV path.",
    )
    parser.add_argument(
        "--delimiter",
        default=DEFAULT_DELIMITER,
        help="CSV delimiter to use.",
    )
    parser.add_argument(
        "--bom",
        action="store_true",
        help="Write file with UTF-8 BOM.",
    )
    parser.add_argument(
        "--dirty-every",
        type=int,
        default=25,
        help="Inject controlled dirty values every N rows. Use 0 to disable.",
    )

    return parser.parse_args()


def generate_csv_performance_fixture(
    output_path: Path,
    row_count: int,
    delimiter: str = DEFAULT_DELIMITER,
    include_bom: bool = False,
    dirty_every: int = 25,
) -> Path:
    """
    Generate a deterministic customer-like CSV fixture.

    Args:
        output_path:
            Target CSV path.

        row_count:
            Number of data rows to generate.

        delimiter:
            CSV delimiter.

        include_bom:
            Whether to write a UTF-8 BOM.

        dirty_every:
            Inject controlled dirty values every N rows. Use 0 to disable.

    Returns:
        Output path.
    """
    if row_count < 0:
        raise ValueError("row_count must be non-negative.")

    if not delimiter:
        raise ValueError("delimiter must not be empty.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if include_bom else "utf-8"

    with output_path.open(mode="w", encoding=encoding, newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=_fieldnames(),
            delimiter=delimiter,
        )
        writer.writeheader()

        for index in range(1, row_count + 1):
            writer.writerow(_build_row(index, dirty_every=dirty_every))

    return output_path


def _fieldnames() -> list[str]:
    """
    Return generated fixture headers.
    """
    return [
        "customer_id",
        "name",
        "email",
        "country",
        "amount",
        "signup_date",
        "active",
        "notes",
        "phone",
        "postal_code",
        "score",
    ]


def _build_row(index: int, dirty_every: int) -> dict[str, str]:
    """
    Build one deterministic customer row.
    """
    country = COUNTRIES[index % len(COUNTRIES)]
    amount = f"{1000 + index}.50"
    signup_date = f"2024-05-{(index % 28) + 1:02d}"
    active = "true" if index % 2 == 0 else "false"
    email = f"customer{index}@example.com"
    score = str(index % 101)
    notes = f"Generated customer row {index}"

    if dirty_every and index % dirty_every == 0:
        amount = "1.200,50"
        notes = "Controlled dirty row with EU amount"

    if dirty_every and index % (dirty_every * 2) == 0:
        email = "invalid-email"
        active = "maybe"
        notes = "Controlled invalid email and boolean"

    if dirty_every and index % (dirty_every * 3) == 0:
        country = "Atlantis"
        score = "150"
        notes = "Controlled invalid country and score"

    return {
        "customer_id": str(index),
        "name": f"Customer {index}",
        "email": email,
        "country": country,
        "amount": amount,
        "signup_date": signup_date,
        "active": active,
        "notes": notes,
        "phone": f"+49 30 {100000 + index}",
        "postal_code": f"{index % 100000:05d}",
        "score": score,
    }


def main() -> int:
    """
    CLI entry point.
    """
    args = parse_arguments()

    output_path = generate_csv_performance_fixture(
        output_path=args.output_path,
        row_count=args.rows,
        delimiter=args.delimiter,
        include_bom=args.bom,
        dirty_every=args.dirty_every,
    )

    print("CSV performance fixture generated.")
    print(f"Rows: {args.rows}")
    print(f"Output path: {output_path}")
    print(f"Delimiter: {repr(args.delimiter)}")
    print(f"UTF-8 BOM: {args.bom}")
    print(f"Dirty every: {args.dirty_every}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
