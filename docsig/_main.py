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


def main() -> int:
    """Main function for package.

    :return: Non-zero exit status if check fails else zero.
    """
    paths: _t.List[_Path] = []
    failures: _FailedDocData = {}
    parser = _Parser()
    for path in parser.args.path:
        _get_files(path, paths)

    members = _get_members(paths)
    for module in members:
        _populate(module.name, module, failures)
        for klass in module.classes:
            name = f"{module.name}::{klass.name}"
            _populate(name, klass, failures)

    _print_failures(failures)

    # pylint: disable=use-implicit-booleaness-not-comparison
    return int(failures != {})
