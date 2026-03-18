"""
docsig._hooks
=============

Exception hook for user-friendly errors unless DOCSIG_DEBUG is set.
"""

import sys as _sys
from os import environ as _e

from ._utils import pretty_print_error as _pretty_print_error


def excepthook(no_ansi: bool = False) -> None:
    """Install a hook that prints user-friendly errors (not default).

    Skipped when DOCSIG_DEBUG is set to "1".

    :param no_ansi: Whether to disable ANSI escape codes in output.
    """
    if _e.get("DOCSIG_DEBUG") != "1":
        _sys.excepthook = lambda x, y, _: _pretty_print_error(
            x,
            str(y),
            no_ansi,
        )
