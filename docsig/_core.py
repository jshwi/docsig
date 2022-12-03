"""
docsig._core
============
"""
from __future__ import annotations

from pathlib import Path as _Path

from ._display import Display as _Display
from ._display import Failures as _Failures
from ._display import FuncStr as _FuncStr
from ._function import KEY as _KEY
from ._function import Function as _Function
from ._function import Param as _Param
from ._module import Modules as _Modules
from ._module import Parent as _Parent
from ._report import Report as _Report


def _compare_args(sig: _Param, doc: _Param) -> bool:
    args = doc, sig
    return all(i.kind == _KEY for i in args) or (
        sig.name == doc.name and all(i.name is not None for i in args)
    )


def _construct_func(func: _Function, no_ansi: bool = False) -> _FuncStr:
    func_str = _FuncStr(func, no_ansi)
    for index in range(len(func)):
        arg = func.signature.args.get(index)
        doc = func.docstring.args.get(index)
        func_str.add_param(arg, doc, not _compare_args(arg, doc))
        if index + 1 != len(func):
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


def _generate_report(func: _Function, targets: list[str], disable: list[str]):
    report = _Report(func, targets, disable)
    report.missing_class_docstring()
    report.missing_func_docstring()
    report.return_not_typed()
    if func.docstring.string is not None:
        report.exists()
        report.missing()
        report.duplicates()
        report.extra_return()
        report.missing_return()
        report.property_return()
        report.class_return()
        for index in range(len(func)):
            arg = func.signature.args.get(index)
            doc = func.docstring.args.get(index)
            report.description_syntax(doc)
            report.indent_syntax(doc)
            if not _compare_args(arg, doc):
                report.order(arg, doc)
                report.incorrect(arg, doc)
                report.misspelled(arg, doc)
                report.not_equal(arg, doc)

    return report


def _run_check(  # pylint: disable=too-many-arguments
    parent: _Parent,
    check_class: bool,
    check_dunders: bool,
    check_overridden: bool,
    check_protected: bool,
    no_ansi: bool,
    targets: list[str],
    disable: list[str],
) -> _Failures:
    failures = _Failures()
    for func in parent:
        if not (func.isoverridden and not check_overridden) and (
            not (func.isprotected and not check_protected)
            and not (func.isinit and not check_class)
            and not (func.isdunder and not check_dunders)
        ):
            report = _generate_report(func, targets, disable)
            func_str = _construct_func(func, no_ansi)
            if report:
                failures.append((func_str, func.lineno, report))

    return failures


def docsig(
    *path: _Path,
    string: str | None = None,
    check_class: bool = False,
    check_dunders: bool = False,
    check_overridden: bool = False,
    check_protected: bool = False,
    no_ansi: bool = False,
    summary: bool = False,
    targets: list[str] | None = None,
    disable: list[str] | None = None,
) -> int:
    """Package's core functionality.

    Populate a sequence of module objects before iterating over their
    top-level functions and classes.

    If any of the functions within the module - and methods within its
    classes - fail, print the resulting function string representation
    and report.

    :param path: Path(s) to check.
    :param string: String to check.
    :param check_class: Check class docstrings.
    :param check_dunders: Check dunder methods
    :param check_overridden: Check overridden methods
    :param check_protected: Check protected functions and classes.
    :param no_ansi: Disable ANSI output.
    :param summary: Print a summarised report.
    :param targets: List of errors to target.
    :param disable: List of errors to disable.
    :return: Exit status for whether test failed or not.
    """
    modules = _Modules(*path, string=string)
    display = _Display(no_ansi)
    for module in modules:
        for top_level in module:
            if not top_level.isprotected or check_protected:
                failures = _run_check(
                    top_level,
                    check_class,
                    check_dunders,
                    check_overridden,
                    check_protected,
                    no_ansi,
                    targets or [],
                    disable or [],
                )
                if failures:
                    display[top_level.path].append(failures)

    if summary:
        display.summarise()
    else:
        display.report()

    return int(bool(display))
