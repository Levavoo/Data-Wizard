from data_processor.adapters.delimiter_detection import detect_delimiter


def test_detect_delimiter_detects_comma() -> None:
    sample = "Name,City\nAlice,Berlin\nBob,Paris\n"

    result = detect_delimiter(sample)

    assert result["selected_delimiter"] == ","
    assert result["confidence"] == "high"


def test_detect_delimiter_detects_semicolon() -> None:
    sample = "Name;City\nAlice;Berlin\nBob;Paris\n"

    result = detect_delimiter(sample)

    assert result["selected_delimiter"] == ";"
    assert result["confidence"] == "high"


def test_detect_delimiter_detects_tab() -> None:
    sample = "Name\tCity\nAlice\tBerlin\nBob\tParis\n"

    result = detect_delimiter(sample)

    assert result["selected_delimiter"] == "\t"
    assert result["confidence"] == "high"


def test_detect_delimiter_detects_pipe() -> None:
    sample = "Name|City\nAlice|Berlin\nBob|Paris\n"

    result = detect_delimiter(sample)

    assert result["selected_delimiter"] == "|"
    assert result["confidence"] == "high"


def test_detect_delimiter_falls_back_to_comma_when_no_viable_candidate() -> None:
    sample = "single column only\nsecond line\n"

    result = detect_delimiter(sample)

    assert result["selected_delimiter"] == ","
    assert result["confidence"] == "low"
    assert "falling back to comma" in result["reason"]


def test_detect_delimiter_falls_back_to_comma_when_ambiguous() -> None:
    sample = "A,B;C\n1,2;3\n"

    result = detect_delimiter(sample)

    assert result["selected_delimiter"] == ","
    assert result["confidence"] == "low"
    assert "ambiguous" in result["reason"]
