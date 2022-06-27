"""
docsig._function
================
"""
from __future__ import annotations

import re as _re
import typing as _t

import astroid as _ast

from ._utils import get_index as _get_index


class Docstring:
    """Represents docstring parameters.

    :param func: ``ast.FunctionDef`` object from which the docstring can
        be parsed.
    """

    PARAM_KEYS = ("param", "key", "keyword", "return")

    def __init__(self, func: _ast.FunctionDef) -> None:
        self._docstring: str | None = func.doc_node
        if self._docstring is not None:
            self._docstring = func.doc_node.value.replace(4 * " ", "")

        self._is_doc = self._docstring is not None
        self._args: _t.List[_t.Tuple[str, str | None]] = []
        self._returns = False
        if self._docstring is not None:
            keys = 0
            for line in self._docstring.splitlines():
                match = _re.match(":(.*?): ", line)
                if (
                    match is not None
                    and line.startswith(match.group(0))
                    and any(
                        match.group(1).startswith(inc)
                        for inc in self.PARAM_KEYS
                    )
                ):
                    string = match.group(1).split()
                    key, value = string[0], _get_index(1, string)
                    if key == "return":
                        self._returns = True
                        continue

                    if key in ("key", "keyword"):
                        if keys == 1:
                            continue

                        keys = 1
                        value = "(**)"

                    self._args.append((key, value))

    @property
    def docstring(self) -> str | None:
        """The raw documentation string, if it exists, else None."""
        return self._docstring

    @property
    def is_doc(self) -> bool:
        """Check that docstring exists."""
        return self._is_doc

    @property
    def args(self) -> _t.Tuple[_t.Tuple[str, str | None], ...]:
        """Docstring args."""
        return tuple(self._args)

    @property
    def returns(self) -> bool:
        """Check that docstring return is documented."""
        return self._returns


class Signature:
    """Represents signature parameters.

    :param func: ``ast.FunctionDef`` object from which the params can be
        parsed.
    """

    def __init__(
        self, func: _ast.FunctionDef, method: bool = False, prop: bool = False
    ) -> None:
        self._func = func
        self._args = [
            a.name for a in self._func.args.args if not a.name.startswith("_")
        ]
        self._prop = prop
        self._returns = self._get_returns(self._func.returns)

        self._get_args_kwargs()

        if method and self._args and self._args[0] in ("self", "cls"):
            self._args.pop(0)

    def _get_args_kwargs(self) -> None:
        vararg = self._func.args.vararg
        if vararg is not None and not vararg.startswith("_"):
            self._args.append(f"*{vararg}")

        kwarg = self._func.args.kwarg
        if kwarg is not None and not kwarg.startswith("_"):
            self._args.append(f"**{kwarg}")

    def _get_returns(  # pylint: disable=too-many-return-statements
        self, returns: _ast.NodeNG | None
    ) -> str | None:
        if not self._prop:
            if isinstance(returns, _ast.Name):
                return returns.name

            if isinstance(returns, _ast.Attribute):
                return returns.attrname

            if isinstance(returns, _ast.Const):
                return returns.kind

            if isinstance(returns, _ast.Subscript):
                return "{}[{}]".format(
                    self._get_returns(returns.value),
                    self._get_returns(returns.slice),
                )

            if isinstance(returns, _ast.BinOp):
                return "{} | {}".format(
                    self._get_returns(returns.left),
                    self._get_returns(returns.right),
                )

        return None

    @property
    def args(self) -> _t.Tuple[str, ...]:
        """Tuple of signature parameters."""
        return tuple(self._args)

    @property
    def returns(self) -> str | None:
        """Return type:"""
        return self._returns


class Function:
    """Represents a function with signature and docstring parameters.

    :param func: ``ast.FunctionDef`` object from which the params can be
        parsed.
    """

    def __init__(self, func: _ast.FunctionDef, method: bool = False) -> None:
        self._name = func.name
        self._isproperty = False
        decorators = func.decorators
        if decorators is not None:
            for dec in decorators.nodes:
                if isinstance(dec, _ast.Name) and dec.name == "property":
                    self._isproperty = True

        self._signature = Signature(func, method=method, prop=self._isproperty)
        self._docstring = Docstring(func)

    @property
    def name(self) -> str:
        """The name of the function."""
        return self._name

    @property
    def isproperty(self) -> bool:
        """Boolean value determining that this func os a property."""
        return self._isproperty

    @property
    def signature(self) -> Signature:
        """The function's signature parameters."""
        return self._signature

    @property
    def docstring(self) -> Docstring:
        """The function's docstring parameters."""
        return self._docstring
