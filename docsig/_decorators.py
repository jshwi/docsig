"""
docsig._decorators
==================
"""

from __future__ import annotations as _

import functools as _functools
import sys as _sys
import typing as _t
from pathlib import Path as _Path
from warnings import warn as _warn

from ._files import Paths as _Paths
from .messages import E as _E

_FuncType = _t.Callable[..., _t.Union[int]]
_WrappedFuncType = _t.Callable[..., _t.Union[str, int]]

_DEFAULT_EXCLUDES = """\
(?x)^(
    |\\.?venv
    |\\.git
    |\\.hg
    |\\.idea
    |\\.mypy_cache
    |\\.nox
    |\\.pytest_cache
    |\\.svn
    |\\.tox
    |\\.vscode
    |_?build
    |__pycache__
    |dist
    |node_modules
)$
"""


def parse_msgs(func: _WrappedFuncType) -> _WrappedFuncType:
    """Parse error codes or symbolic messages into message objects.

    :param func: Function to wrap.
    :return: Wrapped function.
    """

    @_functools.wraps(func)
    def _wrapper(*args: str | _Path, **kwargs: _t.Any) -> str | int:
        disable = _E.from_codes(kwargs.get("disable", [])) or None
        target = _E.from_codes(kwargs.get("target", [])) or None
        kwargs["disable"] = disable
        kwargs["target"] = target
        return func(*args, **kwargs)

    return _wrapper


def handle_deprecations(func: _WrappedFuncType) -> _WrappedFuncType:
    """Allow, but warn, of deprecated arguments.

    :param func: Function to wrap.
    :return: Wrapped function.
    """

    @_functools.wraps(func)
    def _wrapper(*args: str | _Path, **kwargs: _t.Any) -> str | int:
        if kwargs.pop("summary", None):
            _warn(
                "summary is deprecated and will be removed in a future"
                " version",
                category=DeprecationWarning,
                stacklevel=4,
            )

        return func(*args, **kwargs)

    return _wrapper


def validate_args(func: _WrappedFuncType) -> _WrappedFuncType:
    """Confirm args passed to function are valid.

    :param func: Function to wrap.
    :return: Wrapped function.
    """

    @_functools.wraps(func)
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

            for message in kwargs.get("target") or []:
                if not message.isknown:
                    stderr.append(
                        f"unknown option to target '{message.description}'"
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


def collect_paths(func: _FuncType) -> _WrappedFuncType:
    """Parse paths passed to function.

    Normalises such as `.`, where the desired behaviour is to recurse,
    but also exclude paths not wanted with the exclude rule, and take
    gitignore into consideration as well.

    :param func: Function to wrap.
    :return: Wrapped function.
    """

    @_functools.wraps(func)
    def _wrapper(*args: str | _Path, **kwargs: _t.Any) -> str | int:
        exclude = kwargs.pop("exclude", None)
        excludes = [_DEFAULT_EXCLUDES]
        if exclude is not None:
            excludes.append(exclude)

        paths = _Paths(
            *tuple(_Path(i) for i in args),
            excludes=excludes,
            include_ignored=kwargs.pop("include_ignored", False),
            verbose=kwargs.get("verbose", False),
        )
        return func(*paths, **kwargs)

    return _wrapper
