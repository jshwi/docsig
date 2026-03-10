"""
docsig._core
============

Entry point and orchestration for running docstring/signature checks.
"""

from __future__ import annotations as _

import logging as _logging
import os as _os
import sys as _sys
import warnings as _warnings
from pathlib import Path as _Path
from tokenize import TokenError as _TokenError
from warnings import warn as _warn

import astroid as _ast

from . import _decorators
from ._check import run_checks as _run_checks
from ._config import Check as _Check
from ._config import Config as _Config
from ._config import Ignore as _Ignore
from ._directives import Directives as _Directives
from ._files import FILE_INFO as _FILE_INFO
from ._files import Paths as _Paths
from ._module import Error as _Error
from ._module import Parent as _Parent
from ._report import Failures as _Failures
from ._utils import print_checks as _print_checks
from .messages import NEW as _NEW
from .messages import TEMPLATE as _TEMPLATE
from .messages import E as _E
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
    """Set up the docsig logger.

    Only log if verbose mode is enabled.

    :param verbose: Whether to enable verbose mode.
    """
    loglevel = _logging.DEBUG if verbose else _logging.INFO
    logger = _logging.getLogger(__package__)
    logger.setLevel(loglevel)
    if not logger.handlers:
        stream_handler = _logging.StreamHandler(_sys.stdout)
        logger.addHandler(stream_handler)


def _parse_from_file(path: _Path, config: _Config) -> _Parent:
    try:
        code = path.read_text(encoding="utf-8")
        parent = _parse_from_string(
            code,
            config,
            str(path)[:-3].replace(_os.sep, ".").replace("-", "_"),
            path,
        )
    except UnicodeDecodeError as err:
        logger = _logging.getLogger(__package__)
        logger.debug(_FILE_INFO, path, str(err).replace("\n", " "))
        parent = _Parent(error=_Error.UNICODE)

    if parent.error is not None and not path.name.endswith(".py"):
        parent = _Parent()

    return parent


def _parse_from_string(
    code: str,
    config: _Config,
    module_name: str = "",
    path: _Path | None = None,
) -> _Parent:
    logger = _logging.getLogger(__package__)
    source_name = path or "stdin"
    try:
        node = _ast.parse(code, module_name, str(path))
        try:
            directives = _Directives.from_text(code, config.disable)
        except _TokenError as err:
            directives = _Directives()
            logger.debug(
                _FILE_INFO,
                source_name,
                f"error parsing comments {err}".lower(),
            )

        parent = _Parent(
            node,
            directives,
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
            extra = None
            if item.hint:
                extra = f"hint: {item.hint}"

            if item.new:
                extra = "warning: please remember to fix this or disable it"
                _warn(_NEW.format(ref=item.ref), FutureWarning, stacklevel=3)

            print(
                "    "
                + _TEMPLATE.format(
                    ref=item.ref,
                    description=item.description,
                    symbolic=item.symbolic,
                ),
            )
            if extra is not None:
                print(f"    {extra}")

    return max(retcodes)


def handle_deprecations(
    ignore_typechecker: bool,
    disable: list,
    messages: list,
    stacklevel: int,
) -> None:
    """Warn for deprecated arguments.

    :param ignore_typechecker: Whether using or not.
    :param disable: List to add messages to.
    :param messages: Messages.
    :param stacklevel: Warning stacklevel.
    """
    if ignore_typechecker:
        _warnings.warn(
            "ignore-typechecker is deprecated, use disable for SIG5xx instead",
            category=FutureWarning,
            stacklevel=stacklevel,
        )
        disable.extend(messages)


def runner(path: _Path, config: _Config) -> _Failures:
    """Run checks for a single file and return collected failures.

    :param path: Path to the file to check.
    :param config: Configuration object.
    :return: Collected failures for the file.
    """
    module = _parse_from_file(path, config)
    return _run_checks(module, config)


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
    ignore_typechecker: bool = False,  # deprecated
    no_ansi: bool = False,
    verbose: bool = False,
    target: _Messages | None = None,
    disable: _Messages | None = None,
    exclude: str | None = None,
    excludes: list[str] | None = None,
) -> int:
    """Run docstring/signature checks on paths or a string and report.

    Build module objects from the given path(s) or string, then run
    checks on their top-level functions and classes. If any fail, print
    the function representation and report. Return a non-zero exit code
    when there are failures.

    :param path: Path(s) to check.
    :param string: String to check instead of files.
    :param list_checks: Display a list of all checks and their messages.
    :param check_class: Check class docstrings.
    :param check_class_constructor: Check ``__init__`` methods. Mutually
        incompatible with check_class.
    :param check_dunders: Check dunder methods.
    :param check_protected_class_methods: Check public methods belonging
        to protected classes.
    :param check_nested: Check nested functions and classes.
    :param check_overridden: Check overridden methods.
    :param check_protected: Check protected functions and classes.
    :param check_property_returns: Run return checks on properties.
    :param include_ignored: Check files even if they match a gitignore
        pattern.
    :param ignore_no_params: Ignore docstrings where parameters are not
        documented.
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
    :return: Exit code (non-zero if any check failed).
    """
    disable = disable or _Messages()
    handle_deprecations(
        ignore_typechecker,
        disable,
        [
            _E[501],
            _E[502],
            _E[503],
            _E[504],
            _E[505],
            _E[506],
        ],
        stacklevel=5,
    )
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
    )
    config = _Config(
        list_checks=list_checks,
        include_ignored=include_ignored,
        check=check,
        ignore=ignore,
        no_ansi=no_ansi,
        verbose=verbose,
        target=target or _Messages(),
        disable=disable,
        exclude=exclude_,
        excludes=excludes,
    )
    setup_logger(config.verbose)
    if config.list_checks:
        return int(bool(_print_checks()))  # type: ignore

    if string:
        module = _parse_from_string(string, config)
        failures = _run_checks(module, config)
        return _report(failures, config)

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
