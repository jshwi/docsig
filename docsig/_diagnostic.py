"""
docsig._diagnostic
==================

Diagnostic records and per-function check results for docsig runs.
"""

from __future__ import annotations as _

import typing as _t
from dataclasses import dataclass as _dataclass

from ._module import Function as _Function
from .messages import Message as _Message


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


class Collector:
    """Collect diagnostics and exit weights for one function.

    :param func: Function to collect diagnostics for.
    :param qualified_name: Qualified name (Class.method) when nested,
        else bare name.
    :param lineno: Line number of the function in the source.
    """

    def __init__(
        self,
        func: _Function,
        qualified_name: str,
        lineno: int,
    ) -> None:
        self._func = func
        self._qualified_name = qualified_name
        self._lineno = lineno
        self._diagnostics: list[Diagnostic] = []
        self._retcode = RetCode()

    def add(
        self,
        value: _Message,
        include_hint: bool = False,
        **kwargs: _t.Any,
    ) -> None:
        """Add a diagnostic message.

        :param value: Message to add.
        :param include_hint: Whether to include the hint.
        :param kwargs: Additional arguments to format the description.
        """
        self._retcode.add(int(not value.new))
        diagnostic = Diagnostic(
            self._qualified_name,
            value.ref,
            value.description.format(**kwargs),
            value.symbolic,
            self._lineno,
            value.hint if include_hint else None,
            value.new,
        )
        if (
            value not in self._func.messages
            and diagnostic not in self._diagnostics
        ):
            self._diagnostics.append(diagnostic)

    @property
    def diagnostics(self) -> list[Diagnostic]:
        """Diagnostics sorted for stable output."""
        return sorted(self._diagnostics)

    @property
    def retcode(self) -> RetCode:
        """Exit code (non-zero if any check failed)."""
        return self._retcode

    def __bool__(self) -> bool:
        return bool(self._diagnostics)


class FunctionResult:
    """Diagnostics and exit code for one checked function.

    :param name: Qualified name (Class.method) when nested, else bare
        name.
    :param lineno: Line number of the function in the source.
    :param collector: Collector for the function.
    """

    def __init__(
        self,
        name: str,
        lineno: int,
        collector: Collector,
    ) -> None:
        self._name = name
        self._lineno = lineno
        self._collector = collector

    @property
    def name(self) -> str:
        """Qualified name (Class.method) when nested, else bare name."""
        return self._name

    @property
    def lineno(self) -> int:
        """Line number of the function in the source."""
        return self._lineno

    @property
    def retcode(self) -> int:
        """Exit code (non-zero if any check failed)."""
        return self._collector.retcode.result

    def __iter__(self) -> _t.Iterator[Diagnostic]:
        return iter(self._collector.diagnostics)

    def __bool__(self) -> bool:
        return bool(self._collector)
