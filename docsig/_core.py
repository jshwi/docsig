"""
docsig._core
============

Entry point and orchestration for running docstring/signature checks.
"""

import logging as _logging
import sys as _sys
import typing as _t
from pathlib import Path as _Path
from pprint import pformat as _pformat

from . import _decorators
from ._config import DEFAULT_EXCLUDES as _DEFAULT_EXCLUDES
from ._config import Check as _Check
from ._config import Config as _Config
from ._config import Filters as _Filters
from ._config import Ignore as _Ignore
from ._diagnostic import Failures as _Failures
from ._diagnostic import RetCode as _RetCode
from ._files import Files as _Files
from ._parsers import parse_from_file as _parse_from_file
from ._parsers import parse_from_string as _parse_from_string
from ._report import print_checks as _print_checks
from ._report import report as _report
from ._traverse import run_checks as _run_checks
from .messages import Messages as _Messages


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


def runner(file: _Path, config: _Config) -> _Failures:
    """Run checks for a single file and return collected failures.

    :param file: Path to the file to check.
    :param config: Configuration object.
    :return: Collected failures for the file.
    """
    module = _parse_from_file(file, config)
    return _run_checks(module, config)


def _check_string(string: str, config: _Config) -> int:
    module = _parse_from_string(string, config)
    failures = _run_checks(module, config)
    return _report(failures, config)


def _check_files(paths: tuple[str | _Path, ...], config: _Config) -> int:
    retcodes = _RetCode()
    for file in _Files(paths, config.filters):
        failures = runner(file, config)
        retcodes.add(_report(failures, config, str(file)))

    return retcodes.result


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
    no_ansi: bool = False,
    verbose: bool = False,
    target: list[str] | None = None,
    disable: list[str] | None = None,
    exclude: str | list[str] | None = None,
    exclude_glob: list[str] | None = None,
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
    :param no_ansi: Disable ANSI output.
    :param verbose: Increase output verbosity.
    :param target: List of errors to target.
    :param disable: List of errors to disable.
    :param exclude: Regular expression(s) of files and dirs to exclude
        from checks, joined with the default exclusions.
    :param exclude_glob: Files or dirs to exclude from checks.
    :return: Exit code (non-zero if any check failed).
    """
    exclude_patterns = [_DEFAULT_EXCLUDES]
    if isinstance(exclude, str):
        exclude_patterns.append(exclude)
    elif exclude:
        exclude_patterns.extend(exclude)

    # while some params could be taken out for one time use (such as
    # verbose), bundling all the configuration together makes it easier
    # to report what args were provided in verbose mode
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
    filters = _Filters(
        include_ignored=include_ignored,
        exclude=exclude_patterns,
        exclude_glob=exclude_glob or [],
    )
    config = _Config(
        list_checks=list_checks,
        check=check,
        ignore=ignore,
        filters=filters,
        no_ansi=no_ansi,
        verbose=verbose,
        # the annotations describe the caller's interface; _parse_msgs
        # has already converted these to Messages by the time they land
        target=_t.cast("_Messages | None", target) or _Messages(),
        disable=_t.cast("_Messages | None", disable) or _Messages(),
    )
    setup_logger(config.verbose)
    _logging.getLogger(__package__).debug(_pformat(config))
    if config.list_checks:
        # noinspection PyNoneFunctionAssignment
        return int(bool(_print_checks()))  # type: ignore

    if string:
        return _check_string(string, config)

    return _check_files(path, config)
