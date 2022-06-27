"""
docsig._core
============
"""
from __future__ import annotations

import typing as _t
from itertools import zip_longest as _zip_longest
from pathlib import Path as _Path

from ._function import Function as _Function
from ._module import Module as _Module
from ._module import Parent as _Parent
from ._report import Report as _Report
from ._repr import FuncStr as _FuncStr
from ._utils import color as _color
from ._utils import get_index as _get_index

FailedDocData = _t.Dict[str, _t.List[_t.Tuple[_FuncStr, _Report]]]


def get_members(paths: _t.List[_Path]) -> _t.Tuple[_Module, ...]:
    """Get a tuple of module names paired with function information.

    :param paths: Paths to parse for function information.
    :return: A tuple of module level function values.
    """
    return tuple(_Module(p) for p in paths)


def get_files(root: _Path, paths: _t.List[_Path]) -> None:
    """Get files belonging to the provided package.

    :param root: The path where to check for files.
    :param paths: List to populate.
    """
    if root.is_file() and str(root.name).endswith(".py"):
        paths.append(root)

    if root.is_dir():
        for path in root.iterdir():
            get_files(path, paths)


def _compare_args(arg: str | None, doc: str | None, kind: str) -> bool:
    if kind in ("key", "keyword") and arg is not None:
        return arg[:2] == "**"

    if isinstance(arg, str):
        arg = arg.replace("*", "")

    return arg == doc and arg is not None and doc is not None


def construct_func(func: _Function, report: _Report) -> _FuncStr:
    """Construct a string representation of function and docstring info.

    Return None if the test passed.

    :param func: Function object.
    :param report: Report object for final summary of results.
    :return: String if test fails else None.
    """
    func_str = _FuncStr(func.name)
    for count, _ in enumerate(
        _zip_longest(func.signature.args, func.docstring.args)
    ):
        longest = max([len(func.signature.args), len(func.docstring.args)])
        arg = _get_index(count, func.signature.args)
        doc_info = _get_index(count, func.docstring.args)
        if doc_info is not None:
            kind, doc = doc_info
        else:
            kind, doc = "param", None
        if _compare_args(arg, doc, kind):
            func_str.add_param(arg, doc, kind)
        else:
            func_str.add_param(arg, doc, kind, failed=True)
            report.order(arg, doc)
            report.incorrect(arg, doc)

        if count + 1 != longest:
            func_str.add_comma()

    func_str.set_mark()
    if func.docstring.returns and func.signature.returns:
        func_str.add_return()
    elif (
        func.docstring.returns
        and not func.signature.returns
        or func.signature.returns
        and not func.docstring.returns
    ):
        func_str.add_return(failed=True)

    func_str.close_sig(func.signature.returns)
    func_str.close_docstring()
    func_str.render()
    return func_str


def print_failures(failures: FailedDocData) -> None:
    """Print failed tests.

    :param failures: Tuple of module names containing a list of failed
        functions.
    """
    for module, funcs in failures.items():
        for func, summary in funcs:
            _color.magenta.print(module)
            print(len(module) * "-")
            print(f"{func}\n{summary.get_report()}")


def populate(name: str, parent: _Parent, failures: FailedDocData) -> None:
    """Populate function issues.

    :param name: Name of function parent.
    :param parent: Functions ``Parent`` object.
    :param failures: Dictionary of failure objects.
    """
    module_data = []
    for func in parent.funcs:
        report = _Report(func)
        report.exists()
        report.missing()
        report.duplicates()
        report.extra_return()
        report.missing_return()
        func_result = construct_func(func, report)
        if report:
            module_data.append((func_result, report))

    if module_data:
        failures[name] = module_data
