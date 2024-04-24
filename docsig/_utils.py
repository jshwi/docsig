"""
docsig._utils
=============
"""

from __future__ import annotations as _

import sys as _sys
import typing as _t
from difflib import SequenceMatcher as _SequenceMatcher

import click as _click

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


def vprint(msg: str, verbose: bool = False) -> None:
    """Print messages only if verbose is true.

    :param msg: Message to print.
    :param verbose: Whether verbose mode is enabled.
    """
    if verbose:
        _click.echo(msg)


def pretty_print_error(
    exception_type: _t.Type[BaseException], msg: str, no_ansi: bool
) -> None:
    """Print user-friendly exception.

    :param exception_type: Type of the exception.
    :param msg: The exception message.
    :param no_ansi: Whether to in ANSI escape codes.
    """
    _click.echo(
        f"{_click.style(exception_type.__name__, fg='red', bold=True)}: {msg}",
        file=_sys.stderr,
        color=not no_ansi and _sys.stderr.isatty(),
    )


def print_checks() -> None:
    """Print all available checks."""
    for msg in _E.values():
        _click.echo(msg.fstring(_TEMPLATE))
