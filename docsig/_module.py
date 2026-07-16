"""
docsig._module
==============

AST-backed modules, classes, and functions for docstring checking.
"""

import re as _re
import typing as _t
from pathlib import Path as _Path

import astroid as _ast

from ._config import Config as _Config
from ._directives import Comments as _Comments
from ._directives import Directives as _Directives
from ._stub import Docstring as _Docstring
from ._stub import RetType as _RetType
from ._stub import Signature as _Signature
from .messages import Messages as _Messages


class _Imports(dict[str, str]): ...


class _Overloads(dict[str, "Function"]): ...


class _Children(list[_t.Union["Parent", "Function"]]): ...


_DEFAULT_NAME = "module"


class _Walker:
    """Walk an AST body, collecting a scope's children.

    A new walker is used for each scope so that children, along with
    the overloads they merge into, are collected per scope. The one
    exception is imports, which are shared across the whole tree.

    :param directives: Directives and excluded errors per line.
    :param file: Path for this scope (or None).
    :param config: Configuration object.
    :param imports: Imports shared across the whole tree.
    """

    def __init__(
        self,
        directives: _Directives,
        file: _Path | None,
        config: _Config,
        imports: _Imports,
    ) -> None:
        self._directives = directives
        self._file = file
        self._config = config
        self._imports = imports
        self._children = _Children()
        self._overloads = _Overloads()

    @property
    def children(self) -> _Children:
        """Children collected from the walked scope."""
        return self._children

    def walk(
        self,
        node: (
            _ast.nodes.Module
            | _ast.nodes.ClassDef
            | _ast.nodes.FunctionDef
            | _ast.nodes.NodeNG
        ),
    ) -> None:
        """Collect children from the body of an AST node.

        :param node: AST node whose body to walk.
        """
        # need to keep track of `comments` as, even though they are
        # resolved in the directive object, they are needed to notify
        # the user in the case that they are invalid
        parent_comments, parent_disabled = self._directives.get(
            node.lineno or 0,
            (_Comments(), _Messages()),
        )
        if hasattr(node, "body"):
            for subnode in node.body:
                comments, disabled = self._directives.get(
                    subnode.lineno or 0,
                    (_Comments(), _Messages()),
                )

                # astroid sets lineno to the first decorator
                # inline disable on the def line is at fromlineno
                fromlineno = getattr(subnode, "fromlineno", 0)
                if (
                    isinstance(subnode, _ast.nodes.FunctionDef)
                    and fromlineno
                    and fromlineno != (subnode.lineno or 0)
                ):
                    more_comments, more_disabled = self._directives.get(
                        fromlineno,
                        (_Comments(), _Messages()),
                    )
                    comments.extend(more_comments)
                    disabled.extend(more_disabled)

                comments.extend(parent_comments)
                disabled.extend(parent_disabled)
                if isinstance(
                    subnode,
                    (_ast.nodes.Import, _ast.nodes.ImportFrom),
                ):
                    for name in subnode.names:
                        original, alias = name
                        self._imports[original] = alias or original
                elif isinstance(subnode, _ast.nodes.FunctionDef):
                    # walk the function body before constructing the
                    # function, so imports it contains are collected
                    # before decorators or the signature are resolved
                    body_walker = _Walker(
                        self._directives,
                        self._file,
                        self._config,
                        self._imports,
                    )
                    body_walker.walk(subnode)
                    func = Function(
                        subnode,
                        comments,
                        disabled,
                        self._config,
                        self._imports,
                        body_walker.children,
                    )
                    if func.isoverloaded:
                        if (
                            func.name not in self._overloads
                            or self._overloads[
                                func.name
                            ].signature.returns.type
                            == _RetType.NONE
                        ):
                            self._overloads[func.name] = func
                    else:
                        if func.name in self._overloads:
                            func.overload(
                                self._overloads[
                                    func.name
                                ].signature.returns.type,
                            )

                        self._children.append(func)
                elif isinstance(subnode, _ast.nodes.ClassDef):
                    self._children.append(
                        Parent(
                            subnode,
                            self._directives,
                            self._file,
                            self._config,
                            self._imports,
                        ),
                    )
                else:
                    self.walk(subnode)


class Parent:  # pylint: disable=too-many-instance-attributes
    """Container for functions or methods (module, class, or function).

    :param node: AST node for this scope.
    :param directives: Directives and excluded errors per line.
    :param file: Path for this scope (or None).
    :param config: Configuration object.
    :param imports: Imports in this scope.
    """

    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def __init__(
        self,
        node: _ast.nodes.Module | _ast.nodes.ClassDef | None = None,
        directives: _Directives | None = None,
        file: _Path | None = None,
        config: _Config | None = None,
        imports: _Imports | None = None,
    ) -> None:
        super().__init__()
        self._error: type[BaseException] | None = None
        self._directives = directives or _Directives()
        self._config = config or _Config()
        self._children = _Children()
        self._imports = imports or _Imports()
        if node is None:
            # an empty scope, e.g. a file that isn't really python
            self._name = _DEFAULT_NAME
        else:
            self._name = node.name
            walker = _Walker(
                self._directives,
                file,
                self._config,
                self._imports,
            )
            walker.walk(node)
            self._children = walker.children

    @classmethod
    def from_error(cls, error: type[BaseException]) -> "Parent":
        """Represent a scope which could not be parsed.

        :param error: The error which prevented parsing.
        :return: A scope with a single function carrying the error.
        """
        parent = cls()
        parent._error = error
        parent._children.append(Function.from_error(error))
        return parent

    @property
    def isprotected(self) -> bool:
        """Whether this scope is protected (name starts with _)."""
        return self._name.startswith("_")

    @property
    def error(self) -> type[BaseException] | None:
        """Unrecoverable error for this scope, if any."""
        return self._error

    @property
    def children(self) -> _Children:
        """Child scopes (functions or nested classes)."""
        return self._children


class Function:  # pylint: disable=too-many-instance-attributes
    """A callable with parsed signature and docstring for checking.

    :param node: AST node for the function (or None for error).
    :param comments: Comment directives for this function.
    :param messages: Disabled checks for this function.
    :param config: Configuration object.
    :param imports: Imports in this scope.
    :param children: Children parsed from the function body.
    """

    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def __init__(
        self,
        node: _ast.nodes.FunctionDef | None = None,
        comments: _Comments | None = None,
        messages: _Messages | None = None,
        config: _Config | None = None,
        imports: _Imports | None = None,
        children: _Children | None = None,
    ) -> None:
        self._name = node.name if node is not None else _DEFAULT_NAME
        self._comments = comments or _Comments()
        self._messages = messages or _Messages()
        self._config = config or _Config()
        self._imports = imports or _Imports()
        self._children = children or _Children()
        self._frame = None
        self._decorators = None
        self._signature = _Signature()
        self._docstring = _Docstring()
        self._lineno = 0
        self._error: type[BaseException] | None = None
        if node is not None and node.parent is not None:
            self._frame = node.parent.frame()
            self._decorators = node.decorators
            self._lineno = node.lineno
            self._signature = self._signature.from_ast(
                node,
                self._config.ignore,
                skip_bound_arg=self.ismethod and not self.isstaticmethod,
            )
            relevant_doc_node = self._select_doc_node(node)
            if relevant_doc_node is not None:
                self._docstring = self.docstring.from_ast(relevant_doc_node)

    @classmethod
    def from_error(cls, error: type[BaseException]) -> "Function":
        """Represent a module which could not be parsed.

        The report does not analyze modules or classes, it analyzes
        functions, so a module error is carried by a synthetic function
        for later inspection.

        :param error: The error which prevented parsing.
        :return: A function carrying the error.
        """
        func = cls()
        func._error = error
        return func

    def _select_doc_node(
        self,
        node: _ast.nodes.FunctionDef,
    ) -> _ast.nodes.Const | None:
        # docstring for __init__ is expected on the class docstring,
        # unless the class constructor is documented instead
        if (
            self.isinit
            and not self._config.check.class_constructor
            and self._frame is not None
            and not isinstance(self._frame, _ast.nodes.Lambda)
        ):
            return self._frame.doc_node

        return node.doc_node

    def __len__(self) -> int:
        """Length of the longest of signature args or docstring args."""
        return max(len(self.signature.args), len(self.docstring.args))

    def _decorated_with(self, name: str) -> bool:
        name = self._imports.get(name, name)
        if self._decorators is not None:
            for dec in self._decorators.nodes:
                if (isinstance(dec, _ast.nodes.Name) and dec.name == name) or (
                    isinstance(dec, _ast.nodes.Attribute)
                    and dec.attrname == name
                ):
                    return True

        return False

    @property
    def ismethod(self) -> bool:
        """Whether this function is defined in a class (method)."""
        return isinstance(self._frame, _ast.nodes.ClassDef)

    @property
    def isproperty(self) -> bool:
        """Whether this function is a property or property method."""
        valid_properties = "property", "cached_property", "setter", "deleter"
        return self.ismethod and any(
            self._decorated_with(i) for i in valid_properties
        )

    @property
    def isoverloaded(self) -> bool:
        """Whether this function is an overload (typing.overload)."""
        return self._decorated_with("overload")

    @property
    def isinit(self) -> bool:
        """Whether this function is a class constructor (__init__)."""
        return self.ismethod and self.name == "__init__"

    @property
    def isoverridden(self) -> bool:
        """Whether this function overrides a base class method."""
        if (
            self.ismethod
            and not self.isinit
            and self._frame is not None
            and isinstance(self._frame, _ast.nodes.ClassDef)
        ):
            for ancestor in self._frame.ancestors():
                if self.name in ancestor and isinstance(
                    ancestor[self.name],
                    _ast.nodes.FunctionDef,
                ):
                    return True

        return False

    @property
    def isprotected(self) -> bool:
        """Whether this function is protected."""
        return (
            self._name.startswith("_")
            and not self.isinit
            and not self.isdunder
        )

    @property
    def error(self) -> type[BaseException] | None:
        """Unrecoverable error for this function, if any."""
        return self._error

    @property
    def children(self) -> _Children:
        """Functions or classes parsed from the function body."""
        return self._children

    @property
    def isstaticmethod(self) -> bool:
        """Whether this function is a static method."""
        return self.ismethod and self._decorated_with("staticmethod")

    @property
    def isdunder(self) -> bool:
        """Whether this function is a dunder method."""
        return (
            self.ismethod
            and not self.isinit
            and bool(_re.match(r"__(.*)__", self.name))
        )

    @property
    def name(self) -> str:
        """The name of the function."""
        return self._name

    @property
    def frame(
        self,
    ) -> (
        _ast.nodes.FunctionDef
        | _ast.nodes.Module
        | _ast.nodes.ClassDef
        | _ast.nodes.Lambda
        | None
    ):
        """Astroid frame node enclosing this function."""
        return self._frame

    @property
    def lineno(self) -> int:
        """Line number of function declaration."""
        return self._lineno or 0

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
        """Disabled checks for this function."""
        return self._messages

    @property
    def comments(self) -> _Comments:
        """Comment directives for this function."""
        return self._comments

    def overload(self, rettype: _RetType) -> None:
        """Merge an overload return type into this function's signature.

        :param rettype: Return type of the overloaded variant.
        """
        self._signature.overload(rettype)
