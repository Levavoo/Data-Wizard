import pytest

from data_processor.config.profile_resolver import resolve_profile_options


def test_resolve_profile_options_uses_default_when_profile_is_none() -> None:
    result = resolve_profile_options(None)

    assert result["profile_name"] == "default"
    assert result["strict_mode"] is False


def test_resolve_profile_options_resolves_known_profile() -> None:
    result = resolve_profile_options("strict_crm")

    assert result["profile_name"] == "strict_crm"
    assert result["strict_mode"] is True
    assert "quarantine_rows" in result["recommended_outputs"]


def test_resolve_profile_options_applies_overrides() -> None:
    result = resolve_profile_options(
        "strict_crm",
        overrides={"strict_mode": False},
    )

    assert result["profile_name"] == "strict_crm"
    assert result["strict_mode"] is False


def test_resolve_profile_options_ignores_none_overrides() -> None:
    result = resolve_profile_options(
        "strict_crm",
        overrides={"strict_mode": None},
    )

    assert result["strict_mode"] is True


def test_resolve_profile_options_raises_unknown_profile_error() -> None:
    with pytest.raises(ValueError, match="Unknown cleaning profile"):
        resolve_profile_options("missing")
