"""
Cleaning profile resolver.

This module resolves a named built-in profile plus explicit overrides into a
plain options dictionary. It does not run the pipeline.
"""

from typing import Any

from data_processor.config.cleaning_profiles import get_builtin_profile


def resolve_profile_options(
    profile_name: str | None,
    overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Resolve profile defaults and explicit overrides into pipeline option values.

    Args:
        profile_name:
            Optional built-in profile name. If omitted, `default` is used.

        overrides:
            Optional explicit override values. Values set to `None` are ignored.

    Returns:
        Resolved profile option dictionary.
    """
    if profile_name is None:
        profile_name = "default"

    profile = get_builtin_profile(profile_name)

    resolved = {
        "profile_name": profile.name,
        "profile_description": profile.description,
        "strict_mode": profile.strict_mode,
        "recommended_outputs": profile.recommended_outputs,
        "profile_notes": profile.notes,
    }

    if overrides is not None:
        for key, value in overrides.items():
            if value is not None:
                resolved[key] = value

    return resolved
