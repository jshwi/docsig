"""
docsig._check
=============
"""

from __future__ import annotations as _

from ._config import Config as _Config
from ._module import Function as _Function
from ._module import Parent as _Parent
from ._report import Failure as _Failure
from ._report import Failures as _Failures


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
        failure = _Failure(child, config)
        if failure:
            failures.append(failure)

    # recurse for either class methods or, if enabled, nested functions
    if not isinstance(child, _Function) or config.check.nested:
        for func in child.children:
            _run_check(func, child, config, failures)


def run_checks(module: _Parent, config: _Config) -> _Failures:
    """Run checks on the module and return a list of failures.

    Traverse the module's functions and classes. A callable is checked
    only if it is public or if configuration allows protected or
    overridden members. Failures are collected and returned.

    :param module: A module object that contains functions or classes.
    :param config: Configuration object.
    :return: A list of function and class failures.
    """
    failures = _Failures()
    for top_level in module.children:
        if (
            not top_level.isprotected
            or config.check.protected
            or config.check.protected_class_methods
        ):
            _run_check(top_level, module, config, failures)

    return failures
