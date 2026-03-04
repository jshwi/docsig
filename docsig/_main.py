"""
docsig._main
============

Contains package entry point.
"""

from __future__ import annotations as _

from ._config import parse_args as _parse_args
from ._core import docsig as _docsig
from ._hooks import excepthook as _excepthook


def main() -> str | int:
    """Main function for package.

    Collect config and arguments for the commandline.

    :return: Exit status for whether the test failed or not.
    """
    a = _parse_args()
    _excepthook(a.no_ansi)
    kwargs = vars(a)
    path = kwargs.pop("path")
    return _docsig(*path, **kwargs)
