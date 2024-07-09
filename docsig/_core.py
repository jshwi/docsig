"""
docsig._core
============
"""

from __future__ import annotations as _

import sys as _sys
from pathlib import Path as _Path

import astroid as _ast

from . import _decorators
from ._directives import Directives as _Directives
from ._files import FILE_INFO as _FILE_INFO
from ._module import Ast as _Ast
from ._module import Function as _Function
from ._module import Parent as _Parent
from ._report import Failure as _Failure
from ._report import Failures as _Failures
from ._utils import pretty_print_error as _pretty_print_error
from ._utils import print_checks as _print_checks
from ._utils import vprint as _vprint
from .messages import TEMPLATE as _TEMPLATE
from .messages import Messages as _Messages


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
    target: _Messages,
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
                child, target, check_property_returns, ignore_typechecker
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
                    target,
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
                target,
                failures,
            )


def _get_failures(  # pylint: disable=too-many-locals,too-many-arguments
    module: _Parent,
    check_class: bool,
    check_class_constructor: bool,
    check_dunders: bool,
    check_nested: bool,
    check_overridden: bool,
    check_protected: bool,
    check_property_returns: bool,
    ignore_no_params: bool,
    ignore_typechecker: bool,
    check_protected_class_methods: bool,
    no_ansi: bool,
    target: _Messages,
) -> _Failures:
    failures = _Failures()
    for top_level in module:
        if (
            not top_level.isprotected
            or check_protected
            or check_protected_class_methods
        ):
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
                target or _Messages(),
                failures,
            )

    return failures


def _report(
    failures: _Failures, path: str | None = None, no_ansi: bool = False
) -> None:
    for failure in failures:
        module = f"{path}:" if path is not None else ""
        header = f"{module}{failure.lineno} in {failure.name}"
        if not no_ansi and _sys.stdout.isatty():
            header = f"\033[35m{header}\033[0m"

        print(header)
        for item in failure:
            print(
                "    "
                + _TEMPLATE.format(
                    ref=item.ref,
                    description=item.description,
                    symbolic=item.symbolic,
                )
            )
            if item.hint:
                print(f"    hint: {item.hint}")


def runner(  # pylint: disable=too-many-locals,too-many-arguments
    file: str | _Path,
    disable: _Messages | None = None,
    check_class: bool = False,
    check_class_constructor: bool = False,
    check_dunders: bool = False,
    check_nested: bool = False,
    check_overridden: bool = False,
    check_protected: bool = False,
    check_property_returns: bool = False,
    ignore_no_params: bool = False,
    ignore_args: bool = False,
    ignore_kwargs: bool = False,
    ignore_typechecker: bool = False,
    check_protected_class_methods: bool = False,
    no_ansi: bool = False,
    verbose: bool = False,
    target: _Messages | None = None,
) -> tuple[_Failures, int]:
    """Per path runner.

    :param file: Path to check.
    :param disable: Messages to disable.
    :param check_class: Check class docstrings.
    :param check_class_constructor: Check ``__init__`` methods. Note that this
        is mutually incompatible with check_class.
    :param check_dunders: Check dunder methods
    :param check_nested: Check nested functions and classes.
    :param check_overridden: Check overridden methods
    :param check_protected: Check protected functions and classes.
    :param check_property_returns: Run return checks on properties.
    :param ignore_no_params: Ignore docstrings where parameters are not
        documented
    :param ignore_args: Ignore args prefixed with an asterisk.
    :param ignore_kwargs: Ignore kwargs prefixed with two asterisks.
    :param ignore_typechecker: Ignore checking return values.
    :param check_protected_class_methods: Check public methods belonging
        to protected classes.
    :param no_ansi: Disable ANSI output.
    :param verbose: increase output verbosity.
    :param target: List of errors to target.
    :return: Exit status for whether test failed or not.
    """
    failures = _Failures()
    path = _Path(file)
    string = path.read_text(encoding="utf-8")
    ast = _Ast.parse(string)
    if ast.success:
        _vprint(
            _FILE_INFO.format(path=path, msg="Parsing Python code successful"),
            verbose,
        )
        module = _Parent(
            ast.module,
            _Directives(string, disable or _Messages()),
            path,
            ignore_args,
            ignore_kwargs,
            check_class_constructor,
        )
        failures = _get_failures(
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
            check_protected_class_methods,
            no_ansi,
            target or _Messages(),
        )
        return failures, 0

    if path.name.endswith(".py"):
        # pass by silently for files that do not end with .py,  may
        # result in a 123 syntax error exit status in the future
        print(path, file=_sys.stderr)
        _pretty_print_error(type(ast.err), str(ast.err), no_ansi=no_ansi)
        return failures, 1

    _vprint(
        _FILE_INFO.format(path=path, msg=str(ast.err)),
        verbose,
    )
    return failures, 0


@_decorators.parse_msgs
@_decorators.handle_deprecations
@_decorators.validate_args
@_decorators.collect_paths
def docsig(  # pylint: disable=too-many-locals,too-many-arguments
    *path: _Path,
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
    ignore_no_params: bool = False,
    ignore_args: bool = False,
    ignore_kwargs: bool = False,
    ignore_typechecker: bool = False,
    no_ansi: bool = False,
    verbose: bool = False,
    target: _Messages | None = None,
    disable: _Messages | None = None,
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
    :param ignore_no_params: Ignore docstrings where parameters are not
        documented
    :param ignore_args: Ignore args prefixed with an asterisk.
    :param ignore_kwargs: Ignore kwargs prefixed with two asterisks.
    :param ignore_typechecker: Ignore checking return values.
    :param no_ansi: Disable ANSI output.
    :param verbose: increase output verbosity.
    :param target: List of errors to target.
    :param disable: List of errors to disable.
    :return: Exit status for whether test failed or not.
    """
    if list_checks:
        return int(bool(_print_checks()))  # type: ignore

    if string is None:
        retcode = 0
        for file in path:
            failures, retcode = runner(
                file,
                disable,
                check_class,
                check_class_constructor,
                check_dunders,
                check_nested,
                check_overridden,
                check_protected,
                check_property_returns,
                ignore_no_params,
                ignore_args,
                ignore_kwargs,
                ignore_typechecker,
                check_protected_class_methods,
                no_ansi,
                verbose,
                target,
            )
            if failures:
                _report(failures, str(file), no_ansi)
                retcode = 1

        return retcode

    ast = _Ast.parse(string)
    if ast.success:
        _vprint(
            _FILE_INFO.format(
                path="stdin", msg="Parsing Python code successful"
            ),
            verbose,
        )
        module = _Parent(
            _ast.parse(string),
            _Directives(string, messages=disable or _Messages()),
            ignore_args=ignore_args,
            ignore_kwargs=ignore_kwargs,
            check_class_constructor=check_class_constructor,
        )
        failures = _get_failures(
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
            check_protected_class_methods,
            no_ansi,
            target or _Messages(),
        )
        if failures:
            _report(failures, no_ansi=no_ansi)
            return 1

        _vprint(_FILE_INFO.format(path="stdin", msg=str(ast.err)), verbose)

    return 0
