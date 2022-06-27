"""
docsig._utils
=============
"""
from __future__ import annotations

import typing as _t

from object_colors import Color as _Color

from ._objects import T as _T

color = _Color()

color.populate_colors()


def get_index(index: int, seq: _t.Sequence[_T]) -> _T | None:
    """Get index without throwing an error if index does not exist.

    :param index: Index to get.
    :param seq: Sequence object that can be indexed.
    :return: Item from index else None.
    """
    try:
        return seq[index]
    except IndexError:
        return None


def lstrip_quant(string: str, quant: int) -> str:
    """Strip leading whitespace by the number of occurrences provided.

    :param string: String to strip leading whitespace from.
    :param quant: Quantity of whitespace needed to be trimmed.
    :return: Altered string.
    """
    while string.startswith(quant * " "):
        string = string[4:]

    return string
