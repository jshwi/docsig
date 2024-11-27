"""
docsig._config
==============
"""

from __future__ import annotations as _

import argparse as _a
import os as _os
import re as _re
import typing as _t
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
    obj1: dict[str, _t.Any], obj2: dict[str, _t.Any]
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

    def add_list_argument(self, *args: str, **kwargs: _t.Any) -> None:
        """Parse a comma separated list of strings into a list.

        :param args: Long and/or short form argument(s).
        :param kwargs: Kwargs to pass to ``add_argument``.
        """
        kwargs.update(
            {
                "action": "store",
                "type": _split_comma,
                "default": kwargs.get("default", []),
            }
        )
        self.add_argument(*args, **kwargs)


def parse_args(args: _t.Sequence[str] | None = None) -> _a.Namespace:
    """Parse commandline arguments.

    :param args: Args for manual parsing.
    :return: Parsed arguments.
    """
    parser = _ArgumentParser(
        description="Check signature params for proper documentation"
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=__version__,
    )
    parser.add_argument(
        "path",
        nargs="*",
        action="store",
        type=_Path,
        help="directories or files to check",
    )
    parser.add_argument(
        "-l",
        "--list-checks",
        action="store_true",
        help="display a list of all checks and their messages",
    )
    group = parser.add_mutually_exclusive_group(required=False)
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
    parser.add_argument(
        "-D",
        "--check-dunders",
        action="store_true",
        help="check dunder methods",
    )
    parser.add_argument(
        "-m",
        "--check-protected-class-methods",
        action="store_true",
        help="check public methods belonging to protected classes",
    )
    parser.add_argument(
        "-N",
        "--check-nested",
        action="store_true",
        help="check nested functions and classes",
    )
    parser.add_argument(
        "-o",
        "--check-overridden",
        action="store_true",
        help="check overridden methods",
    )
    parser.add_argument(
        "-p",
        "--check-protected",
        action="store_true",
        help="check protected functions and classes",
    )
    parser.add_argument(
        "-P",
        "--check-property-returns",
        action="store_true",
        help="check property return values",
    )
    parser.add_argument(
        "-i",
        "--ignore-no-params",
        action="store_true",
        help="ignore docstrings where parameters are not documented",
    )
    parser.add_argument(
        "-a",
        "--ignore-args",
        action="store_true",
        help="ignore args prefixed with an asterisk",
    )
    parser.add_argument(
        "-k",
        "--ignore-kwargs",
        action="store_true",
        help="ignore kwargs prefixed with two asterisks",
    )
    parser.add_argument(
        "-T",
        "--ignore-typechecker",
        action="store_true",
        help="ignore checking return values",
    )
    parser.add_argument(
        "-I",
        "--include-ignored",
        action="store_true",
        help="check files even if they match a gitignore pattern",
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
    parser.add_argument(
        "-s",
        "--string",
        action="store",
        metavar="STR",
        help="string to parse instead of files",
    )
    parser.add_list_argument(
        "-d",
        "--disable",
        metavar="LIST",
        help="comma separated list of rules to disable",
    )
    parser.add_list_argument(
        "-t",
        "--target",
        metavar="LIST",
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
    return parser.parse_args(args)
