"""
docsig._config
==============
"""
from argparse import HelpFormatter as _HelpFormatter
from pathlib import Path as _Path

from arcon import ArgumentParser as _ArgumentParser

from ._display import color as _color
from ._version import __version__


class Parser(_ArgumentParser):
    """Parse commandline arguments."""

    def __init__(self) -> None:
        super().__init__(
            version=__version__,
            prog=_color.cyan.get(__package__),
            formatter_class=lambda prog: _HelpFormatter(
                prog, max_help_position=45
            ),
            description="Check signature params for proper documentation",
        )
        self._add_arguments()
        self.args = self.parse_args()

    def _add_arguments(self) -> None:
        self.add_argument(
            "path",
            nargs="+",
            action="store",
            type=_Path,
            help="directories or files to check",
        )
        group = self.add_mutually_exclusive_group(required=False)
        group.add_argument(
            "-c",
            "--check-class",
            action="store_true",
            help="check class docstrings",
        )
        group.add_argument(
            "-C",
            "--check-class-constructor",
            action="store_true",
            help="check __init__ methods. Note: mutually incompatible with -c",
        )
        self.add_argument(
            "-D",
            "--check-dunders",
            action="store_true",
            help="check dunder methods",
        )
        self.add_argument(
            "-m",
            "--check-protected-class-methods",
            action="store_true",
            help="check public methods belonging to protected classes",
        )
        self.add_argument(
            "-o",
            "--check-overridden",
            action="store_true",
            help="check overridden methods",
        )
        self.add_argument(
            "-p",
            "--check-protected",
            action="store_true",
            help="check protected functions and classes",
        )
        self.add_argument(
            "-P",
            "--check-property-returns",
            action="store_true",
            help="check property return values",
        )
        self.add_argument(
            "-i",
            "--ignore-no-params",
            action="store_true",
            help="ignore docstrings where parameters are not documented",
        )
        self.add_argument(
            "-a",
            "--ignore-args",
            action="store_true",
            help="ignore args prefixed with an asterisk",
        )
        self.add_argument(
            "-k",
            "--ignore-kwargs",
            action="store_true",
            help="ignore kwargs prefixed with two asterisks",
        )
        self.add_argument(
            "-n",
            "--no-ansi",
            action="store_true",
            help="disable ansi output",
        )
        self.add_argument(
            "-S",
            "--summary",
            action="store_true",
            help="print a summarised report",
        )
        self.add_argument(
            "-s",
            "--string",
            action="store",
            metavar="STR",
            help="string to parse instead of files",
        )
        self.add_list_argument(
            "-d",
            "--disable",
            metavar="LIST",
            help="comma separated list of rules to disable",
        )
        self.add_list_argument(
            "-t",
            "--target",
            metavar="LIST",
            help="comma separated list of rules to target",
        )
