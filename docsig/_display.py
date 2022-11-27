"""
docsig._display
===============
"""
from __future__ import annotations

import typing as _t

from ._ansi import ANSI as _ANSI
from ._ansi import color as _color
from ._objects import MutableMapping as _MutableMapping
from ._objects import MutableSequence as _MutableSequence
from ._report import Report as _Report
from ._repr import FuncStr as _FuncStr


class Failures(_MutableSequence[_t.Tuple[_FuncStr, int, _Report]]):
    """Sequence of failed functions."""


class _DisplaySequence(_MutableMapping[str, _t.List[Failures]]):
    """Sequence for collection of report info.

    If an attempt is made to append a report to a list whose key does
    not exist then the key and its list value will be added first.
    """

    def __getitem__(self, key: str) -> list[Failures]:
        if key not in super().__iter__():
            super().__setitem__(key, [])

        return super().__getitem__(key)


class Display(_DisplaySequence):
    """Collect and display report.

    :param no_ansi: Disable ANSI output.
    """

    def __init__(self, no_ansi: bool = False) -> None:
        super().__init__()
        self._ansi = _ANSI(no_ansi)

    def report(self) -> None:
        """Display report if any checks have failed."""
        for key, value in self.items():
            for failures in value:
                for func_str, lineno, report in failures:
                    header = f"{key}{lineno}"
                    print(self._ansi.get_color(header, _color.magenta))
                    print(len(header) * "-")
                    print(func_str)
                    print(report.get_report())

    def summarise(self) -> None:
        """Display report summary if any checks have failed."""
        for key, value in self.items():
            path = key[:-2]
            print(self._ansi.get_color(path, _color.magenta))
            print(len(path) * "-")
            for failures in value:
                for _, lineno, report in failures:
                    pipe = self._ansi.get_color("|", _color.cyan)
                    print(
                        "{}\t{} {}\n".format(
                            self._ansi.get_color(lineno, _color.yellow),
                            pipe,
                            report.get_report("\t{} ".format(pipe)).strip(),
                        )
                    )
