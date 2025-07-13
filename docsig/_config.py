"""
docsig._config
==============
"""

from __future__ import annotations as _

import argparse as _a
import os as _os
import re as _re
import sys as _sys
import typing as _t
import warnings as _warnings
from pathlib import Path as _Path

import tomli as _tomli

from ._version import __version__

PYPROJECT_TOML = "pyproject.toml"


# split str by comma, but allow for escaping
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
    """Get config dict object from package's tool section in toml file.

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


class _ArgumentParser(_a.ArgumentParser):
    def parse_known_args(  # type: ignore
        self,
        args: _t.Sequence[str] | None = None,
        namespace: _a.Namespace | None = None,
    ) -> tuple[_a.Namespace | None, list[str]]:
        namespace, args = super().parse_known_args(args, namespace)
        config = get_config(_Path(self.prog).stem)
        namespace.__dict__ = merge_configs(namespace.__dict__, config)
        return namespace, args


def _warn_on_deprecated_short_flags():
    deprecated_short_flags = {
        "-c": "--check-class",
        "-C": "--check-class-constructor",
        "-D": "--check-dunders",
        "-m": "--check-protected-class-methods",
        "-N": "--check-nested",
        "-o": "--check-overridden",
        "-p": "--check-protected",
        "-P": "--check-property-returns",
        "-U": "--enforce-capitalization",
        "-i": "--ignore-no-params",
        "-a": "--ignore-args",
        "-k": "--ignore-kwargs",
        "-T": "--ignore-typechecker",
    }
    raw_args = _sys.argv[1:]
    expanded_flags = []
    for arg in raw_args:
        if arg.startswith("--") or not arg.startswith("-") or arg == "-":
            expanded_flags.append(arg)
        elif len(arg) > 2:
            expanded_flags.extend([f"-{ch}" for ch in arg[1:]])
        else:
            expanded_flags.append(arg)

    used_flags = set(expanded_flags)
    for short, long in deprecated_short_flags.items():
        if short in used_flags:
            _warnings.warn(
                f"short option '{short}' is deprecated, use '{long}' instead",
                stacklevel=2,
            )


def parse_args(args: _t.Sequence[str] | None = None) -> _a.Namespace:
    """Parse commandline arguments.

    :param args: Args for manual parsing.
    :return: Parsed arguments.
    """
    _warn_on_deprecated_short_flags()
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
        help="list all available checks and exit",
    )
    parser.add_argument(
        "-n",
        "--no-ansi",
        action="store_true",
        help="disable ansi color output",
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
        help=_a.SUPPRESS,
        dest="check_class",
    )
    group.add_argument(
        "--check-class",
        action="store_true",
        help="check class docstrings",
        dest="check_class",
    )
    group.add_argument(
        "-C",
        action="store_true",
        help=_a.SUPPRESS,
        dest="check_class_constructor",
    )
    group.add_argument(
        "--check-class-constructor",
        action="store_true",
        help="check __init__ methods (mutually exclusive with --check-class)",
        dest="check_class_constructor",
    )
    parser.add_argument(
        "-D",
        action="store_true",
        help=_a.SUPPRESS,
        dest="check_dunders",
    )
    parser.add_argument(
        "--check-dunders",
        action="store_true",
        help="check dunder methods",
        dest="check_dunders",
    )
    parser.add_argument(
        "-N",
        action="store_true",
        help=_a.SUPPRESS,
        dest="check_nested",
    )
    parser.add_argument(
        "--check-nested",
        action="store_true",
        help="check nested functions and classes",
        dest="check_nested",
    )
    parser.add_argument(
        "-o",
        action="store_true",
        help=_a.SUPPRESS,
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
        help=_a.SUPPRESS,
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
        help=_a.SUPPRESS,
        dest="check_protected",
    )
    parser.add_argument(
        "--check-protected",
        action="store_true",
        help="check protected functions and classes",
        dest="check_protected",
    )
    parser.add_argument(
        "-m",
        action="store_true",
        help=_a.SUPPRESS,
        dest="check_protected_class_methods",
    )
    parser.add_argument(
        "--check-protected-class-methods",
        action="store_true",
        help="check public methods belonging to protected classes",
        dest="check_protected_class_methods",
    )
    parser.add_argument(
        "-U",
        action="store_true",
        help=_a.SUPPRESS,
        dest="enforce_capitalization",
    )
    parser.add_argument(
        "--enforce-capitalization",
        action="store_true",
        help="ensure param descriptions are capitalized",
        dest="enforce_capitalization",
    )
    parser.add_argument(
        "-a",
        action="store_true",
        help=_a.SUPPRESS,
        dest="ignore_args",
    )
    parser.add_argument(
        "--ignore-args",
        action="store_true",
        help="ignore args prefixed with an asterisk",
        dest="ignore_args",
    )
    parser.add_argument(
        "-k",
        action="store_true",
        help=_a.SUPPRESS,
        dest="ignore_kwargs",
    )
    parser.add_argument(
        "--ignore-kwargs",
        action="store_true",
        help="ignore kwargs prefixed with two asterisks",
        dest="ignore_kwargs",
    )
    parser.add_argument(
        "-i",
        action="store_true",
        help=_a.SUPPRESS,
        dest="ignore_no_params",
    )
    parser.add_argument(
        "--ignore-no-params",
        action="store_true",
        help="ignore docstrings where parameters are not documented",
        dest="ignore_no_params",
    )
    parser.add_argument(
        "-T",
        action="store_true",
        help=_a.SUPPRESS,
        dest="ignore_typechecker",
    )
    parser.add_argument(
        "--ignore-typechecker",
        action="store_true",
        help="ignore checking return values",
        dest="ignore_typechecker",
    )
    parser.add_argument(
        "-d",
        "--disable",
        metavar="LIST",
        action="store",
        type=_split_comma,
        default=[],
        help="comma-separated list of rule codes to disable",
    )
    parser.add_argument(
        "-t",
        "--target",
        metavar="LIST",
        action="store",
        type=_split_comma,
        default=[],
        help="comma-separated list of rule codes to target",
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
