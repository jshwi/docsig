"""
docsig._core
============
"""

from __future__ import annotations as _

from pathlib import Path as _Path

from . import _decorators
from ._module import Function as _Function
from ._module import Modules as _Modules
from ._module import Parent as _Parent
from ._report import Failure as _Failure
from ._report import Failures as _Failures
from ._report import Report as _Report
from ._utils import print_checks as _print_checks
from .messages import Messages as _Messages

_DEFAULT_EXCLUDES = """\
(?x)^(
    |\\.?venv
    |\\.git
    |\\.hg
    |\\.idea
    |\\.mypy_cache
    |\\.nox
    |\\.pytest_cache
    |\\.svn
    |\\.tox
    |\\.vscode
    |_?build
    |__pycache__
    |dist
    |node_modules
)$
"""


def _run_check(  # pylint: disable=too-many-arguments,too-many-locals
    child: _Parent,
    parent: _Parent,
    check_class: bool,
    check_class_constructor: bool,
    check_dunders: bool,
    check_nested: bool,
    check_overridden: bool,
    check_protected: bool,
    check_property_returns: bool,
    ignore_no_params: bool,
    ignore_typechecker: bool,
    no_ansi: bool,
    targets: _Messages,
    failures: _Failures,
) -> None:
    if isinstance(child, _Function):
        if not (child.isoverridden and not check_overridden) and (
            not (child.isprotected and not check_protected)
            and not (
                child.isinit
                and not (
                    (check_class or check_class_constructor)
                    and not (parent.isprotected and not check_protected)
                )
            )
            and not (child.isdunder and not check_dunders)
            and not (child.docstring.bare and ignore_no_params)
        ):
            failure = _Failure(
                child,
                targets,
                child.messages,
                check_property_returns,
                ignore_typechecker,
            )
            if failure:
                failures.append(failure)

        if check_nested:
            for func in child:
                _run_check(
                    func,
                    child,
                    check_class,
                    check_class_constructor,
                    check_dunders,
                    check_nested,
                    check_overridden,
                    check_protected,
                    check_property_returns,
                    ignore_no_params,
                    ignore_typechecker,
                    no_ansi,
                    targets,
                    failures,
                )
    else:
        # this is a class
        for func in child:
            _run_check(
                func,
                child,
                check_class,
                check_class_constructor,
                check_dunders,
                check_nested,
                check_overridden,
                check_protected,
                check_property_returns,
                ignore_no_params,
                ignore_typechecker,
                no_ansi,
                targets,
                failures,
            )


@_decorators.parse_msgs
@_decorators.handle_deprecations
@_decorators.validate_args
def docsig(  # pylint: disable=too-many-locals,too-many-arguments
    *path: str | _Path,
    string: str | None = None,
    list_checks: bool = False,
    check_class: bool = False,
    check_class_constructor: bool = False,
    check_dunders: bool = False,
    check_protected_class_methods: bool = False,
    check_nested: bool = False,
    check_overridden: bool = False,
    check_protected: bool = False,
    check_property_returns: bool = False,
    include_ignored: bool = False,
    ignore_no_params: bool = False,
    ignore_args: bool = False,
    ignore_kwargs: bool = False,
    ignore_typechecker: bool = False,
    no_ansi: bool = False,
    verbose: bool = False,
    targets: _Messages | None = None,
    disable: _Messages | None = None,
    exclude: str | None = None,
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
    :param check_nested: Check nested functions and classes.
    :param check_overridden: Check overridden methods
    :param check_protected: Check protected functions and classes.
    :param check_property_returns: Run return checks on properties.
    :param include_ignored: Check files even if they match a gitignore
        pattern.
    :param ignore_no_params: Ignore docstrings where parameters are not
        documented
    :param ignore_args: Ignore args prefixed with an asterisk.
    :param ignore_kwargs: Ignore kwargs prefixed with two asterisks.
    :param ignore_typechecker: Ignore checking return values.
    :param no_ansi: Disable ANSI output.
    :param verbose: increase output verbosity.
    :param targets: List of errors to target.
    :param disable: List of errors to disable.
    :param exclude: Regular expression of files and dirs to exclude from
        checks.
    :return: Exit status for whether test failed or not.
    """
    if list_checks:
        return int(bool(_print_checks()))  # type: ignore

    excludes = [_DEFAULT_EXCLUDES]
    if exclude is not None:
        excludes.append(exclude)

    modules = _Modules(
        *tuple(_Path(i) for i in path),
        messages=disable or _Messages(),
        string=string,
        excludes=excludes,
        include_ignored=include_ignored,
        ignore_args=ignore_args,
        ignore_kwargs=ignore_kwargs,
        check_class_constructor=check_class_constructor,
        no_ansi=no_ansi,
        verbose=verbose,
    )
    report = _Report()
    for module in modules:
        for top_level in module:
            if (
                not top_level.isprotected
                or check_protected
                or check_protected_class_methods
            ):
                failures = _Failures()
                _run_check(
                    top_level,
                    module,
                    check_class,
                    check_class_constructor,
                    check_dunders,
                    check_nested,
                    check_overridden,
                    check_protected,
                    check_property_returns,
                    ignore_no_params,
                    ignore_typechecker,
                    no_ansi,
                    targets or _Messages(),
                    failures,
                )
                if failures:
                    report[top_level.path].append(failures)

    report.print(no_ansi)
    return max(int(bool(report)), modules.retcode)
