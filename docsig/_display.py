"""
docsig._display
===============
"""

from __future__ import annotations as _

import sys as _sys
import typing as _t

import click as _click

from ._module import Function as _Function
from ._report import Report as _Report


class Failure(_t.NamedTuple):
    """Failed function data."""

    func: _Function
    report: _Report


class Failures(_t.List[Failure]):
    """Sequence of failed functions."""


class Display(_t.Dict[str, _t.List[Failures]]):
    """Collect and display report."""

    def __getitem__(self, key: str) -> list[Failures]:
        if key not in super().__iter__():
            super().__setitem__(key, [])

        return super().__getitem__(key)

    def report(self, no_ansi: bool = False) -> None:
        """Display report summary if any checks have failed.

        :param no_ansi: Disable ANSI output.
        """
        for key, value in self.items():
            for failures in value:
                for failure in failures:
                    header = f"{key}{failure.func.lineno}"
                    function = failure.func.name
                    if failure.func.parent.name:
                        function = f"{failure.func.parent.name}.{function}"

                    header += f" in {function}"
                    _click.echo(
                        "{}\n    {}".format(
                            _click.style(header, fg="magenta"),
                            "\n    ".join(failure.report),
                        ),
                        color=not no_ansi and _sys.stdout.isatty(),
                    )
