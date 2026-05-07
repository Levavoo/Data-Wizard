from pathlib import Path

from data_processor.core.pipeline import run_csv_pipeline


def test_run_csv_pipeline_creates_output_file(tmp_path: Path) -> None:
    """
    Verify the CSV pipeline creates a cleaned output file.
    """
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"

    input_path.write_text(
        "Name,Active,Amount,Date\n"
        'Alice,YES,"1,000",2026-01-31\n'
        "Bob,no,25.50,31.01.2026\n",
        encoding="utf-8",
    )

    result = run_csv_pipeline(
        input_path=input_path,
        output_path=output_path,
    )

    assert output_path.exists()
    assert "table" in result
    assert "quality_report" in result


def test_run_csv_pipeline_quality_report(tmp_path: Path) -> None:
    """
    Verify the pipeline returns a quality report.
    """
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"

    input_path.write_text(
        "Name,Country,Email\n" "Alice,Germany,\n" "Bob,,bob@example.com\n",
        encoding="utf-8",
    )

    result = run_csv_pipeline(
        input_path=input_path,
        output_path=output_path,
    )

    report = result["quality_report"]

    assert report["table_name"] == "input"
    assert report["row_count"] == 2
    assert report["column_count"] == 3
    assert report["missing_values_by_column"]["country"] == 1
    assert report["missing_values_by_column"]["email"] == 1


def test_run_csv_pipeline_exports_cleaned_values(tmp_path: Path) -> None:
    """
    Verify cleaned values are exported.
    """
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"

    input_path.write_text(
        "Name,Active,Amount\n" " Alice ,YES,1000\n" " Bob ,no,25.50\n",
        encoding="utf-8",
    )

    run_csv_pipeline(
        input_path=input_path,
        output_path=output_path,
    )

    content = output_path.read_text(
        encoding="utf-8",
    )

    assert "Alice,true,1000" in content
    assert "Bob,false,25.5" in content
