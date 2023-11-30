"""
docsig._hooks
=============
"""
import sys as _sys
from os import environ as _e

from ._display import color as _color


def pretty_print_error() -> None:
    """Print user friendly commandline error if debug not enabled."""
    if _e.get("DOCSIG_DEBUG", None) != "1":
        _sys.excepthook = lambda x, y, _: print(
            f"{_color.red.bold.get(x.__name__)}: {y}"
        )
