"""
docsig._display
===============
"""
from __future__ import annotations as _

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
from ._report import Report as _Report

color = _Color()

color.populate_colors()

TAB = "    "


class _ANSI:
    def __init__(self, no_ansi: bool = False) -> None:
        self._no_ansi = no_ansi

    def color(self, obj: _t.Any, color_obj: _Color) -> str:
        """Get string with selected color.

        :param obj: Any object, represented as ``__str__``.
        :param color_obj: Instantiated ``Color`` object.
        :return: Colored string or string as was supplied.
        """
        return str(obj) if self._no_ansi else color_obj.get(obj)

    def syntax(self, obj: _t.Any) -> str:
        """Get code representation with syntax highlighting.

        :param obj: Any object, represented as ``__str__``.
        :return: Colored string or string as was supplied.
        """
        return (
            str(obj)
            if self._no_ansi
            else _highlight(
                obj, _PythonLexer(), _Terminal256Formatter(style="monokai")
            ).strip()
        )


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

        self.data += self._ansi.syntax(f"def {func.name}(")
        if self._is_string:
            self._docstring = self._ansi.syntax(f"{TAB}{self.TRIPLE_QUOTES}")
        else:
            self._docstring = f"{TAB}{self._ansi.color('...', color.red)}\n"

        self._mark = self._ansi.color(self.CHECK, color.green)
        for index in range(len(func)):
            arg = func.signature.args.get(index)
            doc = func.docstring.args.get(index)
            self.add_param(arg, doc, arg != doc)
            if index + 1 != len(func):
                self.add_comma()

        self.set_mark()
        if func.docstring.returns and func.signature.returns:
            self.add_return()
        elif (
            func.docstring.returns
            and not func.signature.returns
            or func.signature.returns
            and not func.docstring.returns
        ):
            self.add_return(failed=True)

        self.close_sig(func.signature.rettype)
        self.close_docstring()
        self.render()

    def _cat_docstring(self, string: str) -> None:
        if self._is_string:
            self._docstring += string

    def set_mark(self, failed: bool = False) -> None:
        """Set mark to a cross or a check.

        :param failed: Boolean to test that check failed.
        """
        self._mark = (
            self._ansi.color(self.CROSS, color.red)
            if failed
            else self._ansi.color(self.CHECK, color.green)
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
                self._ansi.syntax(") -> "),
                self._mark,
                arg,
                self._ansi.syntax(":"),
            )
        else:
            self.data += "{}{}{}".format(
                self._ansi.syntax(")"),
                self._ansi.color("?", color.red),
                self._ansi.syntax(":"),
            )

    def add_comma(self) -> None:
        """Add comma between parenthesis."""
        self.data += self._ansi.syntax(", ")

    def close_docstring(self) -> None:
        """Close docstring."""
        self._cat_docstring(
            f"\n{TAB}{self._ansi.syntax(self.TRIPLE_QUOTES)}\n"
        )

    def render(self) -> None:
        """Render final string by adding docstring to function."""
        if self._isinit:
            self.data = (
                self._ansi.syntax(f"class {self._parent_name}:")
                + f"\n{self._docstring}"
                + f"\n{self.data}\n"
            )
        else:
            self.data += f"\n{self._docstring}"


class Failure(_t.NamedTuple):
    """Failed function data."""

    func: _Function
    func_str: FuncStr
    report: _Report


class Failures(_t.List[Failure]):
    """Sequence of failed functions."""


class _DisplaySequence(_t.Dict[str, _t.List[Failures]]):
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
                for failure in failures:
                    header = f"{key}{failure.func.lineno}"
                    if failure.func.parent.name:
                        header += f" in {failure.func.parent.name}"

                    print(self._ansi.color(header, color.magenta))
                    print(len(header) * "-")
                    print(failure.func_str)
                    print(failure.report.get_report())

    def summarise(self) -> None:
        """Display report summary if any checks have failed."""
        for key, value in self.items():
            for failures in value:
                for failure in failures:
                    header = f"{key}{failure.func.lineno}"
                    function = failure.func.name
                    if failure.func.parent.name:
                        function = f"{failure.func.parent.name}.{function}"

                    header += f" in {function}"
                    print(
                        "{}\n\t{}".format(
                            self._ansi.color(header, color.magenta),
                            failure.report.get_report("\t").strip(),
                        )
                    )
