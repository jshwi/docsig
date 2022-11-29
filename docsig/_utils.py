"""
docsig._utils
=============
"""
from __future__ import annotations

from difflib import SequenceMatcher as _SequenceMatcher


def isprotected(name: str | None) -> bool:
    """Confirm whether attribute is protected or not.

    :param name: Name to check.
    :return: Boolean value for whether attribute is protected or not.
    """
    return str(name).startswith("_")


def almost_equal(str1: str, str2: str, mini: float, maxi: float) -> bool:
    """Show result for more than the minimum but less than the maximum.

    :param str1: String one to compare with string two.
    :param str2: String two to compare with string one.
    :param mini: Minimum difference allowed between two strings.
    :param maxi: Maximum difference allowed to be considered almost
        equal.
    :return: Boolean result for whether both strings are almost equal.
    """
    return mini < _SequenceMatcher(a=str1, b=str2).ratio() < maxi
