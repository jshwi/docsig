"""
docsig._utils
=============

Shared helpers.
"""

from __future__ import annotations as _

import re as _re
import sys as _sys
import typing as _t
from difflib import SequenceMatcher as _SequenceMatcher

from .messages import TEMPLATE as _TEMPLATE
from .messages import E as _E


def almost_equal(str1: str, str2: str, mini: float, maxi: float) -> bool:
    """Return True if the strings are equal or ratio in (mini, maxi).

    Uses SequenceMatcher ratio; exact match always returns True.

    :param str1: First string.
    :param str2: Second string.
    :param mini: Lower bound on ratio (exclusive) when not equal.
    :param maxi: Upper bound on ratio (exclusive) when not equal.
    :return: True when equal or mini < ratio < maxi.
    """
    return (str1 == str2) or mini < _SequenceMatcher(
        a=str1,
        b=str2,
    ).ratio() < maxi


def pretty_print_error(
    exception_type: _t.Type[BaseException],
    msg: str,
    no_ansi: bool,
) -> None:
    """Print exception type and message to stderr (ANSI color if tty).

    :param exception_type: Exception class.
    :param msg: Exception message.
    :param no_ansi: If True, do not use ANSI escape codes.
    """
    exception_type_name = exception_type.__name__
    if not no_ansi and _sys.stdout.isatty():
        exception_type_name = f"\033[1;31m{exception_type_name}\033[0m"

    print(f"{exception_type_name}: {msg}", file=_sys.stderr)


def print_checks() -> None:
    """Print all available docstring-check codes and descriptions.

    Output goes to stdout.
    """
    for msg in _E.values():
        print(msg.fstring(_TEMPLATE))


def has_bad_return(string: str) -> bool:
    """Search for return documented with poor syntax.

    Put this here in case the function increases in complexity.

    Do more than search the docstring for the word return as return
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


def sentence_tokenizer(text: str) -> list[str]:
    """Split text on sentence boundaries, skipping common abbreviations.

    Splits on . ! ? followed by whitespace; treats abbreviations such as
    e.g. and i.e. as non-boundaries.

    :param text: Input string.
    :return: Non-overlapping sentence strings in order.
    """
    abbreviations = {"e.g.", "i.e.", "mr.", "dr.", "vs.", "etc.", "u.s."}
    result = []
    start = 0

    for match in _re.finditer(r"[.!?]\s+", text):
        end = match.end()
        candidate = text[start:end].strip()
        last_word = candidate.lower().split()[-1]
        if last_word in abbreviations:
            continue

        result.append(candidate)
        start = end

    if start < len(text):
        result.append(text[start:].strip())

    return result
