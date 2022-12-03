"""
docsig._display
===============
"""
from __future__ import annotations

import typing as _t
from collections import UserString as _UserString

from object_colors import Color as _Color
from pygments import highlight as _highlight
from pygments.formatters.terminal256 import (
    Terminal256Formatter as _Terminal256Formatter,
)

# noinspection PyUnresolvedReferences
from pygments.lexers.python import PythonLexer as _PythonLexer

from ._function import ARG as _ARG
from ._function import KEY as _KEY
from ._function import Function as _Function
from ._function import Param as _Param
from ._objects import MutableMapping as _MutableMapping
from ._objects import MutableSequence as _MutableSequence
from ._report import Report as _Report

color = _Color()

color.populate_colors()

TAB = "    "


class _ANSI:
    def __init__(self, no_ansi: bool = False) -> None:
        self._no_ansi = no_ansi

    def get_color(self, obj: _t.Any, color_obj: _Color) -> str:
        """Get string with selected color.

        :param obj: Any object, represented as ``__str__``.
        :param color_obj: Instantiated ``Color`` object.
        :return: Colored string or string as was supplied.
        """
        string = str(obj)
        if self._no_ansi:
            return string

        return color_obj.get(obj)

    def get_syntax(self, obj: _t.Any) -> str:
        """Get code representation with syntax highlighting.

        :param obj: Any object, represented as ``__str__``.
        :return: Colored string or string as was supplied.
        """
        string = str(obj)
        if self._no_ansi:
            return string

        formatter = _Terminal256Formatter(style="monokai")
        return _highlight(string, _PythonLexer(), formatter).strip()


class FuncStr(_UserString):
    """String representation for function.

    :param func: Represents a function with signature and docstring
        parameters.
    :param no_ansi: Disable ANSI output.
    """

    CHECK = "\u2713"
    CROSS = "\u2716"
    TRIPLE_QUOTES = '"""'

    def __init__(self, func: _Function, no_ansi: bool = False) -> None:
        super().__init__(func.name)
        self._ansi = _ANSI(no_ansi)
        self._parent_name = func.parent.name
        self._isinit = func.isinit
        self.data = ""
        self._is_string = func.docstring.string is not None
        if self._isinit:
            self.data += TAB

        self.data += self._ansi.get_syntax(f"def {func.name}(")
        if self._is_string:
            self._docstring = self._ansi.get_syntax(
                f"{TAB}{self.TRIPLE_QUOTES}"
            )
        else:
            self._docstring = "{}{}\n".format(
                TAB, self._ansi.get_color("...", color.red)
            )

        self._mark = self._ansi.get_color(self.CHECK, color.green)

    def _cat_docstring(self, string: str) -> None:
        if self._is_string:
            self._docstring += string

    def set_mark(self, failed: bool = False) -> None:
        """Set mark to a cross or a check.

        :param failed: Boolean to test that check failed.
        """
        self._mark = (
            self._ansi.get_color(self.CROSS, color.red)
            if failed
            else self._ansi.get_color(self.CHECK, color.green)
        )

    def add_param(
        self, sig: _Param, doc: _Param, failed: bool = False
    ) -> None:
        """Add parameters to docstring.

        :param sig: Signature argument.
        :param doc: Docstring argument.
        :param failed: Boolean to test that check failed.
        """
        self.set_mark(failed)
        sig_name = sig.name
        if sig.kind == _KEY:
            sig_name = f"**{sig_name}"

        if sig.kind == _ARG:
            sig_name = f"*{sig_name}"

        self.data += f"{self._mark}{sig_name}"
        doc_name = doc.name
        if doc.kind == _KEY:
            doc_name = "(**)"

        self._cat_docstring(f"\n{TAB}:{doc.kind} {doc_name}: {self._mark}")

    def add_return(self, failed: bool = False) -> None:
        """Add return statement to docstring.

        :param failed: Boolean to test that check failed.
        """
        self.set_mark(failed)
        self._cat_docstring(f"\n{TAB}:return: {self._mark}")

    def close_sig(self, arg: str | None) -> None:
        """Close function signature.

        :param arg: Signature argument.
        """
        if arg is not None:
            self.data += "{}{}{}{}".format(
                self._ansi.get_syntax(") -> "),
                self._mark,
                arg,
                self._ansi.get_syntax(":"),
            )
        else:
            self.data += "{}{}{}".format(
                self._ansi.get_syntax(")"),
                self._ansi.get_color("?", color.red),
                self._ansi.get_syntax(":"),
            )

    def add_comma(self) -> None:
        """Add comma between parenthesis."""
        self.data += self._ansi.get_syntax(", ")

    def close_docstring(self) -> None:
        """Close docstring."""
        self._cat_docstring(
            f"\n{TAB}{self._ansi.get_syntax(self.TRIPLE_QUOTES)}\n"
        )

    def render(self) -> None:
        """Render final string by adding docstring to function."""
        if self._isinit:
            self.data = (
                self._ansi.get_syntax(f"class {self._parent_name}:")
                + f"\n{self._docstring}"
                + f"\n{self.data}\n"
            )
        else:
            self.data += f"\n{self._docstring}"


class Failures(_MutableSequence[_t.Tuple[FuncStr, int, _Report]]):
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
                    print(self._ansi.get_color(header, color.magenta))
                    print(len(header) * "-")
                    print(func_str)
                    print(report.get_report())

    def summarise(self) -> None:
        """Display report summary if any checks have failed."""
        for key, value in self.items():
            path = key[:-2]
            print(self._ansi.get_color(path, color.magenta))
            print(len(path) * "-")
            for failures in value:
                for _, lineno, report in failures:
                    pipe = self._ansi.get_color("|", color.cyan)
                    print(
                        "{}\t{} {}\n".format(
                            self._ansi.get_color(lineno, color.yellow),
                            pipe,
                            report.get_report("\t{} ".format(pipe)).strip(),
                        )
                    )
