"""
docsig._config
==============
"""

from __future__ import annotations as _

import argparse as _a
import typing as _t
from pathlib import Path as _Path

from ._arcon import ArgumentParser as _ArgumentParser
from ._version import __version__


def parse_args(args: _t.Sequence[str] | None = None) -> _a.Namespace:
    """Parse commandline arguments.

    :param args: Args for manual parsing.
    :return: Parsed arguments.
    """
    parser = _ArgumentParser(
        version=__version__,
        description="Check signature params for proper documentation",
        version_short_form="-V",
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

    # deprecated
    parser.add_argument(
        "-S",
        "--summary",
        action="store_true",
        help=_a.SUPPRESS,
    )

    return parser.parse_args(args)
