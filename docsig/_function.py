"""
docsig._function
================
"""
from __future__ import annotations

import astroid as _ast

from ._docstring import Docstring as _Docstring
from ._signature import Signature as _Signature
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


class Function:
    """Represents a function with signature and docstring parameters.

    :param node: Function's abstract syntax tree.
    """

    def __init__(self, node: _ast.FunctionDef) -> None:
        self._kind = _FunctionKind(node)
        self._name = node.name
        parent = node.parent.frame()
        self._parent_name = parent.name
        self._lineno = node.lineno or 0
        doc_node = node.doc_node
        if self._kind.isinit:
            doc_node = parent.doc_node

        self._signature = _Signature(
            node.args,
            node.returns,
            self._kind.ismethod,
            self._kind.isstaticmethod,
        )
        self._docstring = _Docstring(doc_node)

    @property
    def name(self) -> str:
        """The name of the function."""
        return self._name

    @property
    def parent_name(self) -> str:
        """The name of the function's parent."""
        return self._parent_name

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
