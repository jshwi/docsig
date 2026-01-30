"""
docsig._core
============
"""

from __future__ import annotations as _

import logging as _logging
import os as _os
import sys as _sys
import typing as _t
from pathlib import Path as _Path

import astroid as _ast

from . import _decorators
from ._config import Check as _Check
from ._config import Config as _Config
from ._config import Ignore as _Ignore
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


def _should_check_function(
    child: _Function,
    parent: _Parent,
    config: _Config,
) -> bool:
    if child.isoverridden and not config.check.overridden:
        return False

    if child.isprotected and not config.check.protected:
        return False

    if child.isdunder and not config.check.dunders:
        return False

    if child.docstring.bare and config.ignore.no_params:
        return False

    if child.isinit and (
        not (config.check.class_ or config.check.class_constructor)
        or (parent.isprotected and not config.check.protected)
    ):
        return False

    return True


def _run_check(
    child: _Parent,
    parent: _Parent,
    config: _Config,
    failures: _Failures,
) -> None:
    if isinstance(child, _Function) and _should_check_function(
        child,
        parent,
        config,
    ):
        failure = _Failure(
            child,
            config.target,
            config.check.property_returns,
            config.ignore.typechecker,
        )
        if failure:
            failures.append(failure)

    # recurse for either class methods or, if enabled, nested functions
    if not isinstance(child, _Function) or config.check.nested:
        for func in child.children:
            _run_check(func, child, config, failures)


def _from_file(path: _Path, config: _Config) -> _Parent:
    try:
        code = path.read_text(encoding="utf-8")
        parent = _from_str(
            context={
                "code": code,
                "module_name": _derive_module_name(path),
                "path": path,
            },
            config=config,
            path=path,
        )
    except UnicodeDecodeError as err:
        logger = _logging.getLogger(__package__)
        logger.debug(_FILE_INFO, path, str(err).replace("\n", " "))
        parent = _Parent(error=_Error.UNICODE)

    if parent.error is not None and not path.name.endswith(".py"):
        parent = _Parent()

    return parent


def _from_str(
    context: dict[str, _t.Any],
    config: _Config,
    path: _Path | None = None,
) -> _Parent:
    logger = _logging.getLogger(__package__)
    source_name = path or "stdin"
    try:
        parent = _Parent(
            _ast.parse(**context),
            _Directives.from_text(context["code"], config.disable),
            path,
            config.ignore.args,
            config.ignore.kwargs,
            config.check.class_constructor,
        )
        logger.debug(_FILE_INFO, source_name, "Parsing Python code successful")
    except _ast.AstroidSyntaxError as err:
        logger.debug(_FILE_INFO, source_name, str(err).replace("\n", " "))
        parent = _Parent(error=_Error.SYNTAX)

    return parent


def _get_failures(module: _Parent, config: _Config) -> _Failures:
    failures = _Failures()
    for top_level in module.children:
        if (
            not top_level.isprotected
            or config.check.protected
            or config.check.protected_class_methods
        ):
            _run_check(top_level, module, config, failures)

    return failures


def _report(
    failures: _Failures,
    config: _Config,
    path: str | None = None,
) -> int:
    retcodes = [0]
    for failure in failures:
        retcodes.append(failure.retcode)
        path_prefix = f"{path}:" if path is not None else ""
        header = f"{path_prefix}{failure.lineno} in {failure.name}"
        if not config.no_ansi and _sys.stdout.isatty():
            header = f"\033[35m{header}\033[0m"

        print(header)
        for item in failure:
            print(
                "    "
                + _TEMPLATE.format(
                    ref=item.ref,
                    description=item.description,
                    symbolic=item.symbolic,
                ),
            )
            if item.hint:
                print(f"    hint: {item.hint}")

    return max(retcodes)


def _run_docsig(
    *path: str | _Path,
    string: str | None = None,
    config: _Config,
) -> int:
    setup_logger(config.verbose)
    if config.list_checks:
        return int(bool(_print_checks()))  # type: ignore

    if string is None:
        retcodes = [0]
        paths = _Paths(
            *path,
            patterns=config.exclude,
            excludes=config.excludes,
            include_ignored=config.include_ignored,
        )
        for path_ in paths:
            failures = runner(path_, config)
            retcodes.append(_report(failures, config, str(path_)))

        return max(retcodes)

    module = _from_str({"code": string}, config)
    failures = _get_failures(module, config)
    return _report(failures, config)


def runner(path: _Path, config: _Config) -> _Failures:
    """Per path runner.

    :param path: Path to check.
    :param config: Configuration object.
    :return: Exit status for whether the test failed or not.
    """
    module = _from_file(path, config)
    return _get_failures(module, config)


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
    :param verbose: Increase output verbosity.
    :param target: List of errors to target.
    :param disable: List of errors to disable.
    :param exclude: Regular expression of files and dirs to exclude from
        checks.
    :param excludes: Files or dirs to exclude from checks.
    :return: Exit status for whether a test failed or not.
    """
    exclude_ = [_DEFAULT_EXCLUDES]
    if exclude is not None:
        exclude_.append(exclude)

    check = _Check(
        class_=check_class,
        class_constructor=check_class_constructor,
        dunders=check_dunders,
        protected_class_methods=check_protected_class_methods,
        nested=check_nested,
        overridden=check_overridden,
        protected=check_protected,
        property_returns=check_property_returns,
    )
    ignore = _Ignore(
        no_params=ignore_no_params,
        args=ignore_args,
        kwargs=ignore_kwargs,
        typechecker=ignore_typechecker,
    )
    config = _Config(
        list_checks=list_checks,
        include_ignored=include_ignored,
        check=check,
        ignore=ignore,
        no_ansi=no_ansi,
        verbose=verbose,
        target=target or _Messages(),
        disable=disable or _Messages(),
        exclude=exclude_,
        excludes=excludes,
    )
    return _run_docsig(*path, string=string, config=config)


def _derive_module_name(file_path: str | _Path) -> str:
    converted = _os.path.splitext(str(file_path))[0]
    converted = converted.replace(_os.sep, ".")
    converted = converted.replace("-", "_")
    return converted
