"""
docsig._main
============

Contains package entry point.
"""
import typing as _t
from pathlib import Path as _Path

from ._cli import Parser as _Parser
from ._core import FailedDocData as _FailedDocData
from ._core import construct_func as _construct_func
from ._core import get_files as _get_files
from ._core import get_members as _get_members
from ._core import print_failures as _print_failures
from ._function import Function as _Function
from ._report import Report as _Report
from ._report import warn as _warn


def main() -> int:
    """Main function for package.

    :return: Non-zero exit status if check fails else zero.
    """
    paths: _t.List[_Path] = []
    failures: _FailedDocData = {}
    missing: _t.List[_t.Tuple[str, _Function]] = []
    parser = _Parser()
    _get_files(parser.args.path, paths)
    members = _get_members(paths)
    for module in members:
        module_data = []
        for func in module.funcs:
            if not func.docstring.is_doc:
                missing.append((module.name, func))
            else:
                report = _Report(func)
                report.exists()
                report.missing()
                report.duplicates()
                report.extra_return()
                report.missing_return()
                func_result = _construct_func(func, report)
                if report:
                    module_data.append((func_result, report))

        if module_data:
            failures[module.name] = module_data

    _print_failures(failures)
    _warn(missing)

    # pylint: disable=use-implicit-booleaness-not-comparison
    return int(failures != {})
