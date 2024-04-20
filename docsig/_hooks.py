"""
docsig._hooks
=============
"""

import sys as _sys
from os import environ as _e

import click as _click


def pretty_print_error(no_ansi: bool = False) -> None:
    """Print user friendly commandline error if debug not enabled.

    :param no_ansi: Disable ANSI output.
    """
    if _e.get("DOCSIG_DEBUG", None) != "1":
        _sys.excepthook = lambda x, y, _: _click.echo(
            f"{_click.style(x.__name__, fg='red', bold=True)}: {y}",
            file=_sys.stderr,
            color=not no_ansi and _sys.stderr.isatty(),
        )
