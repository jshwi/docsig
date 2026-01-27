"""
docsig._config
==============
"""

from __future__ import annotations as _

import argparse as _argparse
import os as _os
import re as _re
import typing as _t
from dataclasses import dataclass as _dataclass
from dataclasses import field as _field
from pathlib import Path as _Path

import tomli as _tomli

from ._version import __version__
from .messages import Messages

PYPROJECT_TOML = "pyproject.toml"


# split str by comma but allow for escaping
def _split_comma(value: str) -> list[str]:
    return [i.replace("\\,", ",") for i in _re.split(r"(?<!\\),", value)]


# attempt to locate a pyproject.toml file if one exists in parents
def _find_pyproject_toml(path: _Path | None = None) -> _Path | None:
    if not path:
        path = _Path.cwd()

    pyproject_toml = path / PYPROJECT_TOML
    if pyproject_toml.is_file():
        return pyproject_toml

    if str(path) == _os.path.abspath(_os.sep):
        return None

    return _find_pyproject_toml(path.parent)


def get_config(prog: str) -> dict[str, _t.Any]:
    """Get the config object from the package's tool section the config.

    :param prog: Program name.
    :return: Config dict.
    """
    pyproject_file = _find_pyproject_toml()
    if pyproject_file is None:
        return {}

    return {
        k.replace("-", "_"): v
        for k, v in _tomli.loads(pyproject_file.read_text())
        .get("tool", {})
        .get(prog, {})
        .items()
    }


def merge_configs(
    obj1: dict[str, _t.Any],
    obj2: dict[str, _t.Any],
) -> dict[str, _t.Any]:
    """Merge two config dicts.

    :param obj1: Config dict one.
    :param obj2: Config dict two.
    :return: Config dict.
    """
    for key, n_val in obj1.items():
        c_val = obj2.get(key)
        if isinstance(c_val, list) and isinstance(n_val, list):
            obj1[key].extend(c_val)
        elif c_val:
            obj1[key] = c_val

    return obj1


class _ArgumentParser(_argparse.ArgumentParser):
    def parse_known_args(  # type: ignore
        self,
        args: _t.Sequence[str] | None = None,
        namespace: _argparse.Namespace | None = None,
    ) -> tuple[_argparse.Namespace | None, list[str]]:
        namespace, args = super().parse_known_args(args, namespace)
        config = get_config(_Path(self.prog).stem)
        namespace.__dict__ = merge_configs(namespace.__dict__, config)
        return namespace, args


def parse_args(args: _t.Sequence[str] | None = None) -> _argparse.Namespace:
    """Parse commandline arguments.

    :param args: Args for manual parsing.
    :return: Parsed arguments.
    """
    parser = _ArgumentParser(
        description="Check signature params for proper documentation",
    )
    parser.add_argument(
        "path",
        nargs="*",
        action="store",
        type=_Path,
        help="directories or files to check",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=__version__,
    )
    parser.add_argument(
        "-l",
        "--list-checks",
        action="store_true",
        help="display a list of all checks and their messages",
    )
    parser.add_argument(
        "-n",
        "--no-ansi",
        action="store_true",
        help="disable ansi output",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="increase output verbosity",
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-c",
        action="store_true",
        help=_argparse.SUPPRESS,
        dest="check_class",
    )
    group.add_argument(
        "--check-class",
        action="store_true",
        help="check class docstrings",
        dest="check_class",
    )
    group.add_argument(
        "--check-class-constructor",
        action="store_true",
        help="check __init__ methods",
    )
    parser.add_argument(
        "-D",
        action="store_true",
        help=_argparse.SUPPRESS,
        dest="check_dunders",
    )
    parser.add_argument(
        "--check-dunders",
        action="store_true",
        help="check dunder methods",
        dest="check_dunders",
    )
    parser.add_argument(
        "--check-nested",
        action="store_true",
        help="check nested functions and classes",
    )
    parser.add_argument(
        "-o",
        action="store_true",
        help=_argparse.SUPPRESS,
        dest="check_overridden",
    )
    parser.add_argument(
        "--check-overridden",
        action="store_true",
        help="check overridden methods",
        dest="check_overridden",
    )
    parser.add_argument(
        "-P",
        action="store_true",
        help=_argparse.SUPPRESS,
        dest="check_property_returns",
    )
    parser.add_argument(
        "--check-property-returns",
        action="store_true",
        help="check property return values",
        dest="check_property_returns",
    )
    parser.add_argument(
        "-p",
        action="store_true",
        help=_argparse.SUPPRESS,
        dest="check_protected",
    )
    parser.add_argument(
        "--check-protected",
        action="store_true",
        help="check protected functions and classes",
        dest="check_protected",
    )
    parser.add_argument(
        "--check-protected-class-methods",
        action="store_true",
        help="check public methods belonging to protected classes",
    )
    parser.add_argument(
        "--ignore-args",
        action="store_true",
        help="ignore args prefixed with an asterisk",
    )
    parser.add_argument(
        "--ignore-kwargs",
        action="store_true",
        help="ignore kwargs prefixed with two asterisks",
    )
    parser.add_argument(
        "-i",
        action="store_true",
        help=_argparse.SUPPRESS,
        dest="ignore_no_params",
    )
    parser.add_argument(
        "--ignore-no-params",
        action="store_true",
        help="ignore docstrings where parameters are not documented",
        dest="ignore_no_params",
    )
    parser.add_argument(
        "--ignore-typechecker",
        action="store_true",
        help="ignore checking return values",
    )
    parser.add_argument(
        "-d",
        "--disable",
        metavar="LIST",
        action="store",
        type=_split_comma,
        default=[],
        help="comma separated list of rules to disable",
    )
    parser.add_argument(
        "-t",
        "--target",
        metavar="LIST",
        action="store",
        type=_split_comma,
        default=[],
        help="comma separated list of rules to target",
    )
    parser.add_argument(
        "-e",
        "--exclude",
        metavar="PATTERN",
        help="regular expression of files or dirs to exclude from checks",
    )
    parser.add_argument(
        "-E",
        "--excludes",
        nargs="+",
        metavar="PATH",
        help="path glob patterns to exclude from checks",
    )
    parser.add_argument(
        "-I",
        "--include-ignored",
        action="store_true",
        help="check files even if they match a gitignore pattern",
    )
    parser.add_argument(
        "-s",
        "--string",
        action="store",
        metavar="STR",
        help="string to parse instead of files",
    )
    return parser.parse_args(args)


# pylint: disable=too-many-instance-attributes,too-few-public-methods
@_dataclass
class Check:
    """Configuration for what to check.

    :param class: Check class docstrings.
    :param class_constructor: Check ``__init__`` methods. Note
        that this is mutually incompatible with check_class.
    :param dunders: Check dunder methods.
    :param nested: Check nested functions and classes.
    :param overridden: Check overridden methods.
    :param protected: Check protected functions and classes.
    :param property_returns: Run return checks on properties.
    :param protected_class_methods: Check public methods belonging
        to protected classes.
    """

    class_: bool = False
    class_constructor: bool = False
    dunders: bool = False
    nested: bool = False
    overridden: bool = False
    protected: bool = False
    property_returns: bool = False
    protected_class_methods: bool = False


@_dataclass
class Ignore:
    """Configuration for what to ignore.

    :param no_params: Ignore docstrings where parameters are not
        documented.
    :param args: Ignore args prefixed with an asterisk.
    :param kwargs: Ignore kwargs prefixed with two asterisks.
    :param typechecker: Ignore checking return values.
    """

    no_params: bool = False
    args: bool = False
    kwargs: bool = False
    typechecker: bool = False


@_dataclass(frozen=True)
class Config:
    """Internal run configuration for docsig.

    Groups check/ignore settings and run options, so the core runner
    takes a single config object instead of many parameters.
    """

    check: Check = _field(default_factory=Check)
    ignore: Ignore = _field(default_factory=Ignore)
    target: Messages = _field(default_factory=Messages)
    disable: Messages = _field(default_factory=Messages)
    exclude: list[str] = _field(default_factory=list)
    excludes: list[str] | None = None
    list_checks: bool = False
    include_ignored: bool = False
    no_ansi: bool = False
    verbose: bool = False
