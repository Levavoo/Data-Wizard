from data_processor.analysis.row_classification import classify_row
from data_processor.analysis.row_classification import classify_table_rows
from data_processor.core.column import Column
from data_processor.core.schema import Schema
from data_processor.core.table import Table


def test_classify_empty_row() -> None:
    row = {"customer_id": None, "amount": ""}

    result = classify_row(row=row, row_index=0)

    assert result["classification"] == "empty_row"
    assert result["row_index"] == 0
    assert result["confidence"] == 1.0


def test_classify_comment_row() -> None:
    row = {"customer_id": "# generated export", "amount": None}

    result = classify_row(row=row, row_index=1)

    assert result["classification"] == "comment_row"
    assert result["row_index"] == 1


def test_classify_summary_row() -> None:
    row = {"customer_id": "TOTAL", "amount": "650.50"}

    result = classify_row(row=row, row_index=2)

    assert result["classification"] == "summary_row"
    assert result["row_index"] == 2


def test_classify_footer_row() -> None:
    row = {"customer_id": "End of export", "amount": None}

    result = classify_row(row=row, row_index=3)

    assert result["classification"] == "footer_row"
    assert result["row_index"] == 3


def test_classify_garbage_row() -> None:
    row = {"customer_id": "random free text", "amount": None, "country": None}

    result = classify_row(row=row, row_index=4)

    assert result["classification"] == "garbage_row"
    assert result["row_index"] == 4


def test_classify_normal_row() -> None:
    row = {"customer_id": "1", "amount": "100", "country": "Germany"}

    result = classify_row(row=row, row_index=5)

    assert result["classification"] == "normal_row"
    assert result["row_index"] == 5


def test_classify_table_rows_reports_suspicious_rows() -> None:
    schema = Schema(
        columns=[
            Column(name="customer_id"),
            Column(name="amount"),
        ]
    )

    table = Table(
        name="orders",
        schema=schema,
        rows=[
            {"customer_id": "1", "amount": "100"},
            {"customer_id": "TOTAL", "amount": "100"},
            {"customer_id": "End of export", "amount": None},
        ],
    )

    result = classify_table_rows(table)

    assert len(result["rows"]) == 3
    assert len(result["suspicious_rows"]) == 2
    assert result["summary"] == {
        "normal_row": 1,
        "summary_row": 1,
        "footer_row": 1,
    }
    assert result["suspicious_rows"][0]["classification"] == "summary_row"
    assert result["suspicious_rows"][1]["classification"] == "footer_row"
