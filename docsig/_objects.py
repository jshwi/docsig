"""
docsig._objects
===============
"""
from __future__ import annotations

import typing as _t

T = _t.TypeVar("T")


class MutableSequence(_t.MutableSequence[T]):
    """List-object to inherit from.

    :param iterable: Initial iterable to to construct sequence with.
    """

    def __init__(self, iterable: _t.Iterable[T] = ()) -> None:
        self._list: list[T] = []
        self.extend(iterable)

    def insert(self, index: int, value: T) -> None:
        self._list.insert(index, value)

    @_t.overload
    def __getitem__(self, i: int) -> T:
        ...

    @_t.overload
    def __getitem__(self, s: slice) -> _t.MutableSequence[T]:
        ...

    def __getitem__(self, i):
        return self._list.__getitem__(i)

    @_t.overload
    def __setitem__(self, i: int, o: T) -> None:
        ...

    @_t.overload
    def __setitem__(self, s: slice, o: _t.Iterable[T]) -> None:
        ...

    def __setitem__(self, i, o):
        return self._list.__setitem__(i, o)

    @_t.overload
    def __delitem__(self, i: int) -> None:
        ...

    @_t.overload
    def __delitem__(self, i: slice) -> None:
        ...

    def __delitem__(self, i):
        return self._list.__delitem__(i)

    def __len__(self):
        return self._list.__len__()
