"""
docsig._utils
=============
"""
from __future__ import annotations

import typing as _t
from difflib import SequenceMatcher as _SequenceMatcher
from pathlib import Path as _Path

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


def find_pyproject_toml(path: _Path | None = None) -> _Path | None:
    """Attempt to locate a pyproject.toml file if one exists in parents.

    :param path: Path to start search, if None start with CWD.
    :return: Path to pyproject.toml if it exists, else None.
    """
    if not path:
        path = _Path.cwd()

    pyproject_toml = path / "pyproject.toml"
    if pyproject_toml.is_file():
        return pyproject_toml

    if path == _Path("/"):
        return None

    return find_pyproject_toml(path.parent)


def isprotected(name: str | None) -> bool:
    """Confirm whether attribute is protected or not.

    :param name: Name to check.
    :return: Boolean value for whether attribute is protected or not.
    """
    return str(name).startswith("_")


def almost_equal(str1: str, str2: str, mini: float, maxi: float) -> bool:
    """Show result for more than the minimum but less than the maximum.

    :param str1: String one to compare with string two.
    :param str2: String two to compare with string one.
    :param mini: Minimum difference allowed between two strings.
    :param maxi: Maximum difference allowed to be considered almost
        equal.
    :return: Boolean result for whether both strings are almost equal.
    """
    return mini < _SequenceMatcher(a=str1, b=str2).ratio() < maxi
