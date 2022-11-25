"""
docsig._objects
===============
"""
from __future__ import annotations

import typing as _t

T = _t.TypeVar("T")
KT = _t.TypeVar("KT")
VT = _t.TypeVar("VT")


class MutableSequence(_t.MutableSequence[T]):
    """List-object to inherit from."""

    def __init__(self) -> None:
        self._list: list[T] = []

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


class MutableMapping(_t.MutableMapping[KT, VT]):
    """Dict-object to inherit from."""

    def __init__(self) -> None:
        self._dict: dict[KT, VT] = {}

    def __setitem__(self, __k: KT, __v: VT) -> None:
        self._dict.__setitem__(__k, __v)

    def __delitem__(self, __v: KT) -> None:
        self._dict.__delitem__(__v)

    def __getitem__(self, __k: KT) -> VT:
        return self._dict.__getitem__(__k)

    def __len__(self) -> int:
        return self._dict.__len__()

    def __iter__(self) -> _t.Iterator[KT]:
        return self._dict.__iter__()
