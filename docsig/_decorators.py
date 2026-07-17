"""
docsig._decorators
==================
"""

import functools as _functools
import sys as _sys
import typing as _t
from pathlib import Path as _Path

from ._diagnostic import RetCode as _RetCode
from ._report import print_error as _print_error
from .messages import E as _E

_FuncType = _t.Callable[..., int]


def parse_msgs(func: _FuncType) -> _FuncType:
    """Convert disable and target kwargs to message objects.

    The wrapped function receives kwargs with disable and target as
    Message lists instead of raw strings.

    :param func: Function to wrap.
    :return: Wrapped function.
    """

    @_functools.wraps(func)
    def _wrapper(*args: str | _Path, **kwargs: _t.Any) -> int:
        disable = _E.from_codes(kwargs.get("disable", [])) or None
        target = _E.from_codes(kwargs.get("target", [])) or None
        kwargs["disable"] = disable
        kwargs["target"] = target
        return func(*args, **kwargs)

    return _wrapper


# TODO: make report json by default and wrap with a reporter for cli
def validate_args(func: _FuncType) -> _FuncType:
    """Validate arguments before calling the wrapped function.

    If path or string is missing, or disable and target options are
    unknown, or mutually exclusive options are set, return an error
    string instead of calling the function.

    Argparse is not sufficient if there is an issue with the
    pyproject.toml file or the API is used incorrectly.

    :param func: Function to wrap.
    :return: Wrapped function.
    """

    @_functools.wraps(func)
    def _wrapper(*args: str | _Path, **kwargs: _t.Any) -> int:
        retcode = _RetCode(2)
        errors = []
        if not kwargs.get("list_checks", False):
            if not args and not kwargs.get("string"):
                errors.append(
                    "the following arguments are required: path(s) or string",
                )

            for option in ("disable", "target"):
                for message in kwargs.get(option) or []:
                    if not message.isknown:
                        errors.append(
                            f"unknown option to {option}"
                            f" '{message.description}'",
                        )

            if kwargs.get("check_class") and kwargs.get(
                "check_class_constructor",
            ):
                errors.append(
                    "argument to check class constructor not allowed with"
                    " argument to check class",
                )
                # if we don't make it past this condition, then we are
                # running this using the python interpreter
                if _sys.stdin and _sys.stdin.isatty():
                    # otherwise, it is impossible to reach here by
                    # passing both commandline args as argparse won't
                    # allow it, therefore, this must be an issue with
                    # the pyproject.toml configuration
                    errors.append(
                        "please check your pyproject.toml configuration",
                    )
        if errors:
            _print_error("\n".join(errors), retcode.result)
            return retcode.result

        return func(*args, **kwargs)

    return _wrapper
