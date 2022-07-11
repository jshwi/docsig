"""
docsig._core
============
"""
from __future__ import annotations

import typing as _t
from itertools import zip_longest as _zip_longest

from ._function import Function as _Function
from ._module import Parent as _Parent
from ._report import Report as _Report
from ._repr import FuncStr as _FuncStr
from ._utils import color as _color
from ._utils import get_index as _get_index

FailedDocList = _t.List[_t.Tuple[_FuncStr, int, _Report]]


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
            report.not_equal(arg, doc)

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

    func_str.close_sig(func.signature.return_value)
    func_str.close_docstring()
    func_str.render()
    return func_str


def print_failures(name: str, funcs: FailedDocList) -> None:
    """Print failed tests.

    :param name: Name of the parent of the failed test.
    :param funcs: List of tuples containing failed doc information.
    """
    for func, lineno, summary in funcs:
        header = f"{name}::{lineno}"
        _color.magenta.print(header)
        print(len(header) * "-")
        print(f"{func}\n{summary.get_report()}")


def populate(
    parent: _Parent, targets: _t.List[str], disable: _t.List[str]
) -> FailedDocList:
    """Populate function issues.

    :param parent: Functions ``Parent`` object.
    :param targets: List of errors to target.
    :param disable: List of errors to disable.
    :return: List of tuples containing failed doc information.
    """
    module_data = []
    for func in parent:
        report = _Report(func, targets, disable)
        report.exists()
        report.missing()
        report.duplicates()
        report.extra_return()
        report.return_not_typed()
        report.missing_return()
        report.property_return()
        func_result = construct_func(func, report)
        if report:
            module_data.append((func_result, func.lineno, report))

    return module_data
