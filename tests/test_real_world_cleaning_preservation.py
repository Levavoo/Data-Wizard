from pathlib import Path

from data_processor.core.pipeline import run_csv_pipeline


HEAVY_FIXTURE_PATH = Path("tests/fixtures/csv/real_world_messy_customers_heavy.csv")


def _run_fixture(tmp_path: Path) -> dict:
    output_path = tmp_path / "real_world_messy_customers_clean.csv"

    return run_csv_pipeline(
        input_path=HEAVY_FIXTURE_PATH,
        output_path=output_path,
    )


def _row_by_name(result: dict, name: str) -> dict:
    table = result["table"]

    for row in table.rows:
        if row.get("name") == name:
            return row

    raise AssertionError(f"Expected row with name {name!r} to exist.")


def test_real_world_cleaning_trims_surrounding_whitespace(tmp_path: Path) -> None:
    """
    Verify safe text cleanup for leading/trailing whitespace.
    """
    result = _run_fixture(tmp_path)

    alice = _row_by_name(result, "Alice Smith")
    trailing_country = _row_by_name(result, "Trailing Spaces")
    email_spaces = _row_by_name(result, "Email Spaces")

    assert alice["name"] == "Alice Smith"
    assert trailing_country["country"] == "Germany"
    assert email_spaces["email"] == "emailspace@example.com"


def test_real_world_cleaning_collapses_internal_whitespace(tmp_path: Path) -> None:
    """
    Verify repeated internal whitespace is normalized by the text cleaner.
    """
    result = _run_fixture(tmp_path)

    row = _row_by_name(result, "Multiple Internal Spaces")

    assert row["name"] == "Multiple Internal Spaces"


def test_real_world_preserves_multiline_and_escaped_quote_notes(tmp_path: Path) -> None:
    """
    Verify multiline quoted fields and escaped quote text are preserved.
    """
    result = _run_fixture(tmp_path)

    multiline = _row_by_name(result, "Uma Multiline")
    quoted = _row_by_name(result, "Tina Quote")

    assert "First line of note" in multiline["notes"]
    assert "Second line of note" in multiline["notes"]
    assert "\n" in multiline["notes"]
    assert 'She said "hello" yesterday' == quoted["notes"]


def test_real_world_preserves_quoted_delimiters_inside_notes(tmp_path: Path) -> None:
    """
    Verify quoted semicolon, comma, pipe, and tab text remains inside notes.
    """
    result = _run_fixture(tmp_path)

    semicolon = _row_by_name(result, "Victor Semicolon")
    comma = _row_by_name(result, "Wendy Comma")
    pipe = _row_by_name(result, "Xavier Pipe")
    tab = _row_by_name(result, "Yara Tab")

    assert semicolon["notes"] == "Note contains; semicolon inside quotes"
    assert comma["notes"] == "Note contains, comma inside quotes"
    assert pipe["notes"] == "Note contains | pipe"
    assert "Note contains tab ->" in tab["notes"]
    assert "<- here" in tab["notes"]


def test_real_world_preserves_unicode_and_emoji_text(tmp_path: Path) -> None:
    """
    Verify Unicode and emoji text survives parsing and cleaning.
    """
    result = _run_fixture(tmp_path)

    zoe = _row_by_name(result, "Zoë Accent")
    alvaro = _row_by_name(result, "Álvaro García")
    miyuki = _row_by_name(result, "Miyuki 山田")
    emoji = _row_by_name(result, "Ola Emoji")

    assert zoe["notes"] == "Unicode name"
    assert alvaro["notes"] == "Unicode accents"
    assert miyuki["notes"] == "Unicode CJK"
    assert emoji["notes"] == "contains emoji 😀"


def test_real_world_preserves_risky_text_as_text(tmp_path: Path) -> None:
    """
    Verify formula-like and HTML-like note values remain text.

    This does not claim spreadsheet injection hardening is solved. It only checks
    that the pipeline does not execute or reinterpret these strings.
    """
    result = _run_fixture(tmp_path)

    html = _row_by_name(result, "HTML Text")
    formula = _row_by_name(result, "Formula Text")
    injection = _row_by_name(result, "Injection Like")

    assert html["notes"] == "<b>HTML-like note</b>"
    assert formula["notes"] == "=SUM(A1:A2) should stay text"
    assert injection["notes"] == "+CMD|' /C calc'!A0"


def test_real_world_preserves_phone_values_as_text_like_values(tmp_path: Path) -> None:
    """
    Verify phone values with plus signs and spaces remain text-like values.
    """
    result = _run_fixture(tmp_path)

    alice = _row_by_name(result, "Alice Smith")
    charlie = _row_by_name(result, "Charlie Dupont")
    grace = _row_by_name(result, "Grace Lee")

    assert alice["phone"] == "+49 30 123456"
    assert charlie["phone"] == "+33 1 44 55 66"
    assert grace["phone"] == "+1 212 555 0100"
