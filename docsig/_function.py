"""
docsig._function
================
"""
from __future__ import annotations

import re as _re
import typing as _t

import astroid as _ast

from ._utils import get_index as _get_index
from ._utils import lstrip_quant as _lstrip_quant


class Docstring:
    """Represents docstring.

    :param node: Docstring's abstract syntax tree.
    """

    PARAM_KEYS = ("param", "key", "keyword", "return")

    def __init__(self, node: _ast.Const | None = None) -> None:
        self._docstring = None
        self._returns = False
        self._args: _t.List[_t.Tuple[str, str | None]] = []
        if node is not None:
            self._docstring = node.value
            keys = 0
            for line in self._docstring.splitlines():
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
    def args(self) -> _t.Tuple[_t.Tuple[str, str | None], ...]:
        """Docstring args."""
        return tuple(self._args)

    @property
    def returns(self) -> bool:
        """Check that docstring return is documented."""
        return self._returns


class Signature:
    """Represents signature parameters.

    :param arguments: Argument's abstract syntax tree.
    :param returns: Function's return value.
    :param method: Boolean for whether function is a class method.
    """

    def __init__(
        self,
        arguments: _ast.Arguments,
        returns: _ast.Module,
        method: bool = False,
    ) -> None:
        self._arguments = arguments
        self._args = [
            a.name for a in self._arguments.args if not a.name.startswith("_")
        ]
        self._return_value = self._get_returns(returns)
        self._returns = (
            self._return_value is not None and self._return_value != "None"
        )
        self._get_args_kwargs()
        if method and self._args and self._args[0] in ("self", "cls"):
            self._args.pop(0)

    def _get_args_kwargs(self) -> None:
        vararg = self._arguments.vararg
        if vararg is not None and not vararg.startswith("_"):
            self._args.append(f"*{vararg}")

        if self._arguments.kwonlyargs:
            self._args.extend([k.name for k in self._arguments.kwonlyargs])

        kwarg = self._arguments.kwarg
        if kwarg is not None and not kwarg.startswith("_"):
            self._args.append(f"**{kwarg}")

    def _get_returns(self, returns: _ast.NodeNG | None) -> str | None:
        if isinstance(returns, _ast.Name):
            return returns.name

        if isinstance(returns, _ast.Attribute):
            return returns.attrname

        if isinstance(returns, _ast.Const):
            return str(returns.kind)

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
    def return_value(self) -> str | None:
        """Function's return value.

        If a function is typed to return None, return str(None). If no
        typehint exists then return None (NoneType).
        """
        return self._return_value

    @property
    def returns(self) -> bool:
        """Check that a function returns a value."""
        return self._returns


class Function:
    """Represents a function with signature and docstring parameters.

    :param node: Function's abstract syntax tree.
    :param method: Boolean for whether function is a class method.
    """

    def __init__(self, node: _ast.FunctionDef, method: bool = False) -> None:
        self._name = node.name
        self._lineno = node.lineno or 0
        self._isproperty = False
        self._isinit = False
        doc_node = node.doc_node
        decorators = node.decorators
        if decorators is not None:
            for dec in decorators.nodes:
                if isinstance(dec, _ast.Name) and dec.name == "property":
                    self._isproperty = True

        if (
            isinstance(node.parent.frame(), _ast.ClassDef)
            and node.name == "__init__"
        ):
            self._isinit = True
            doc_node = node.parent.frame().doc_node

        self._signature = Signature(node.args, node.returns, method=method)
        self._docstring = Docstring(doc_node)

    @property
    def name(self) -> str:
        """The name of the function."""
        return self._name

    @property
    def lineno(self) -> int:
        """Line number of function declaration."""
        return self._lineno

    @property
    def isproperty(self) -> bool:
        """Boolean value determining that this func is a property."""
        return self._isproperty

    @property
    def isinit(self) -> bool:
        """Boolean value determining this as a class constructor."""
        return self._isinit

    @property
    def signature(self) -> Signature:
        """The function's signature parameters."""
        return self._signature

    @property
    def docstring(self) -> Docstring:
        """The function's docstring."""
        return self._docstring
