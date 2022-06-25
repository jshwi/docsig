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


class FuncStr(_UserString):
    """String representation for function.

    :param name: Name of the function to construct:
    """

    CHECK = _color.green.get("\u2713")
    CROSS = _color.red.get("\u2716")
    TRIPLE_QUOTES = '"""'
    TAB = "    "

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.data = self._lexer(f"def {name}(")
        self._docstring = (
            f"{self._lexer(f'{self.TAB}{self.TRIPLE_QUOTES}...')}\n"
        )
        self._mark = self.CHECK

    @staticmethod
    def _lexer(value: str) -> str:
        formatter = _Terminal256Formatter(style="monokai")
        return _highlight(value, _PythonLexer(), formatter).strip()

    def set_mark(self, failed: bool = False) -> None:
        """Set mark to a cross or a check.

        :param failed: Boolean to test that check failed.
        """
        self._mark = self.CROSS if failed else self.CHECK

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
        self.data += "{}{}{}{}".format(
            self._lexer(") -> "), self._mark, arg, self._lexer(":")
        )

    def add_comma(self) -> None:
        """Add comma between parenthesis."""
        self.data += self._lexer(", ")

    def close_docstring(self) -> None:
        """Close docstring."""
        self._docstring += f"\n{self.TAB}{self._lexer(self.TRIPLE_QUOTES)}\n"

    def render(self) -> None:
        """Render final string by adding docstring to function."""
        self.data += f"\n{self._docstring}"
