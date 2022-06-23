"""
docsig._objects
===============
"""
import typing as _t

T = _t.TypeVar("T")


class MutableSet(_t.MutableSet[T]):
    """Set objet to inherit from."""

    def __init__(self) -> None:
        self._set: _t.Set[T] = set()

    def add(self, value: T) -> None:
        self._set.add(value)

    def discard(self, value: T) -> None:
        self._set.discard(value)

    def __contains__(self, x: object) -> bool:
        return self._set.__contains__(x)

    def __len__(self) -> int:
        return self._set.__len__()

    def __iter__(self) -> _t.Iterator[T]:
        return self._set.__iter__()
