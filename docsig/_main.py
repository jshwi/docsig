"""
docsig._main
============

Contains package entry point.
"""
import typing as _t
from pathlib import Path as _Path

from ._cli import Parser as _Parser
from ._core import FailedDocData as _FailedDocData
from ._core import get_files as _get_files
from ._core import get_members as _get_members
from ._core import populate as _populate
from ._core import print_failures as _print_failures
from ._function import Function as _Function
from ._report import warn as _warn


def main() -> int:
    """Main function for package.

    :return: Non-zero exit status if check fails else zero.
    """
    paths: _t.List[_Path] = []
    failures: _FailedDocData = {}
    missing: _t.List[_t.Tuple[str, _Function]] = []
    parser = _Parser()
    for path in parser.args.path:
        _get_files(path, paths)

    members = _get_members(paths)
    for module in members:
        _populate(module.name, module, failures, missing)
        for klass in module.classes:
            name = f"{module.name}::{klass.name}"
            _populate(name, klass, failures, missing)

    _print_failures(failures)
    _warn(missing)

    # pylint: disable=use-implicit-booleaness-not-comparison
    return int(failures != {})
