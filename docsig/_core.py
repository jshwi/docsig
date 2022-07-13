"""
docsig._core
============
"""
from __future__ import annotations

import typing as _t
from itertools import zip_longest as _zip_longest
from pathlib import Path as _Path

from ._function import Function as _Function
from ._module import Modules as _Modules
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


def _construct_func(
    func: _Function, parent: _Parent, report: _Report
) -> _FuncStr:
    func_str = _FuncStr(func.name, parent.name, func.isinit)
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


def _print_failures(name: str, funcs: FailedDocList) -> None:
    for func_str, lineno, report in funcs:
        header = f"{name}{lineno}"
        _color.magenta.print(header)
        print(len(header) * "-")
        print(func_str)
        print(report.get_report())


def _run_check(
    parent: _Parent,
    check_class: bool = False,
    targets: _t.List[str] | None = None,
    disable: _t.List[str] | None = None,
) -> FailedDocList:
    failures = []
    for func in parent:
        if func.name == "__init__" and not check_class:
            continue

        report = _Report(func, targets, disable)
        report.exists()
        report.missing()
        report.duplicates()
        report.extra_return()
        report.return_not_typed()
        report.missing_return()
        report.property_return()
        report.class_return()
        func_str = _construct_func(func, parent, report)
        if report:
            failures.append((func_str, func.lineno, report))

    return failures


def docsig(
    *path: _Path,
    string: str | None = None,
    check_class: bool = False,
    targets: _t.List[str] | None = None,
    disable: _t.List[str] | None = None,
) -> int:
    """Package's core functionality.

    Populate a sequence of module objects before iterating over their
    top-level functions and classes.

    If any of the functions within the module - and methods within its
    classes - fail, print the resulting function string representation
    and report.

    :param path: Path(s) to check.
    :param string: String to check.
    :param check_class: check class docstrings.
    :param targets: List of errors to target.
    :param disable: List of errors to disable.
    :return: Exit status for whether test failed or not.
    """
    failed = False
    modules = _Modules(*path, string=string)
    for module in modules:
        for top_level in module:
            failures = _run_check(top_level, check_class, targets, disable)
            if failures:
                failed = True
                _print_failures(top_level.path, failures)

    return int(failed)
