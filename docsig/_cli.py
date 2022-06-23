"""
docsig._cli
===========
"""
import sys as _sys
from argparse import ArgumentParser as _ArgumentParser
from pathlib import Path as _Path

from ._utils import color as _color
from ._version import __version__

NAME = __name__.split(".", maxsplit=1)[0]


class Parser(_ArgumentParser):
    """Parse commandline arguments."""

    def __init__(self) -> None:
        super().__init__(
            prog=_color.cyan.get(NAME),
            description="Check docstring matches signature",
        )
        self._add_arguments()
        self._version_request()
        self.args = self.parse_args()

    def _add_arguments(self) -> None:
        self.add_argument(
            "path",
            nargs="*",
            action="store",
            type=_Path,
            help="directories or files to check",
        )
        self.add_argument(
            "-v",
            "--version",
            action="store_true",
            help="show version and exit",
        )

    @staticmethod
    def _version_request() -> None:
        if len(_sys.argv) > 1 and _sys.argv[1] == "--version":
            print(__version__)
            _sys.exit(0)
