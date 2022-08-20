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


class _BaseDocStyle:
    PARAM_KEYS: _t.Tuple[str, ...] = tuple()

    def __init__(self):
        self._returns = False
        self._args: _t.List[_t.Tuple[str, str | None]] = []

    @property
    def args(self) -> _t.Tuple[_t.Tuple[str, str | None], ...]:
        """Docstring args."""
        return tuple(self._args)

    @property
    def returns(self) -> bool:
        """Check that docstring return is documented."""
        return self._returns


class _DocStyle(_BaseDocStyle):
    def __init__(self, string: str) -> None:
        super().__init__()
        self._string = string

    @property
    def isstyle(self) -> bool:
        """Boolean result for whether string matches this style."""
        return any(i in self._string for i in self.PARAM_KEYS)


class _SphinxStyle(_DocStyle):

    PARAM_KEYS = ("param", "key", "keyword", "return")

    def __init__(self, string: str) -> None:
        super().__init__(string)
        keys = 0
        for line in string.splitlines():
            line = _lstrip_quant(line, 4)
            match = _re.match(":(.*?): ", line)
            if (
                match is not None
                and line.startswith(match.group(0))
                and any(
                    match.group(1).startswith(inc) for inc in self.PARAM_KEYS
                )
            ):
                string_list = match.group(1).split()
                key, value = string_list[0], _get_index(1, string_list)
                if key == "return":
                    self._returns = True
                    continue

                if key in ("key", "keyword"):
                    if keys == 1:
                        continue

                    keys = 1
                    value = "(**)"

                self._args.append((key, value))


class Docstring:
    """Represents docstring.

    :param node: Docstring's abstract syntax tree.
    """

    def _get_style(self):
        sphinx_style = _SphinxStyle(self._string)
        if sphinx_style.isstyle:
            self._style = sphinx_style

    def __init__(self, node: _ast.Const | None = None) -> None:
        self._string = None
        self._returns = False
        self._args: _t.List[_t.Tuple[str, str | None]] = []
        self._style = _BaseDocStyle()
        if node is not None:
            self._string = node.value
            self._get_style()

    @property
    def string(self) -> str | None:
        """The raw documentation string, if it exists, else None."""
        return self._string

    @property
    def args(self) -> _t.Tuple[_t.Tuple[str, str | None], ...]:
        """Docstring args."""
        return tuple(self._style.args)

    @property
    def returns(self) -> bool:
        """Check that docstring return is documented."""
        return self._style.returns
