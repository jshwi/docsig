"""
docsig._docstring
=================
"""

from __future__ import annotations

import re as _re
import typing as _t

import astroid as _ast

from ._utils import get_index as _get_index
from ._utils import lstrip_quant as _lstrip_quant


class Docstring:
    """Represents docstring.

    :param node: Docstring's abstract syntax tree.
    """

    PARAM_KEYS = ("param", "key", "keyword", "return")

    def __init__(self, node: _ast.Const | None = None) -> None:
        self._string = None
        self._returns = False
        self._args: _t.List[_t.Tuple[str, str | None]] = []
        if node is not None:
            self._string = node.value
            keys = 0
            for line in self._string.splitlines():
                line = _lstrip_quant(line, 4)
                match = _re.match(":(.*?): ", line)
                if (
                    match is not None
                    and line.startswith(match.group(0))
                    and any(
                        match.group(1).startswith(inc)
                        for inc in self.PARAM_KEYS
                    )
                ):
                    string = match.group(1).split()
                    key, value = string[0], _get_index(1, string)
                    if key == "return":
                        self._returns = True
                        continue

                    if key in ("key", "keyword"):
                        if keys == 1:
                            continue

                        keys = 1
                        value = "(**)"

                    self._args.append((key, value))

    @property
    def string(self) -> str | None:
        """The raw documentation string, if it exists, else None."""
        return self._string

    @property
    def args(self) -> _t.Tuple[_t.Tuple[str, str | None], ...]:
        """Docstring args."""
        return tuple(self._args)

    @property
    def returns(self) -> bool:
        """Check that docstring return is documented."""
        return self._returns
