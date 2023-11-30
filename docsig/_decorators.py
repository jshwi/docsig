"""
docsig._decorators
==================
"""
from __future__ import annotations as _

import sys as _sys
import typing as _t
from pathlib import Path as _Path

from .messages import E as _E

_FuncType = _t.Callable[..., _t.Union[int]]
_WrappedFuncType = _t.Callable[..., _t.Union[str, int]]


def parse_msgs(func: _WrappedFuncType) -> _WrappedFuncType:
    """Parse error codes or symbolic messages into message objects.

    :param func: Function to wrap.
    :return: Wrapped function.
    """

    def _wrapper(*args: str | _Path, **kwargs: _t.Any) -> str | int:
        disable = list(_E.fromcodes(kwargs.get("disable", []))) or None
        targets = list(_E.fromcodes(kwargs.get("targets", []))) or None
        kwargs["disable"] = disable
        kwargs["targets"] = targets
        return func(*args, **kwargs)

    return _wrapper


def validate_args(func: _FuncType) -> _WrappedFuncType:
    """Confirm args passed to function are valid.

    :param func: Function to wrap.
    :return: Wrapped function.
    """

    def _wrapper(*args: str | _Path, **kwargs: _t.Any) -> str | int:
        stderr = []
        if not kwargs.get("list_checks", False):
            if not args and not kwargs.get("string"):
                stderr.append(
                    "the following arguments are required: path(s) or string"
                )

            for message in kwargs.get("disable") or []:
                if not message.isknown:
                    stderr.append(
                        f"unknown option to disable '{message.description}'"
                    )

            for message in kwargs.get("targets") or []:
                if not message.isknown:
                    stderr.append(
                        f"unknown option to target '{message.description}'",
                    )

            if kwargs.get("check_class") and kwargs.get(
                "check_class_constructor"
            ):
                stderr.append(
                    "argument to check class constructor not allowed with"
                    " argument to check class"
                )
                # if we don't make it past this condition then we are
                # running this using the python interpreter
                if _sys.stdin and _sys.stdin.isatty():
                    # otherwise, it is impossible to reach here by
                    # passing both commandline args as argparse won't
                    # allow it, therefore, this must be an issue with
                    # the pyproject.toml configuration
                    stderr.append(
                        "please check your pyproject.toml configuration"
                    )

        return "\n".join(stderr) if stderr else func(*args, **kwargs)

    return _wrapper
