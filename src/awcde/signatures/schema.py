"""Signature schema version management.

Tracks the current schema version and provides validation utilities
for schema version strings.
"""

from __future__ import annotations

import re

CURRENT_SCHEMA_VERSION = "1.0.0"

_SEMVER_PATTERN = re.compile(
    r"^(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*)?$"
)


def get_schema_version() -> str:
    """Return the current schema version string.

    Returns:
        The current schema version in semver format.
    """
    return CURRENT_SCHEMA_VERSION


def validate_schema_version(version: str) -> bool:
    """Validate that a version string follows semantic versioning format.

    Checks for the pattern MAJOR.MINOR.PATCH with optional pre-release
    suffix (e.g. '1.0.0', '2.1.0-beta.1').

    Args:
        version: The version string to validate.

    Returns:
        True if the version string is valid semver, False otherwise.
    """
    return bool(_SEMVER_PATTERN.match(version))
