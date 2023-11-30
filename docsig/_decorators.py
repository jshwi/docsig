"""
docsig._decorators
==================
"""
from __future__ import annotations as _

import typing as _t
from pathlib import Path as _Path

from .messages import E as _E

_FuncType = _t.Callable[..., _t.Union[int]]


def parse_msgs(func: _FuncType) -> _FuncType:
    """Parse error codes or symbolic messages into message objects.

    :param func: Function to wrap.
    :return: Wrapped function.
    """

    def _wrapper(*args: str | _Path, **kwargs: _t.Any) -> int:
        disable = list(_E.fromcodes(kwargs.get("disable", []))) or None
        targets = list(_E.fromcodes(kwargs.get("targets", []))) or None
        kwargs["disable"] = disable
        kwargs["targets"] = targets
        return func(*args, **kwargs)

    return _wrapper
