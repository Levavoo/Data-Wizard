"""
Built-in CSV cleaning profiles.

Profiles define reusable workflow defaults. They do not run the pipeline or
mutate data.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CleaningProfile:
    """
    Built-in CSV cleaning profile definition.
    """

    name: str
    description: str
    strict_mode: bool
    recommended_outputs: tuple[str, ...]
    notes: str


BUILTIN_CLEANING_PROFILES: dict[str, CleaningProfile] = {
    "default": CleaningProfile(
        name="default",
        description="Current default CSV workflow behavior.",
        strict_mode=False,
        recommended_outputs=(),
        notes="Matches existing no-profile behavior.",
    ),
    "light_touch": CleaningProfile(
        name="light_touch",
        description="Minimal review workflow for light cleaning runs.",
        strict_mode=False,
        recommended_outputs=("json_report",),
        notes="Useful when users want basic diagnostics without strict policy failure.",
    ),
    "migration_audit": CleaningProfile(
        name="migration_audit",
        description="Audit-oriented migration workflow with reports and quarantine review.",
        strict_mode=False,
        recommended_outputs=(
            "json_report",
            "html_report",
            "quarantine_candidates",
            "quarantine_rows",
            "accepted_rows",
        ),
        notes="Useful for reviewing migration issues before deciding on strict rules.",
    ),
    "strict_crm": CleaningProfile(
        name="strict_crm",
        description="Strict CRM migration workflow for constraint-sensitive imports.",
        strict_mode=True,
        recommended_outputs=(
            "json_report",
            "html_report",
            "quarantine_candidates",
            "quarantine_rows",
            "accepted_rows",
        ),
        notes="Strict mode is enabled by default, but explicit CLI overrides can disable it.",
    ),
}


def get_builtin_profile(profile_name: str) -> CleaningProfile:
    """
    Return one built-in cleaning profile by name.

    Args:
        profile_name:
            Built-in profile name.

    Raises:
        ValueError:
            If the profile does not exist.
    """
    try:
        return BUILTIN_CLEANING_PROFILES[profile_name]
    except KeyError as error:
        available = ", ".join(sorted(BUILTIN_CLEANING_PROFILES))
        raise ValueError(
            f"Unknown cleaning profile '{profile_name}'. Available profiles: {available}."
        ) from error


def list_builtin_profile_names() -> list[str]:
    """
    Return sorted built-in profile names.
    """
    return sorted(BUILTIN_CLEANING_PROFILES)
