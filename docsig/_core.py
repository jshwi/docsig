"""
docsig._core
============
"""
from __future__ import annotations as _

from pathlib import Path as _Path

from . import _decorators
from ._display import Display as _Display
from ._display import Failure as _Failure
from ._display import Failures as _Failures
from ._display import FuncStr as _FuncStr
from ._message import Message as _Message
from ._module import Modules as _Modules
from ._module import Parent as _Parent
from ._report import generate_report as _generate_report
from .messages import TEMPLATE as _TEMPLATE
from .messages import E as _E


def _print_checks() -> None:
    for msg in _E.values():
        print(msg.fstring(_TEMPLATE))


def _run_check(  # pylint: disable=too-many-arguments
    parent: _Parent,
    check_class: bool,
    check_class_constructor: bool,
    check_dunders: bool,
    check_overridden: bool,
    check_protected: bool,
    check_property_returns: bool,
    ignore_no_params: bool,
    no_ansi: bool,
    targets: list[_Message],
) -> _Failures:
    failures = _Failures()
    for func in parent:
        if not (func.isoverridden and not check_overridden) and (
            not (func.isprotected and not check_protected)
            and not (
                func.isinit
                and not (
                    (check_class or check_class_constructor)
                    and not (parent.isprotected and not check_protected)
                )
            )
            and not (func.isdunder and not check_dunders)
            and not (func.docstring.bare and ignore_no_params)
        ):
            report = _generate_report(
                func, targets, func.disabled, check_property_returns
            )
            if report:
                failures.append(
                    _Failure(func, _FuncStr(func, no_ansi), report)
                )

    return failures


@_decorators.parse_msgs
@_decorators.validate_args
def docsig(  # pylint: disable=too-many-locals,too-many-arguments
    *path: str | _Path,
    string: str | None = None,
    list_checks: bool = False,
    check_class: bool = False,
    check_class_constructor: bool = False,
    check_dunders: bool = False,
    check_protected_class_methods: bool = False,
    check_overridden: bool = False,
    check_protected: bool = False,
    check_property_returns: bool = False,
    ignore_no_params: bool = False,
    ignore_args: bool = False,
    ignore_kwargs: bool = False,
    no_ansi: bool = False,
    summary: bool = False,
    targets: list[_Message] | None = None,
    disable: list[_Message] | None = None,
) -> int:
    """Package's core functionality.

    Populate a sequence of module objects before iterating over their
    top-level functions and classes.

    If any of the functions within the module - and methods within its
    classes - fail, print the resulting function string representation
    and report.

    :param path: Path(s) to check.
    :param string: String to check.
    :param list_checks: Display a list of all checks and their messages.
    :param check_class: Check class docstrings.
    :param check_class_constructor: Check ``__init__`` methods. Note that this
        is mutually incompatible with check_class.
    :param check_dunders: Check dunder methods
    :param check_protected_class_methods: Check public methods belonging
        to protected classes.
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
    if list_checks:
        return int(bool(_print_checks()))  # type: ignore

    modules = _Modules(
        *tuple(_Path(i) for i in path),
        disable=disable or [],
        string=string,
        ignore_args=ignore_args,
        ignore_kwargs=ignore_kwargs,
        check_class_constructor=check_class_constructor,
    )
    display = _Display(no_ansi)
    for module in modules:
        for top_level in module:
            if (
                not top_level.isprotected
                or check_protected
                or check_protected_class_methods
            ):
                failures = _run_check(
                    top_level,
                    check_class,
                    check_class_constructor,
                    check_dunders,
                    check_overridden,
                    check_protected,
                    check_property_returns,
                    ignore_no_params,
                    no_ansi,
                    targets or [],
                )
                if failures:
                    display[top_level.path].append(failures)

    if summary:
        display.summarise()
    else:
        display.report()

    return int(bool(display))
