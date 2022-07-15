"""
docsig._config
==============
"""
import re as _re
import sys as _sys
import typing as _t
from argparse import ArgumentParser as _ArgumentParser
from argparse import HelpFormatter as _HelpFormatter
from pathlib import Path as _Path

import tomli as _tomli

from ._utils import color as _color
from ._utils import find_pyproject_toml as _find_pyproject_toml
from ._version import __version__

NAME = __name__.split(".", maxsplit=1)[0]

ConfigType = _t.Dict[str, _t.Any]


# split str by comma, but allow for escaping
def _split_comma(value: str) -> _t.List[str]:
    return [i.replace("\\,", ",") for i in _re.split(r"(?<!\\),", value)]


def get_config() -> ConfigType:
    """Get config dict object from package's tool section in toml file.

    :return: Dict object; containing config if there is one, else return
        empty.
    """
    pyproject_file = _find_pyproject_toml()
    if pyproject_file is None:
        return {}

    return (
        _tomli.loads(pyproject_file.read_text()).get("tool", {}).get(NAME, {})
    )


class Parser(_ArgumentParser):
    """Parse commandline arguments.

    :param kwargs: Default args from parsed config.
    """

    def __init__(self, kwargs: ConfigType) -> None:
        super().__init__(
            prog=_color.cyan.get(NAME),
            formatter_class=lambda prog: _HelpFormatter(
                prog, max_help_position=45
            ),
            description="Check signature params for proper documentation",
        )
        self._kwargs = kwargs
        self._add_arguments()
        self._version_request()
        self.args = self.parse_args()

    def _add_arguments(self) -> None:
        self.add_argument(
            "path",
            nargs="*",
            action="store",
            type=_Path,
            default=[_Path(".")],
            help="directories or files to check (default: .)",
        )
        self.add_argument(
            "-v",
            "--version",
            action="store_true",
            help="show version and exit",
        )
        self.add_argument(
            "-c",
            "--check-class",
            action="store_true",
            default=self._kwargs.get("check-class", False),
            help="check class docstrings",
        )
        self.add_argument(
            "-D",
            "--check-dunders",
            action="store_true",
            default=self._kwargs.get("check-dunders", False),
            help="check dunder methods",
        )
        self.add_argument(
            "-o",
            "--check-overridden",
            action="store_true",
            default=self._kwargs.get("check-overridden", False),
            help="check overridden methods",
        )
        self.add_argument(
            "-p",
            "--check-protected",
            action="store_true",
            default=self._kwargs.get("check-protected", False),
            help="check protected functions and classes",
        )
        self.add_argument(
            "-n",
            "--no-ansi",
            action="store_true",
            default=self._kwargs.get("no-ansi", False),
            help="disable ansi output",
        )
        self.add_argument(
            "-S",
            "--summary",
            action="store_true",
            default=self._kwargs.get("summary", False),
            help="print a summarised report",
        )
        self.add_argument(
            "-s",
            "--string",
            action="store",
            metavar="STR",
            help="string to parse instead of files",
        )
        self.add_argument(
            "-d",
            "--disable",
            action="store",
            metavar="LIST",
            type=_split_comma,
            default=self._kwargs.get("disable", []),
            help="comma separated list of rules to disable",
        )
        self.add_argument(
            "-t",
            "--target",
            action="store",
            metavar="LIST",
            type=_split_comma,
            default=self._kwargs.get("target", []),
            help="comma separated list of rules to target",
        )

    @staticmethod
    def _version_request() -> None:
        if len(_sys.argv) > 1 and _sys.argv[1] in ("-v", "--version"):
            print(__version__)
            _sys.exit(0)
