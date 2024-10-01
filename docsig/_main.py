"""
docsig._main
============

Contains package entry point.
"""

from __future__ import annotations as _

from ._config import parse_args as _parse_args
from ._core import docsig as _docsig
from ._hooks import excepthook as _excepthook


def main() -> str | int:
    """Main function for package.

    Collect config and arguments for the commandline.

    :return: Exit status for whether test failed or not.
    """
    a = _parse_args()
    _excepthook(a.no_ansi)
    return _docsig(
        *a.path,
        string=a.string,
        list_checks=a.list_checks,
        check_class=a.check_class,
        check_class_constructor=a.check_class_constructor,
        check_dunders=a.check_dunders,
        check_protected_class_methods=a.check_protected_class_methods,
        check_nested=a.check_nested,
        check_overridden=a.check_overridden,
        check_protected=a.check_protected,
        check_property_returns=a.check_property_returns,
        include_ignored=a.include_ignored,
        ignore_no_params=a.ignore_no_params,
        ignore_args=a.ignore_args,
        ignore_kwargs=a.ignore_kwargs,
        ignore_typechecker=a.ignore_typechecker,
        no_ansi=a.no_ansi,
        verbose=a.verbose,
        target=a.target,
        disable=a.disable,
        exclude=a.exclude,
        excludes=a.excludes,
    )
