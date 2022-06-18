"""
docsig._objects
===============
"""
import typing as _t

_T = _t.TypeVar("_T")


class MutableSet(_t.MutableSet[_T]):
    """Set objet to inherit from."""

    def __init__(self) -> None:
        self._set: _t.Set[_T] = set()

    def add(self, value: _T) -> None:
        self._set.add(value)

    def discard(self, value: _T) -> None:
        self._set.discard(value)

    def __contains__(self, x: object) -> bool:
        return self._set.__contains__(x)

    def __len__(self) -> int:
        return self._set.__len__()

    def __iter__(self) -> _t.Iterator[_T]:
        return self._set.__iter__()
