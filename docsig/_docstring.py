"""
docsig._docstring
=================
"""
from __future__ import annotations

import re as _re
import textwrap as _textwrap

import astroid as _ast
from sphinxcontrib.napoleon import GoogleDocstring as _GoogleDocstring
from sphinxcontrib.napoleon import NumpyDocstring as _NumpyDocstring

from ._utils import get_index as _get_index
from ._utils import lstrip_quant as _lstrip_quant


class Docstring:
    """Represents docstring.

    :param node: Docstring's abstract syntax tree.
    """

    PARAM_KEYS = ("param", "key", "keyword", "return", "returns")

    def __init__(self, node: _ast.Const | None = None) -> None:
        self._string = None
        self._returns = False
        self._args: list[tuple[str, str | None]] = []
        if node is not None:
            string = _textwrap.dedent("\n".join(node.value.splitlines()[1:]))
            string = string.replace("*", "")
            string = "\n".join(_NumpyDocstring(string).lines())
            string = "\n".join(_GoogleDocstring(string).lines())
            self._string = string.replace(":return:", ":return: ").replace(
                ":returns:", ":returns: "
            )
            keys = 0
            for line in self._string.splitlines():
                line = _lstrip_quant(line, 4)
                match = _re.match(":(.*?): ", line)
                if (
                    match is not None
                    and line.startswith(match.group(0))
                    and any(
                        match.group(1).startswith(inc)
                        for inc in self.PARAM_KEYS
                    )
                ):
                    string_list = match.group(1).split()
                    key, value = string_list[0], _get_index(1, string_list)
                    if key in ("return", "returns"):
                        self._returns = True
                        continue

                    if key in ("key", "keyword"):
                        if keys == 1:
                            continue

                        keys = 1
                        value = "(**)"

                    self._args.append((key, value))

    @property
    def string(self) -> str | None:
        """The raw documentation string, if it exists, else None."""
        return self._string

    @property
    def args(self) -> tuple[tuple[str, str | None], ...]:
        """Docstring args."""
        return tuple(self._args)

    @property
    def returns(self) -> bool:
        """Check that docstring return is documented."""
        return self._returns
