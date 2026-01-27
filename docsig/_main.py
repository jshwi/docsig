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
        "-D": "--check-dunders",
        "-o": "--check-overridden",
        "-p": "--check-protected",
        "-P": "--check-property-returns",
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
    kwargs = vars(a)
    path = kwargs.pop("path")
    return _docsig(*path, **kwargs)
