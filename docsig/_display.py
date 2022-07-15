"""
docsig._display
===============
"""
import typing as _t

from object_colors import Color as _Color

from ._objects import MutableMapping as _MutableMapping
from ._report import Report as _Report
from ._repr import FuncStr as _FuncStr
from ._utils import color as _color

FailedDocList = _t.List[_t.Tuple[_FuncStr, int, _Report]]


class Display(_MutableMapping[str, _t.List[FailedDocList]]):
    """Collect and display report.

    :param no_ansi: Disable ANSI output.
    """

    def __init__(self, no_ansi: bool = False) -> None:
        super().__init__()
        self._no_ansi = no_ansi

    def add_failure(self, path: str, failed: FailedDocList) -> None:
        """Add report information.

        :param path: Path to file, and class if applicable.
        :param failed: Failed check information.
        """
        if path not in self:
            self[path] = []

        self[path].append(failed)

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
