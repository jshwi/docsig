"""
docsig._repr
============
"""
from __future__ import annotations

from collections import UserString as _UserString

from ._ansi import ANSI as _ANSI
from ._ansi import color as _color
from ._function import Function as _Function


class FuncStr(_UserString):
    """String representation for function.

    :param func: Represents a function with signature and docstring
        parameters.
    :param no_ansi: Disable ANSI output.
    """

    CHECK = "\u2713"
    CROSS = "\u2716"
    TRIPLE_QUOTES = '"""'
    TAB = "    "

    def __init__(self, func: _Function, no_ansi: bool = False) -> None:
        super().__init__(func.name)
        self._ansi = _ANSI(no_ansi)
        self._parent_name = func.parent_name
        self._isinit = func.kind.isinit
        self.data = ""
        if self._isinit:
            self.data += self.TAB

        self.data += self._ansi.get_syntax(f"def {func.name}(")
        self._docstring = (
            f"{self._ansi.get_syntax(f'{self.TAB}{self.TRIPLE_QUOTES}...')}\n"
        )
        self._mark = self._ansi.get_color(self.CHECK, _color.green)

    def set_mark(self, failed: bool = False) -> None:
        """Set mark to a cross or a check.

        :param failed: Boolean to test that check failed.
        """
        self._mark = (
            self._ansi.get_color(self.CROSS, _color.red)
            if failed
            else self._ansi.get_color(self.CHECK, _color.green)
        )

    def add_param(
        self, arg: str | None, doc: str | None, kind: str, failed: bool = False
    ) -> None:
        """Add parameters to docstring.

        :param arg: Signature argument.
        :param doc: Docstring argument.
        :param kind: Type of docstring parameter.
        :param failed: Boolean to test that check failed.
        """
        self.set_mark(failed)
        self.data += f"{self._mark}{arg}"
        self._docstring += f"\n{self.TAB}:{kind} {doc}: {self._mark}"

    def add_return(self, failed: bool = False) -> None:
        """Add return statement to docstring.

        :param failed: Boolean to test that check failed.
        """
        self.set_mark(failed)
        self._docstring += f"\n{self.TAB}:return: {self._mark}"

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
                self._ansi.get_color("?", _color.red),
                self._ansi.get_syntax(":"),
            )

    def add_comma(self) -> None:
        """Add comma between parenthesis."""
        self.data += self._ansi.get_syntax(", ")

    def close_docstring(self) -> None:
        """Close docstring."""
        self._docstring += (
            f"\n{self.TAB}{self._ansi.get_syntax(self.TRIPLE_QUOTES)}\n"
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
