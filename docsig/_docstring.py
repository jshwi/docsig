"""
docsig._docstring
=================
"""
from __future__ import annotations

import re as _re
import textwrap as _textwrap
import typing as _t

import astroid as _ast
import sphinxcontrib.napoleon as _s

from ._utils import get_index as _get_index
from ._utils import lstrip_quant as _lstrip_quant


class Param(_t.NamedTuple):
    """A tuple of param declarations and descriptions."""

    declaration: str
    description: str | None


class _GoogleDocstring(str):
    def __new__(cls, string: str) -> _GoogleDocstring:
        return super().__new__(cls, str(_s.GoogleDocstring(string)))


class _NumpyDocstring(str):
    def __new__(cls, string: str) -> _NumpyDocstring:
        return super().__new__(cls, str(_s.NumpyDocstring(string)))


class _DocFmt(str):
    def __new__(cls, string: str) -> _DocFmt:
        return super().__new__(
            cls,
            _textwrap.dedent("\n".join(string.splitlines()[1:])).replace(
                "*", ""
            ),
        )


class RawDocstring(str):
    """Instantiate a `Sphinx` docstring from available types."""

    def __new__(cls, string: str) -> RawDocstring:
        return super().__new__(
            cls, _NumpyDocstring(_GoogleDocstring(_DocFmt(string)))
        )


class Docstring:
    """Represents docstring.

    :param node: Docstring's abstract syntax tree.
    """

    PARAM_KEYS = ("param", "key", "keyword", "return", "returns")

    def __init__(self, node: _ast.Const | None = None) -> None:
        self._string = None
        self._args: list[Param] = []
        if node is not None:
            self._string = RawDocstring(node.value)
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
                    string_list = match.group(1).split()
                    key, value = string_list[0], _get_index(1, string_list)
                    if key in ("return", "returns"):
                        continue

                    if key in ("key", "keyword"):
                        if keys == 1:
                            continue

                        keys = 1
                        value = "(**)"

                    self._args.append(Param(key, value))

    @property
    def string(self) -> RawDocstring | None:
        """The raw documentation string, if it exists, else None."""
        return self._string

    @property
    def args(self) -> tuple[Param, ...]:
        """Docstring args."""
        return tuple(self._args)

    @property
    def returns(self) -> bool:
        """Check that docstring return is documented."""
        return (
            False
            if self._string is None
            else any(i in self._string for i in (":return:", ":returns:"))
        )
