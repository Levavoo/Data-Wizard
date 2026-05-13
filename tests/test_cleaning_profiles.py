import pytest

from data_processor.config.cleaning_profiles import get_builtin_profile
from data_processor.config.cleaning_profiles import list_builtin_profile_names


def test_list_builtin_profile_names() -> None:
    assert list_builtin_profile_names() == [
        "default",
        "light_touch",
        "migration_audit",
        "strict_crm",
    ]


def test_default_profile_matches_existing_behavior() -> None:
    profile = get_builtin_profile("default")

    assert profile.name == "default"
    assert profile.strict_mode is False
    assert profile.recommended_outputs == ()


def test_strict_crm_profile_enables_strict_mode() -> None:
    profile = get_builtin_profile("strict_crm")

    assert profile.strict_mode is True
    assert "json_report" in profile.recommended_outputs
    assert "quarantine_rows" in profile.recommended_outputs


def test_unknown_profile_raises_clear_error() -> None:
    with pytest.raises(ValueError, match="Unknown cleaning profile"):
        get_builtin_profile("unknown")
