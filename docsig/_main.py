"""
docsig._main
============

CLI entry point that parses args and runs docsig.
"""

import os as _os
import sys as _sys
import warnings as _warnings

from ._config import parse_args as _parse_args
from ._core import docsig as _docsig
from ._report import pretty_print_error as _pretty_print_error


def _excepthook(no_ansi: bool = False) -> None:
    """Install a hook that prints user-friendly errors (not default).

    Skipped when DOCSIG_DEBUG is set to "1".

    :param no_ansi: Whether to disable ANSI escape codes in output.
    """
    if _os.environ.get("DOCSIG_DEBUG") != "1":
        _sys.excepthook = lambda x, y, _: _pretty_print_error(
            x,
            str(y),
            no_ansi,
        )


def _warn_on_deprecated_short_flags() -> None:
    deprecated_short_flags = {
        "-I": "--include-ignored",
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
    """Parse CLI args, install the exception hook, and run docsig.

    :return: Exit code (non-zero if any check failed).
    """
    if _os.getenv("_DOCSIG_FORMAT_JSON"):
        _warnings.simplefilter("ignore", FutureWarning)

    _warn_on_deprecated_short_flags()
    a = _parse_args()
    _excepthook(a.no_ansi)
    kwargs = vars(a)
    path = kwargs.pop("path")
    return _docsig(*path, **kwargs)
