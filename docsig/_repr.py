"""
docsig._repr
============
"""
from __future__ import annotations

from collections import UserString as _UserString

from pygments import highlight as _highlight
from pygments.formatters.terminal256 import (
    Terminal256Formatter as _Terminal256Formatter,
)

# noinspection PyUnresolvedReferences
from pygments.lexers.python import PythonLexer as _PythonLexer

from ._utils import color as _color


class FuncStr(_UserString):  # pylint: disable=too-many-instance-attributes
    """String representation for function.

    :param name: Name of the function to construct:
    :param parent_name: Name of class, if parent is a class:
    :param isinit: Boolean value for whether function is a class
        constructor or not.
    :param no_ansi: Disable ANSI output.
    """

    TRIPLE_QUOTES = '"""'
    TAB = "    "

    def __init__(
        self,
        name: str,
        parent_name: str,
        isinit: bool = False,
        no_ansi: bool = False,
    ) -> None:
        super().__init__(name)
        self._parent_name = parent_name
        self._isinit = isinit
        self._no_ansi = no_ansi
        self._check = "\u2713"
        self._cross = "\u2716"
        self._question = "?"
        if not self._no_ansi:
            self._check = _color.green.get(self._check)
            self._cross = _color.red.get(self._cross)
            self._question = _color.red.get(self._question)

        self.data = ""
        if self._isinit:
            self.data += self.TAB

        self.data += self._lexer(f"def {name}(")
        self._docstring = (
            f"{self._lexer(f'{self.TAB}{self.TRIPLE_QUOTES}...')}\n"
        )
        self._mark = self._check

    def _lexer(self, value: str) -> str:
        if self._no_ansi:
            return value

        formatter = _Terminal256Formatter(style="monokai")
        return _highlight(value, _PythonLexer(), formatter).strip()

    def set_mark(self, failed: bool = False) -> None:
        """Set mark to a cross or a check.

        :param failed: Boolean to test that check failed.
        """
        self._mark = self._cross if failed else self._check

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
                self._lexer(") -> "), self._mark, arg, self._lexer(":")
            )
        else:
            self.data += "{}{}{}".format(
                self._lexer(")"), self._question, self._lexer(":")
            )

    def add_comma(self) -> None:
        """Add comma between parenthesis."""
        self.data += self._lexer(", ")

    def close_docstring(self) -> None:
        """Close docstring."""
        self._docstring += f"\n{self.TAB}{self._lexer(self.TRIPLE_QUOTES)}\n"

    def render(self) -> None:
        """Render final string by adding docstring to function."""
        if self._isinit:
            self.data = (
                self._lexer(f"class {self._parent_name}:")
                + f"\n{self._docstring}"
                + f"\n{self.data}\n"
            )
        else:
            self.data += f"\n{self._docstring}"
