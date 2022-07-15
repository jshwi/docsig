"""
docsig._display
===============
"""
import typing as _t

from ._objects import MutableMapping as _MutableMapping
from ._report import Report as _Report
from ._repr import FuncStr as _FuncStr
from ._utils import color as _color

FailedDocList = _t.List[_t.Tuple[_FuncStr, int, _Report]]


class Display(_MutableMapping[str, _t.List[FailedDocList]]):
    """Collect and display report."""

    def add_failure(self, path: str, failed: FailedDocList) -> None:
        """Add report information.

        :param path: Path to file, and class if applicable.
        :param failed: Failed check information.
        """
        if path not in self:
            self[path] = []

        self[path].append(failed)

    def report(self) -> None:
        """Display report if any checks have failed."""
        for key, value in self.items():
            for failures in value:
                for func_str, lineno, report in failures:
                    header = f"{key}{lineno}"
                    _color.magenta.print(header)
                    print(len(header) * "-")
                    print(func_str)
                    print(report.get_report())
