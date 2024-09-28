"""
docsig._utils
=============
"""

from __future__ import annotations as _

import sys as _sys
import typing as _t
from difflib import SequenceMatcher as _SequenceMatcher

from .messages import TEMPLATE as _TEMPLATE
from .messages import E as _E


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


def pretty_print_error(
    exception_type: _t.Type[BaseException], msg: str, no_ansi: bool
) -> None:
    """Print user-friendly exception.

    :param exception_type: Type of the exception.
    :param msg: The exception message.
    :param no_ansi: Whether to in ANSI escape codes.
    """
    exception_type_name = exception_type.__name__
    if not no_ansi and _sys.stdout.isatty():
        exception_type_name = f"\033[1;31m{exception_type_name}\033[0m"

    print(f"{exception_type_name}: {msg}", file=_sys.stderr)


def print_checks() -> None:
    """Print all available checks."""
    for msg in _E.values():
        print(msg.fstring(_TEMPLATE))


def has_bad_return(string: str) -> bool:
    """Search for return documented with poor syntax.

    Put this here in case the function increases in complexity.

    Do more than just search the docstring for the word return as return
    statements come last, so only search the last line params can also
    come last, so make sure it is not a param declaration.

    :param string: Docstring to check.
    :return: Boolean value indicating if a function has a bad return
        statement.
    """
    lines = string.splitlines()
    return (
        len(lines) > 1 and "return" in lines[-1] and ":param" not in lines[-1]
    )
