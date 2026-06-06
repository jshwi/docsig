"""
docsig._diagnostic
==================

Diagnostic records and per-function check results for docsig runs.
"""

from dataclasses import dataclass as _dataclass


class RetCode:
    """RetCode object.

    :param code: Initial return code, if any, otherwise zero.
    """

    def __init__(self, code: int = 0) -> None:
        self._data = [code]

    def add(self, code: int) -> None:
        """Add a return code.

        :param code: Return code to add.
        """
        self._data.append(code)

    @property
    def result(self) -> int:
        """Maximum return code."""
        return max(self._data)


@_dataclass(frozen=True, order=True)
class Diagnostic:  # pylint: disable=too-few-public-methods
    """Single reported issue for one function."""

    name: str
    ref: str
    description: str
    symbolic: str
    lineno: int
    hint: str | None = None
    new: bool = False
