"""
docsig._utils
=============
"""

from __future__ import annotations as _

from difflib import SequenceMatcher as _SequenceMatcher

import click as _click


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


def vprint(msg: str, verbose: bool = False) -> None:
    """Print messages only if verbose is true.

    :param msg: Message to print.
    :param verbose: Whether verbose mode is enabled.
    """
    if verbose:
        _click.echo(msg)
