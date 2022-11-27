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

from ._objects import MutableSequence as _MutableSequence
from ._utils import get_index as _get_index


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


class _Matches(_MutableSequence[Param]):
    _pattern = _re.compile(":(.*?): ")

    def __init__(self, string: str) -> None:
        super().__init__()
        matches = [self._pattern.match(i) for i in string.splitlines()]
        params = [i.group(1).split() for i in matches if i is not None]
        super().extend(Param(i[0], _get_index(1, i)) for i in params)


class Docstring:
    """Represents docstring.

    :param node: Docstring's abstract syntax tree.
    """

    def __init__(self, node: _ast.Const | None = None) -> None:
        self._string = None
        self._args: list[Param] = []
        if node is not None:
            self._string = RawDocstring(node.value)
            matches = _Matches(self._string)
            for match in matches:
                keys = ("key", "keyword")
                if match.declaration == "param":
                    self._args.append(match)

                elif match.declaration in keys and not any(
                    i in y for y in self._args for i in keys
                ):
                    self._args.append(Param(match.declaration, "(**)"))

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
