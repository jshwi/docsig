"""
docsig._config
==============
"""

from __future__ import annotations

import os as _os
import re as _re
import typing as _t
from argparse import SUPPRESS as _SUPPRESS
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace
from copy import deepcopy
from pathlib import Path as _Path

import tomli as _tomli

from ._version import __version__


# split str by comma, but allow for escaping
def _split_comma(value: str) -> list[str]:
    return [i.replace("\\,", ",") for i in _re.split(r"(?<!\\),", value)]


# attempt to locate a pyproject.toml file if one exists in parents
def _find_pyproject_toml(path: _Path | None = None) -> _Path | None:
    if not path:
        path = _Path.cwd()

    pyproject_toml = path / "pyproject.toml"
    if pyproject_toml.is_file():
        return pyproject_toml

    if str(path) == _os.path.abspath(_os.sep):
        return None

    return _find_pyproject_toml(path.parent)


# Get config dict object from package's tool section in toml file.
def _get_config(prog: str) -> dict[str, _t.Any]:
    pyproject_file = _find_pyproject_toml()
    if pyproject_file is None:
        return {}

    return (
        _tomli.loads(pyproject_file.read_text()).get("tool", {}).get(prog, {})
    )


class Parser(_ArgumentParser):
    """Parse commandline arguments."""

    def __init__(self) -> None:
        """Argument parser for docsig."""
        super().__init__(
            description="Check signature params for proper documentation",
        )
        self._config = {
            k.replace("-", "_"): v for k, v in _get_config(self.prog).items()
        }
        self._add_arguments()
        self.args = self.parse_args()

    def parse_known_args(  # type: ignore
        self,
        args: _t.Sequence[str] | None = None,
        namespace: _Namespace | None = None,
    ) -> tuple[_Namespace | None, list[str]]:
        namespace, args = super().parse_known_args(args, namespace)
        namedict = namespace.__dict__
        for key, value in self._config.items():
            if key in namedict and namedict[key] in (None, False):
                namedict[key] = value

        for key in namedict:
            if key in self._config:
                if (
                    self._config[key] is not namedict[key]
                    and isinstance(self._config[key], list)
                    and isinstance(namedict[key], list)
                ):
                    self._config[key].extend(deepcopy(namedict[key]))
            else:
                self._config[key] = deepcopy(namedict[key])

        namespace.__dict__ = self._config
        return namespace, args

    def _add_arguments(self) -> None:
        self.add_argument(
            "-V", "--version", action="version", version=__version__
        )
        self.add_argument(
            "path",
            nargs="*",
            action="store",
            type=_Path,
            help="directories or files to check",
        )
        self.add_argument(
            "-l",
            "--list-checks",
            action="store_true",
            help="display a list of all checks and their messages",
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
            "-N",
            "--check-nested",
            action="store_true",
            help="check nested functions and classes",
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
            "-T",
            "--ignore-typechecker",
            action="store_true",
            help="ignore checking return values",
        )
        self.add_argument(
            "-I",
            "--include-ignored",
            action="store_true",
            help="check files even if they match a gitignore pattern",
        )
        self.add_argument(
            "-n",
            "--no-ansi",
            action="store_true",
            help="disable ansi output",
        )
        self.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="increase output verbosity",
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
            metavar="LIST",
            type=_split_comma,
            default=[],
            help="comma separated list of rules to disable",
        )
        self.add_argument(
            "-t",
            "--target",
            metavar="LIST",
            type=_split_comma,
            default=[],
            help="comma separated list of rules to target",
        )
        self.add_argument(
            "-e",
            "--exclude",
            metavar="PATTERN",
            help="regular expression of files or dirs to exclude from checks",
        )
        self.add_argument(
            "-E",
            "--excludes",
            nargs="+",
            metavar="PATH",
            help="path glob patterns to exclude from checks",
        )

        # deprecated
        self.add_argument(
            "-S",
            "--summary",
            action="store_true",
            help=_SUPPRESS,
        )
