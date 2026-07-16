"""
docsig._traverse
================

Traverse modules and run docstring/signature checks per function.
"""

from ._checker import check_function as _check_function
from ._config import Config as _Config
from ._diagnostic import Failures as _Failures
from ._module import Function as _Function
from ._module import Scope as _Scope


def _should_check_function(
    function: _Function,
    parent: _Scope | _Function,
    config: _Config,
) -> bool:
    if function.isoverridden and not config.check.overridden:
        return False

    if function.isprotected and not config.check.protected:
        return False

    if function.isdunder and not config.check.dunders:
        return False

    if function.docstring.bare and config.ignore.no_params:
        return False

    if function.isinit and (
        not (config.check.class_ or config.check.class_constructor)
        or (parent.isprotected and not config.check.protected)
    ):
        return False

    return True


def _run_check(
    child: _Scope | _Function,
    parent: _Scope | _Function,
    config: _Config,
    failures: _Failures,
) -> None:
    if isinstance(child, _Function) and _should_check_function(
        child,
        parent,
        config,
    ):
        result = _check_function(child, config)
        if result:
            failures.append(result)

    # recurse for either class methods or, if enabled, nested functions
    if not isinstance(child, _Function) or config.check.nested:
        for child_of_child in child.children:
            _run_check(child_of_child, child, config, failures)


def run_checks(module: _Scope, config: _Config) -> _Failures:
    """Run checks on the module and return a list of failures.

    Traverse the module's functions and classes. A callable is checked
    only if it is public or if configuration allows protected or
    overridden members. Failures are collected and returned.

    :param module: A module object that contains functions or classes.
    :param config: Configuration object.
    :return: A list of function and class failures.
    """
    failures = _Failures()
    for child in module.children:
        if (
            not child.isprotected
            or config.check.protected
            or config.check.protected_class_methods
        ):
            _run_check(child, module, config, failures)

    return failures
