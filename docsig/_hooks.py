"""
docsig._hooks
=============
"""

import sys as _sys
from os import environ as _e

from ._utils import pretty_print_error as _pretty_print_error


def excepthook(no_ansi: bool = False) -> None:
    """Print user friendly commandline error if debug not enabled.

    :param no_ansi: Disable ANSI output.
    """
    if _e.get("DOCSIG_DEBUG", None) != "1":
        _sys.excepthook = lambda x, y, _: _pretty_print_error(
            x, str(y), no_ansi
        )
