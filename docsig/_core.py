"""
docsig._core
============
"""
from __future__ import annotations

from pathlib import Path as _Path

from ._display import Display as _Display
from ._display import Failure as _Failure
from ._display import Failures as _Failures
from ._display import FuncStr as _FuncStr
from ._module import Modules as _Modules
from ._module import Parent as _Parent
from ._report import generate_report as _generate_report


def _run_check(  # pylint: disable=too-many-arguments
    parent: _Parent,
    check_class: bool,
    check_dunders: bool,
    check_overridden: bool,
    check_protected: bool,
    check_property_returns: bool,
    ignore_no_params: bool,
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
            and not (func.docstring.bare and ignore_no_params)
        ):
            report = _generate_report(
                func, targets, disable, check_property_returns
            )
            if report:
                failures.append(
                    _Failure(func, _FuncStr(func, no_ansi), report)
                )

    return failures


def docsig(  # pylint: disable=too-many-locals
    *path: _Path,
    string: str | None = None,
    check_class: bool = False,
    check_dunders: bool = False,
    check_overridden: bool = False,
    check_protected: bool = False,
    check_property_returns: bool = False,
    ignore_no_params: bool = False,
    ignore_args: bool = False,
    ignore_kwargs: bool = False,
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
    :param check_property_returns: Run return checks on properties.
    :param ignore_no_params: Ignore docstrings where parameters are not
        documented
    :param ignore_args: Ignore args prefixed with an asterisk.
    :param ignore_kwargs: Ignore kwargs prefixed with two asterisks.
    :param no_ansi: Disable ANSI output.
    :param summary: Print a summarised report.
    :param targets: List of errors to target.
    :param disable: List of errors to disable.
    :return: Exit status for whether test failed or not.
    """
    modules = _Modules(
        *path,
        string=string,
        ignore_args=ignore_args,
        ignore_kwargs=ignore_kwargs,
    )
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
                    check_property_returns,
                    ignore_no_params,
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
