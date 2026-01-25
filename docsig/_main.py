"""
docsig._main
============

Contains package entry point.
"""

from __future__ import annotations as _

import sys as _sys
import warnings as _warnings

from ._config import parse_args as _parse_args
from ._core import docsig as _docsig
from ._hooks import excepthook as _excepthook


def _warn_on_deprecated_short_flags() -> None:
    deprecated_short_flags = {
        "-c": "--check-class",
        "-C": "--check-class-constructor",
        "-D": "--check-dunders",
        "-m": "--check-protected-class-methods",
        "-N": "--check-nested",
        "-o": "--check-overridden",
        "-p": "--check-protected",
        "-P": "--check-property-returns",
        "-i": "--ignore-no-params",
        "-a": "--ignore-args",
        "-k": "--ignore-kwargs",
    }
    raw_args = _sys.argv[1:]
    expanded_flags = []
    for arg in raw_args:
        if arg.startswith("--") or not arg.startswith("-") or arg == "-":
            expanded_flags.append(arg)
        elif len(arg) > 2:
            expanded_flags.extend([f"-{ch}" for ch in arg[1:]])
        else:
            expanded_flags.append(arg)

    used_flags = set(expanded_flags)
    for short, long in deprecated_short_flags.items():
        if short in used_flags:
            _warnings.warn(
                f"short option '{short}' is deprecated, use '{long}' instead",
                category=FutureWarning,
                stacklevel=2,
            )


def main() -> str | int:
    """Main function for package.

    Collect config and arguments for the commandline.

    :return: Exit status for whether the test failed or not.
    """
    _warn_on_deprecated_short_flags()
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
