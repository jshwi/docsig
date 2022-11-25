"""
docsig._display
===============
"""
from __future__ import annotations

import typing as _t

from object_colors import Color as _Color

from ._objects import MutableMapping as _MutableMapping
from ._report import Report as _Report
from ._repr import FuncStr as _FuncStr
from ._utils import color as _color

FailedDocList = _t.List[_t.Tuple[_FuncStr, int, _Report]]


class _DisplaySequence(_MutableMapping[str, _t.List[FailedDocList]]):
    """Sequence for collection of report info.

    If an attempt is made to append a report to a list whose key does
    not exist then the key and its list value will be added first.
    """

    def __getitem__(self, key: str) -> list[FailedDocList]:
        if key not in super().__iter__():
            super().__setitem__(key, [])

        return super().__getitem__(key)


class Display(_DisplaySequence):
    """Collect and display report.

    :param no_ansi: Disable ANSI output.
    """

    def __init__(self, no_ansi: bool = False) -> None:
        super().__init__()
        self._no_ansi = no_ansi

    def _get_color(self, obj: _t.Any, color: _Color) -> str:
        string = str(obj)
        if not self._no_ansi:
            return color.get(obj)

        return string

    def report(self) -> None:
        """Display report if any checks have failed."""
        for key, value in self.items():
            for failures in value:
                for func_str, lineno, report in failures:
                    header = f"{key}{lineno}"
                    print(self._get_color(header, _color.magenta))
                    print(len(header) * "-")
                    print(func_str)
                    print(report.get_report())

    def summarise(self) -> None:
        """Display report summary if any checks have failed."""
        for key, value in self.items():
            path = key[:-2]
            print(self._get_color(path, _color.magenta))
            print(len(path) * "-")
            for failures in value:
                for _, lineno, report in failures:
                    pipe = self._get_color("|", _color.cyan)
                    print(
                        "{}\t{} {}\n".format(
                            self._get_color(lineno, _color.yellow),
                            pipe,
                            report.get_report("\t{} ".format(pipe)).strip(),
                        )
                    )
