"""
docsig._docstring
=================
"""

from __future__ import annotations

import re as _re
import typing as _t

import astroid as _ast

from ._utils import get_index as _get_index
from ._utils import lstrip_quant as _lstrip_quant


class _BaseDocStyle:
    PARAM_KEYS: _t.Tuple[str, ...] = tuple()

    def __init__(self):
        self._returns = False
        self._args: _t.List[_t.Tuple[str, str | None]] = []

    @property
    def args(self) -> _t.Tuple[_t.Tuple[str, str | None], ...]:
        """Docstring args."""
        return tuple(self._args)

    @property
    def returns(self) -> bool:
        """Check that docstring return is documented."""
        return self._returns


class _DocStyle(_BaseDocStyle):
    def __init__(self, string: str) -> None:
        super().__init__()
        self._string = string

    @property
    def isstyle(self) -> bool:
        """Boolean result for whether string matches this style."""
        return any(i in self._string for i in self.PARAM_KEYS)


class _SphinxStyle(_DocStyle):

    PARAM_KEYS = ("param", "key", "keyword", "return")

    def __init__(self, string: str) -> None:
        super().__init__(string)
        keys = 0
        for line in string.splitlines():
            line = _lstrip_quant(line, 4)
            match = _re.match(":(.*?): ", line)
            if (
                match is not None
                and line.startswith(match.group(0))
                and any(
                    match.group(1).startswith(inc) for inc in self.PARAM_KEYS
                )
            ):
                string_list = match.group(1).split()
                key, value = string_list[0], _get_index(1, string_list)
                if key == "return":
                    self._returns = True
                    continue

                if key in ("key", "keyword"):
                    if keys == 1:
                        continue

                    keys = 1
                    value = "(**)"

                self._args.append((key, value))


class _NumpyStyle(_DocStyle):
    TAB = "    "
    PARAM_KEYS = ("Parameters", "**kwargs", "Returns")
    PARAM_UL = tuple(len(i) * "-" for i in PARAM_KEYS)

    def _populate_args(self, line, stripped_line):
        if self.PARAM_KEYS[0] in stripped_line:
            self._in_params = 1

        elif self._in_params == 1 and stripped_line == self.PARAM_UL[0]:
            self._in_params = 2

        elif self._in_params == 2:
            if not line.startswith(self.TAB):
                self._in_params = 0
            else:
                match = _re.match("(.*?) : ", stripped_line)
                if match is not None and stripped_line.startswith(
                    match.group(0)
                ):
                    string_list = match.group(1).split()
                    key, value = "param", string_list[0]
                    self._args.append((key, value))

    def _populate_kwargs(self, line, stripped_line):
        if self.PARAM_KEYS[1] in stripped_line:
            self._in_kwargs = 1

        elif self._in_kwargs == 1:
            if not line.startswith(self.TAB):
                self._in_kwargs = 0
            elif not self._got_kwargs:
                self._got_kwargs = True
                self._args.append(("keyword", "(**)"))

    def _populate_returns(self, stripped_line):
        if self.PARAM_KEYS[2] in stripped_line:
            self._in_returns = 1

        elif self._in_returns == 1 and stripped_line == self.PARAM_UL[2]:
            self._in_returns = 2

        elif self._in_returns == 2:
            self._in_returns = 3

        elif self._in_returns == 3:
            self._returns = True

    def __init__(self, string: str) -> None:
        super().__init__(string)
        self._in_params = 0
        self._in_kwargs = 0
        self._in_returns = 0
        self._got_kwargs = False
        for line in string.splitlines():
            stripped_line = _lstrip_quant(line, 4)
            self._populate_args(line, stripped_line)
            self._populate_kwargs(line, stripped_line)
            self._populate_returns(stripped_line)

    @property
    def isstyle(self) -> bool:
        """Boolean result for whether string matches this style."""
        return super().isstyle and any(
            i in self._string for i in self.PARAM_UL
        )


class Docstring:
    """Represents docstring.

    :param node: Docstring's abstract syntax tree.
    """

    def _get_style(self):
        sphinx_style = _SphinxStyle(self._string)
        numpy_style = _NumpyStyle(self._string)
        if numpy_style.isstyle:
            self._style = numpy_style

        elif sphinx_style.isstyle:
            self._style = sphinx_style

    def __init__(self, node: _ast.Const | None = None) -> None:
        self._string = None
        self._returns = False
        self._args: _t.List[_t.Tuple[str, str | None]] = []
        self._style = _BaseDocStyle()
        if node is not None:
            self._string = node.value
            self._get_style()

    @property
    def string(self) -> str | None:
        """The raw documentation string, if it exists, else None."""
        return self._string

    @property
    def args(self) -> _t.Tuple[_t.Tuple[str, str | None], ...]:
        """Docstring args."""
        return tuple(self._style.args)

    @property
    def returns(self) -> bool:
        """Check that docstring return is documented."""
        return self._style.returns
