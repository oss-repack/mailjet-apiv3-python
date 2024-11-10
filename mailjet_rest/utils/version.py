"""Versioning utilities for the Mailjet REST API client.

This module defines the current version of the Mailjet client and provides
a helper function, `get_version`, to retrieve the version as a formatted string.

Attributes:
    VERSION (tuple[int, int, int]): A tuple representing the major, minor, and patch
    version of the package.

Functions:
    get_version: Returns the version as a string in the format "major.minor.patch".
"""

from __future__ import annotations


VERSION: tuple[int, int, int] = (1, 3, 5)


def get_version(version: tuple[int, ...] | None = None) -> str:
    """Calculate package version based on a 3 item tuple.

    In addition, verify that the tuple contains 3 items.

    Parameters:
    version (tuple[int, ...], optional): A tuple representing the version of the package.
        If not provided, the function will use the VERSION constant.
        Default is None.

    Returns:
    str: The version as a string in the format "major.minor.patch".

    Raises:
    ValueError: If the provided tuple does not contain exactly 3 items.
    """
    if version is None:
        version = VERSION
    if len(version) != 3:
        msg = "The tuple 'version' must contain 3 items"
        raise ValueError(msg)
    return "{}.{}.{}".format(*(x for x in version))
