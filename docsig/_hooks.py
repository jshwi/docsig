"""
docsig._hooks
=============
"""

import sys as _sys
from os import environ as _e

import click as _click


def pretty_print_error() -> None:
    """Print user friendly commandline error if debug not enabled."""
    if _e.get("DOCSIG_DEBUG", None) != "1":
        _sys.excepthook = lambda x, y, _: print(
            f"{_click.style(x.__name__, fg='red', bold=True)}: {y}"
        )
