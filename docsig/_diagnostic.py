"""
docsig._diagnostic
==================

Diagnostic records and per-function check results for docsig runs.
"""

from dataclasses import dataclass as _dataclass


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
