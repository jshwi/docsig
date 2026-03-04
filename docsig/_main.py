"""
docsig._main
============

CLI entry point that parses args and runs docsig.
"""

import os as _os
import sys as _sys
import warnings as _warnings

from ._config import parse_args as _parse_args
from ._core import docsig as _docsig
from ._report import pretty_print_error as _pretty_print_error


def _excepthook(no_ansi: bool = False) -> None:
    """Install a hook that prints user-friendly errors (not default).

    Skipped when DOCSIG_DEBUG is set to "1".

    :param no_ansi: Whether to disable ANSI escape codes in output.
    """
    if _os.environ.get("DOCSIG_DEBUG") != "1":
        _sys.excepthook = lambda x, y, _: _pretty_print_error(
            x,
            str(y),
            no_ansi,
        )


def main() -> str | int:
    """Parse CLI args, install the exception hook, and run docsig.

    :return: Exit code (non-zero if any check failed).
    """
    if _os.getenv("_DOCSIG_FORMAT_JSON"):
        _warnings.simplefilter("ignore", FutureWarning)

    a = _parse_args()
    _excepthook(a.no_ansi)
    kwargs = vars(a)
    path = kwargs.pop("path")
    return _docsig(*path, **kwargs)
