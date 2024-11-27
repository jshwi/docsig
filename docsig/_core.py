"""
docsig._core
============
"""

from __future__ import annotations as _

import logging as _logging
import sys as _sys
from pathlib import Path as _Path

import astroid as _ast

from . import _decorators
from ._directives import Directives as _Directives
from ._files import FILE_INFO as _FILE_INFO
from ._files import Paths as _Paths
from ._module import Error as _Error
from ._module import Function as _Function
from ._module import Parent as _Parent
from ._report import Failure as _Failure
from ._report import Failures as _Failures
from ._utils import print_checks as _print_checks
from .messages import TEMPLATE as _TEMPLATE
from .messages import Messages as _Messages

_DEFAULT_EXCLUDES = """\
(?x)^(
    |\\.?venv[\\\\/].*
    |\\.git[\\\\/].*
    |\\.hg[\\\\/].*
    |\\.idea[\\\\/].*
    |\\.mypy_cache[\\\\/].*
    |\\.nox[\\\\/].*
    |\\.pytest_cache[\\\\/].*
    |\\.svn[\\\\/].*
    |\\.tox[\\\\/].*
    |\\.vscode[\\\\/].*
    |_?build[\\\\/].*
    |.*[\\\\/]__pycache__[\\\\/].*
    |dist[\\\\/].*
    |node_modules[\\\\/].*
)$
"""


def setup_logger(verbose: bool) -> None:
    """Setup docsig logger.

    Only log if verbose mode is enabled.

    :param verbose: Whether to enable verbose mode.
    """
    loglevel = _logging.DEBUG if verbose else _logging.INFO
    logger = _logging.getLogger(__package__)
    logger.setLevel(loglevel)
    if not logger.handlers:
        stream_handler = _logging.StreamHandler(_sys.stdout)
        logger.addHandler(stream_handler)


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
            for func in child.children:
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
        for func in child.children:
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


def _from_file(
    path: _Path,
    messages: _Messages,
    ignore_args: bool,
    ignore_kwargs: bool,
    check_class_constructor,
) -> _Parent:
    try:
        string = path.read_text(encoding="utf-8")
        parent = _from_str(
            messages=messages,
            string=string,
            path=path,
            ignore_args=ignore_args,
            ignore_kwargs=ignore_kwargs,
            check_class_constructor=check_class_constructor,
        )
    except UnicodeDecodeError as err:
        logger = _logging.getLogger(__package__)
        logger.debug(_FILE_INFO, path, str(err).replace("\n", " "))
        parent = _Parent(error=_Error.UNICODE)

    if parent.error is not None and not path.name.endswith(".py"):
        parent = _Parent()

    return parent


def _from_str(  # pylint: disable=too-many-arguments
    string: str,
    messages: _Messages,
    ignore_args: bool,
    ignore_kwargs: bool,
    check_class_constructor,
    path: _Path | None = None,
) -> _Parent:
    logger = _logging.getLogger(__package__)
    try:
        parent = _Parent(
            _ast.parse(string),
            _Directives.from_text(string, messages),
            path,
            ignore_args,
            ignore_kwargs,
            check_class_constructor,
        )
        logger.debug(
            _FILE_INFO, path or "stdin", "Parsing Python code successful"
        )
    except _ast.AstroidSyntaxError as err:
        logger.debug(_FILE_INFO, path or "stdin", str(err).replace("\n", " "))
        parent = _Parent(error=_Error.SYNTAX)

    return parent


def _get_failures(  # pylint: disable=too-many-arguments
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
    for top_level in module.children:
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
) -> int:
    retcodes = [0]
    for failure in failures:
        retcodes.append(failure.retcode)
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

    return max(retcodes)


def runner(  # pylint: disable=too-many-locals,too-many-arguments
    path: _Path,
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
    target: _Messages | None = None,
) -> _Failures:
    """Per path runner.

    :param path: Path to check.
    :param disable: Messages to disable.
    :param check_class: Check class docstrings.
    :param check_class_constructor: Check ``__init__`` methods. Note
        that this is mutually incompatible with check_class.
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
    :param target: List of errors to target.
    :return: Exit status for whether test failed or not.
    """
    module = _from_file(
        path,
        disable or _Messages(),
        ignore_args,
        ignore_kwargs,
        check_class_constructor,
    )
    return _get_failures(
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
    target: _Messages | None = None,
    disable: _Messages | None = None,
    exclude: str | None = None,
    excludes: list[str] | None = None,
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
    :param check_class_constructor: Check ``__init__`` methods. Note
        that this is mutually incompatible with check_class.
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
    :param target: List of errors to target.
    :param disable: List of errors to disable.
    :param exclude: Regular expression of files and dirs to exclude from
        checks.
    :param excludes: Files or dirs to exclude from checks.
    :return: Exit status for whether test failed or not.
    """
    setup_logger(verbose)
    if list_checks:
        return int(bool(_print_checks()))  # type: ignore

    exclude_ = [_DEFAULT_EXCLUDES]
    if exclude is not None:
        exclude_.append(exclude)

    if string is None:
        retcodes = [0]
        paths = _Paths(
            *path,
            patterns=exclude_,
            excludes=excludes,
            include_ignored=include_ignored,
        )
        for path_ in paths:
            failures = runner(
                path_,
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
                target,
            )
            retcodes.append(_report(failures, str(path_), no_ansi))

        return max(retcodes)

    module = _from_str(
        string,
        disable or _Messages(),
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
    return _report(failures, no_ansi=no_ansi)
