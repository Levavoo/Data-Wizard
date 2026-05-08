Replace the test input:

input_path.write_text(
    "customer_id,name\n" "1,Alice,Germany\n",
    encoding="utf-8",
)

with:

input_path.write_text(
    "customer_id,name\n"
    "1,Alice\n"
    "2,Bob,Germany\n"
    "3,Charlie\n",
    encoding="utf-8",
)

Then update the row assertion:

assert table.rows[1] == {
    "customer_id": "2",
    "name": "Bob",
}

Full corrected test:

def test_csv_adapter_extra_fields_are_ignored(tmp_path: Path) -> None:
    """
    Verify extra row fields beyond headers are ignored for now.
    """
    input_path = tmp_path / "extra_fields.csv"

    input_path.write_text(
        "customer_id,name\n"
        "1,Alice\n"
        "2,Bob,Germany\n"
        "3,Charlie\n",
        encoding="utf-8",
    )

    adapter = CsvAdapter(input_path)

    table = adapter.read()

    assert table.schema.column_names() == [
        "customer_id",
        "name",
    ]

    assert table.rows[1] == {
        "customer_id": "2",
        "name": "Bob",
    }

Then run:

black tests\test_csv_adapter.py
pytest tests\test_csv_adapter.py
pytest


Current rule:

choose first row with highest field count

That works for metadata-before-header files, but fails when one data row has an extra field:

customer_id,name        ← 2 fields, real header
1,Alice                 ← 2 fields
2,Bob,Germany           ← 3 fields, bad row
3,Charlie               ← 2 fields

The adapter incorrectly chooses:

2,Bob,Germany

as the header.

Fix csv_adapter.py

Replace only this method:

def _detect_header_row_index(
    self,
    rows: list[list[str]],
) -> int:
    """
    Detect the most likely header row.

    Current heuristic:
    choose the first row with the highest field count.

    Args:
        rows:
            Parsed CSV rows.

    Returns:
        Zero-based header row index.
    """
    max_field_count = max(len(row) for row in rows)

    for index, row in enumerate(rows):
        if len(row) == max_field_count:
            return index

    return 0

with this improved version:

def _detect_header_row_index(
    self,
    rows: list[list[str]],
) -> int:
    """
    Detect the most likely header row.

    Heuristic:
    - prefer the first row with more than one field
    - require at least one following row with the same field count
    - fall back to the first row if no stronger candidate exists

    This supports files with metadata/preamble lines before the header
    while avoiding accidental selection of a single malformed data row.
    """
    for index, row in enumerate(rows):
        field_count = len(row)

        if field_count <= 1:
            continue

        following_rows = rows[index + 1 :]

        has_matching_data_row = any(
            len(following_row) == field_count
            for following_row in following_rows
        )

        if has_matching_data_row:
            return index

    return 0
Why this works

For metadata-before-header:

row 0 → 1 field
row 1 → 1 field
row 2 → 1 field
row 3 → 5 fields
row 4 → 5 fields

It selects row 3.

For extra-field file:

row 0 → 2 fields
row 1 → 2 fields
row 2 → 3 fields
row 3 → 2 fields

It selects row 0.

Then run:

black data_processor\adapters\csv_adapter.py

pytest tests\test_csv_adapter.py

pytest