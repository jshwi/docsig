"""
docsig._display
===============
"""

from __future__ import annotations as _

import sys as _sys
import typing as _t
from collections import UserString as _UserString

import click as _click
from pygments import highlight as _highlight
from pygments.formatters.terminal256 import (
    Terminal256Formatter as _Terminal256Formatter,
)

# noinspection PyUnresolvedReferences
from pygments.lexers.python import PythonLexer as _PythonLexer

from ._module import Function as _Function
from ._report import Report as _Report
from ._stub import ARG as _ARG
from ._stub import KEY as _KEY
from ._stub import Param as _Param

TAB = "    "


def syntax(obj: _t.Any) -> str:
    """Get code representation with syntax highlighting.

    :param obj: Any object, represented as ``__str__``.
    :return: Colored string or string as was supplied.
    """
    return _highlight(
        obj, _PythonLexer(), _Terminal256Formatter(style="monokai")
    ).strip()


class FuncStr(_UserString):
    """String representation for function.

    :param func: Represents a function with signature and docstring
        parameters.
    """

    CHECK = "\u2713"
    CROSS = "\u2716"
    TRIPLE_QUOTES = '"""'

    def __init__(self, func: _Function) -> None:
        super().__init__(func.name)
        self._parent_name = func.parent.name
        self._isinit = func.isinit
        self.data = ""
        self._is_string = func.docstring.string is not None
        if self._isinit:
            self.data += TAB

        self.data += syntax(f"def {func.name}(")
        if self._is_string:
            self._docstring = syntax(f"{TAB}{self.TRIPLE_QUOTES}")
        else:
            self._docstring = f"{TAB}{_click.style('...', fg='red')}\n"

        self._mark = _click.style(self.CHECK, fg="green")
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
            _click.style(self.CROSS, fg="red")
            if failed
            else _click.style(self.CHECK, fg="green")
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
            self.data += f"{syntax(') -> ')}{self._mark}{arg}{syntax(':')}"
        else:
            self.data += "{}{}{}".format(
                syntax(")"),
                _click.style("?", fg="red"),
                syntax(":"),
            )

    def add_comma(self) -> None:
        """Add comma between parenthesis."""
        self.data += syntax(", ")

    def close_docstring(self) -> None:
        """Close docstring."""
        self._cat_docstring(f"\n{TAB}{syntax(self.TRIPLE_QUOTES)}\n")

    def render(self) -> None:
        """Render final string by adding docstring to function."""
        if self._isinit:
            self.data = (
                syntax(f"class {self._parent_name}:")
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


class Display(_t.Dict[str, _t.List[Failures]]):
    """Collect and display report.

    :param no_ansi: Disable ANSI output.
    """

    def __init__(self, no_ansi: bool = False) -> None:
        super().__init__()
        self._ansi = not no_ansi and _sys.stdout.isatty()

    def __getitem__(self, key: str) -> list[Failures]:
        if key not in super().__iter__():
            super().__setitem__(key, [])

        return super().__getitem__(key)

    def report(self) -> None:
        """Display report if any checks have failed."""
        for key, value in self.items():
            for failures in value:
                for failure in failures:
                    header = f"{key}{failure.func.lineno}"
                    if failure.func.parent.name:
                        header += f" in {failure.func.parent.name}"

                    _click.echo(
                        _click.style(header, fg="magenta"), color=self._ansi
                    )
                    _click.echo(len(header) * "-", color=self._ansi)
                    _click.echo(failure.func_str, color=self._ansi)
                    _click.echo(failure.report.get_report(), color=self._ansi)

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
                    _click.echo(
                        "{}\n    {}".format(
                            _click.style(header, fg="magenta"),
                            failure.report.get_report("    ").strip(),
                        ),
                        color=self._ansi,
                    )
