"""
docsig._module
==============
"""

from __future__ import annotations as _

import re as _re
import typing as _t
from pathlib import Path as _Path

import astroid as _ast

from ._directives import Comment as _Comment
from ._directives import Directives as _Directives
from ._stub import Docstring as _Docstring
from ._stub import RetType as _RetType
from ._stub import Signature as _Signature
from .messages import Messages as _Messages


class Parent(_t.List["Parent"]):
    """Represents an object that contains functions or methods.

    :param node: Parent's abstract syntax tree.
    :param directives: Data for directives and, subsequently, total of
        errors which are excluded from function checks.
    :param path: Path to base path representation on.
    :param ignore_args: Ignore args prefixed with an asterisk.
    :param ignore_kwargs: Ignore kwargs prefixed with two asterisks.
    :param check_class_constructor: Check the class constructor's
        docstring. Otherwise, expect the constructor's documentation to
        be on the class level docstring.
    :param imports: Imports within this scope.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        node: _ast.Module | _ast.ClassDef | _ast.FunctionDef,
        directives: _Directives,
        path: _Path | None = None,
        ignore_args: bool = False,
        ignore_kwargs: bool = False,
        check_class_constructor: bool = False,
        imports: dict[str, str] | None = None,
    ) -> None:
        super().__init__()
        self._name = node.name
        self._overloads: dict[str, Function] = {}
        self._imports = imports or {}
        self._parse_ast(
            node,
            directives,
            path,
            ignore_args,
            ignore_kwargs,
            check_class_constructor,
        )

    def _parse_imports(self, names: list[tuple[str, str | None]]) -> None:
        for name in names:
            original, alias = name
            self._imports[original] = alias or original

    def _parse_ast(  # pylint: disable=protected-access,too-many-arguments
        self,
        node,
        directives,
        path,
        ignore_args,
        ignore_kwargs,
        check_class_constructor,
    ) -> None:
        # need to keep track of `comments` as, even though they are
        # resolved in directives object, they are needed to notify user
        # in the case that they are invalid
        parent_comments, parent_disabled = directives.get(
            node.lineno, ([], [])
        )
        if hasattr(node, "body"):
            for subnode in node.body:
                comments, disabled = directives.get(subnode.lineno, ([], []))
                comments.extend(parent_comments)
                disabled.extend(parent_disabled)
                if isinstance(subnode, (_ast.Import, _ast.ImportFrom)):
                    self._parse_imports(subnode.names)
                elif isinstance(subnode, _ast.FunctionDef):
                    func = Function(
                        subnode,
                        comments,
                        directives,
                        disabled,
                        path,
                        ignore_args,
                        ignore_kwargs,
                        check_class_constructor,
                        self._imports,
                    )
                    if func.isoverloaded:
                        if (
                            func.name not in self._overloads
                            or self._overloads[func.name].signature.rettype
                            == _RetType.NONE
                        ):
                            self._overloads[func.name] = func
                    else:
                        if func.name in self._overloads:
                            func.overload(
                                self._overloads[func.name].signature.rettype
                            )

                        self.append(func)
                elif isinstance(subnode, _ast.ClassDef):
                    self.append(
                        Parent(
                            subnode,
                            directives,
                            path,
                            ignore_args,
                            ignore_kwargs,
                            check_class_constructor,
                            self._imports,
                        )
                    )
                else:
                    self._parse_ast(
                        subnode,
                        directives,
                        path,
                        ignore_args,
                        ignore_kwargs,
                        check_class_constructor,
                    )

    @property
    def isprotected(self) -> bool:
        """Boolean value for whether class is protected."""
        return self._name.startswith("_")


class Function(Parent):
    """Represents a function with signature and docstring parameters.

    :param node: Function's abstract syntax tree.
    :param comments: Comments in list form containing directives.
    :param directives: Directive, if any, belonging to this function.
    :param messages: List of disabled checks specific to this function.
    :param path: Path to base path representation on.
    :param ignore_args: Ignore args prefixed with an asterisk.
    :param ignore_kwargs: Ignore kwargs prefixed with two asterisks.
    :param check_class_constructor: If the function is the class
        constructor, use its own docstring. Otherwise, use the class
        level docstring for the constructor function.
    :param imports: Imports within this scope.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        node: _ast.FunctionDef,
        comments: list[_Comment],
        directives: _Directives,
        messages: _Messages,
        path: _Path | None = None,
        ignore_args: bool = False,
        ignore_kwargs: bool = False,
        check_class_constructor: bool = False,
        imports: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            node,
            directives,
            path,
            ignore_args,
            ignore_kwargs,
            check_class_constructor,
            imports,
        )
        self._node = node
        self._comments = comments
        self._messages = messages
        self._parent = node.parent.frame()
        self._signature = _Signature(
            node.args,
            node.returns,
            self.ismethod,
            self.isstaticmethod,
            ignore_args,
            ignore_kwargs,
        )
        if self.isinit and not check_class_constructor:
            # docstring for __init__ is expected on the class docstring
            relevant_doc_node = self._parent.doc_node
        else:
            relevant_doc_node = node.doc_node
        self._docstring = _Docstring(relevant_doc_node, ignore_kwargs)

    def __len__(self) -> int:
        """Length of the longest sequence of args."""
        return max([len(self.signature.args), len(self.docstring.args)])

    def _decorated_with(self, name: str) -> bool:
        name = self._imports.get(name, name)
        if self._node.decorators is not None:
            for dec in self._node.decorators.nodes:
                return (isinstance(dec, _ast.Name) and dec.name == name) or (
                    isinstance(dec, _ast.Attribute) and dec.attrname == name
                )

        return False

    @property
    def ismethod(self) -> bool:
        """Boolean value for whether function is a method."""
        return isinstance(self._parent, _ast.ClassDef)

    @property
    def isproperty(self) -> bool:
        """Boolean value for whether function is a property."""
        valid_properties = [
            "property",
            "cached_property",
        ]
        return self.ismethod and any(
            self._decorated_with(i) for i in valid_properties
        )

    @property
    def isoverloaded(self) -> bool:
        """Boolean value for whether function is a property."""
        return self._decorated_with("overload")

    @property
    def isinit(self) -> bool:
        """Boolean value for whether function is a class constructor."""
        return self.ismethod and self.name == "__init__"

    @property
    def isoverridden(self) -> bool:
        """Boolean value for whether function is overridden."""
        if self.ismethod and not self.isinit:
            for ancestor in self._parent.ancestors():
                if self.name in ancestor and isinstance(
                    ancestor[self.name], _ast.FunctionDef
                ):
                    return True

        return False

    @property
    def isprotected(self) -> bool:
        """Boolean value for whether function is protected."""
        return super().isprotected and not self.isinit and not self.isdunder

    @property
    def isstaticmethod(self) -> bool:
        """Boolean value for whether function is a static method."""
        return self.ismethod and self._decorated_with("staticmethod")

    @property
    def isdunder(self) -> bool:
        """Boolean value for whether function is a dunder method."""
        return (
            self.ismethod
            and not self.isinit
            and bool(_re.match(r"__(.*)__", self.name))
        )

    @property
    def name(self) -> str:
        """The name of the function."""
        return self._node.name

    @property
    def parent(
        self,
    ) -> _ast.FunctionDef | _ast.Module | _ast.ClassDef | _ast.Lambda:
        """Function's parent node."""
        return self._parent

    @property
    def lineno(self) -> int:
        """Line number of function declaration."""
        return self._node.lineno or 0

    @property
    def signature(self) -> _Signature:
        """The function's signature parameters."""
        return self._signature

    @property
    def docstring(self) -> _Docstring:
        """The function's docstring."""
        return self._docstring

    @property
    def messages(self) -> _Messages:
        """List of disabled checks specific to this function."""
        return self._messages

    @property
    def comments(self) -> list[_Comment]:
        """Comments, if any, belonging to this function."""
        return self._comments

    def overload(self, rettype: _RetType) -> None:
        """Overload function with new signature return type.

        :param rettype: Return type of overloaded signature.
        """
        self._signature.overload(rettype)
