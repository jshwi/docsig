"""
docsig._function
================
"""
from __future__ import annotations

import typing as _t

import astroid as _ast

from ._docstring import Docstring as _Docstring
from ._utils import isprotected as _isprotected


class _FunctionKind:
    """Check node for kinds of functions.

    :param node: Function's abstract syntax tree.
    """

    def __init__(self, node: _ast.FunctionDef) -> None:
        self._node = node
        self._parent = node.parent.frame()

    def _by_decorated(self, name: str) -> bool:
        decorators = self._node.decorators
        if decorators is not None:
            for dec in decorators.nodes:
                if isinstance(dec, _ast.Name) and dec.name == name:
                    return True

        return False

    @property
    def ismethod(self) -> bool:
        """Boolean value for whether function is a method."""
        return isinstance(self._parent, _ast.ClassDef)

    @property
    def isproperty(self) -> bool:
        """Boolean value for whether function is a property."""
        return self.ismethod and self._by_decorated("property")

    @property
    def isinit(self) -> bool:
        """Boolean value for whether function is a class constructor."""
        return self.ismethod and self._node.name == "__init__"

    @property
    def isoverridden(self) -> bool:
        """Boolean value for whether function is overridden."""
        if self.ismethod and not self.isinit:
            for ancestor in self._parent.ancestors():
                if self._node.name in ancestor and isinstance(
                    ancestor[self._node.name], _ast.nodes.FunctionDef
                ):
                    return True

        return False

    @property
    def isprotected(self) -> bool:
        """Boolean value for whether function is protected."""
        return (
            _isprotected(self._node.name)
            and not self.isinit
            and not self.isdunder
        )

    @property
    def isstaticmethod(self) -> bool:
        """Boolean value for whether function is a static method."""
        return self.ismethod and self._by_decorated("staticmethod")

    @property
    def isdunder(self) -> bool:
        """Boolean value for whether function is a dunder method."""
        return (
            self.ismethod
            and not self.isinit
            and self._node.name[:2] + self._node.name[-2:] == "____"
        )


class _Signature:
    """Represents signature parameters.

    :param arguments: Argument's abstract syntax tree.
    :param returns: Function's return value.
    :param kind: Kind of function.
    """

    def __init__(
        self,
        arguments: _ast.Arguments,
        returns: _ast.Module,
        kind: _FunctionKind,
    ) -> None:
        self._arguments = arguments
        self._args = [
            a.name for a in self._arguments.args if not _isprotected(a.name)
        ]
        self._return_value = self._get_returns(returns)
        self._returns = (
            self._return_value is not None and self._return_value != "None"
        )
        self._get_args_kwargs()
        if kind.ismethod and not kind.isstaticmethod and self._args:
            self._args.pop(0)

    def _get_args_kwargs(self) -> None:
        vararg = self._arguments.vararg
        if vararg is not None and not _isprotected(vararg):
            self._args.append(f"*{vararg}")

        if self._arguments.kwonlyargs:
            self._args.extend([k.name for k in self._arguments.kwonlyargs])

        kwarg = self._arguments.kwarg
        if kwarg is not None and not _isprotected(kwarg):
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
    """

    def __init__(self, node: _ast.FunctionDef) -> None:
        self._kind = _FunctionKind(node)
        self._name = node.name
        self._lineno = node.lineno or 0
        doc_node = node.doc_node
        if self._kind.isinit:
            doc_node = node.parent.frame().doc_node

        self._signature = _Signature(node.args, node.returns, self._kind)
        self._docstring = _Docstring(doc_node)

    @property
    def name(self) -> str:
        """The name of the function."""
        return self._name

    @property
    def lineno(self) -> int:
        """Line number of function declaration."""
        return self._lineno

    @property
    def kind(self) -> _FunctionKind:
        """Kind of function."""
        return self._kind

    @property
    def signature(self) -> _Signature:
        """The function's signature parameters."""
        return self._signature

    @property
    def docstring(self) -> _Docstring:
        """The function's docstring."""
        return self._docstring
