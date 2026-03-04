"""
docsig._main
============

CLI entry point that parses args and runs docsig.
"""

from __future__ import annotations as _

from ._config import parse_args as _parse_args
from ._core import docsig as _docsig
from ._hooks import excepthook as _excepthook


def main() -> str | int:
    """Parse CLI args, install the exception hook, and run docsig.

    :return: Exit code (non-zero if any check failed).
    """
    a = _parse_args()
    _excepthook(a.no_ansi)
    kwargs = vars(a)
    path = kwargs.pop("path")
    return _docsig(*path, **kwargs)
