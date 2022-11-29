"""
docsig._params
==============
"""
from __future__ import annotations

import typing as _t

from ._objects import MutableSequence as _MutableSequence


class Param(_t.NamedTuple):
    """A tuple of param types and their names."""

    kind: str
    name: str | None
    description: str | None
    indent: int


class Params(_MutableSequence[Param]):
    """Represents collection of parameters."""

    _param = "param"
    _keys = ("key", "keyword")
    _kwarg_value = "(**)"

    def insert(self, index: int, value: Param) -> None:
        """Insert value by index.

        .. todo::
            Fix raising of E113 for this method when missing a
            docstring.
            This method should be considered overridden.

        :param index: Index of value to insert.
        :param value: Value to insert.
        """
        if value.kind == self._param:
            super().insert(index, value)

        elif value.kind in self._keys and not any(
            i in y for y in self for i in self._keys
        ):
            super().insert(
                index,
                Param(value.kind, self._kwarg_value, value.description, 0),
            )

    def get(self, index: int) -> Param:
        """Get a param.

        If the index does not exist return a `Param` with None as
        `Param.name`.

        :param index: Index of param to get.
        :return: Param belonging to the index.
        """
        try:
            return self[index]
        except IndexError:
            return Param(self._param, None, None, 0)
