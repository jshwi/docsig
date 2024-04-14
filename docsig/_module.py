"""
docsig._module
==============
"""

from __future__ import annotations as _

import re as _re
import typing as _t
from pathlib import Path as _Path

import astroid as _ast
from astroid import AstroidSyntaxError as _AstroidSyntaxError

from ._directives import Directive as _Directive
from ._directives import Directives as _Directives
from ._message import Message as _Message
from ._stub import Docstring as _Docstring
from ._stub import Signature as _Signature
from ._utils import vprint as _vprint

_FILE_INFO = "{path}: {msg}"


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
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        node: _ast.Module | _ast.ClassDef | _ast.FunctionDef,
        directives: _Directives,
        path: _Path | None = None,
        ignore_args: bool = False,
        ignore_kwargs: bool = False,
        check_class_constructor: bool = False,
    ) -> None:
        super().__init__()
        self._name = node.name
        self._path = f"{path}:" if path is not None else ""
        overloads: list[str] = []
        returns = None
        self._parse_ast(
            node,
            directives,
            path,
            ignore_args,
            ignore_kwargs,
            check_class_constructor,
            overloads,
            returns,
        )

    def _parse_ast(  # pylint: disable=protected-access,too-many-arguments
        self,
        node,
        directives,
        path,
        ignore_args,
        ignore_kwargs,
        check_class_constructor,
        overloads,
        returns,
    ) -> None:
        parent_comments, parent_disabled = directives.get(
            node.lineno, ([], [])
        )
        if hasattr(node, "body"):
            for subnode in node.body:
                comments, disabled = directives.get(subnode.lineno, ([], []))
                comments.extend(parent_comments)
                disabled.extend(parent_disabled)
                if isinstance(subnode, _ast.FunctionDef):
                    func = Function(
                        subnode,
                        comments,
                        directives,
                        disabled,
                        path,
                        ignore_args,
                        ignore_kwargs,
                        check_class_constructor,
                    )
                    if func.isoverloaded:
                        overloads.append(func.name)
                        returns = func.signature.rettype
                    else:
                        if func.name in overloads:
                            subnode.returns = returns
                            # noinspection PyProtectedMember
                            func._signature._rettype = (
                                returns
                                if isinstance(returns, str)
                                else func._signature._get_rettype(returns)
                            )
                            # noinspection PyProtectedMember
                            func._signature._returns = (
                                str(func._signature._rettype) != "None"
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
                        overloads,
                        returns,
                    )

    @property
    def path(self) -> str:
        """Representation of path to parent."""
        return self._path

    @property
    def isprotected(self) -> bool:
        """Boolean value for whether class is protected."""
        return self._name.startswith("_")


class Function(Parent):
    """Represents a function with signature and docstring parameters.

    :param node: Function's abstract syntax tree.
    :param comments: Comments in list form containing directives.
    :param directives: Directive, if any, belonging to this function.
    :param disabled: List of disabled checks specific to this function.
    :param path: Path to base path representation on.
    :param ignore_args: Ignore args prefixed with an asterisk.
    :param ignore_kwargs: Ignore kwargs prefixed with two asterisks.
    :param check_class_constructor: If the function is the class
        constructor, use its own docstring. Otherwise, use the class
        level docstring for the constructor function.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        node: _ast.FunctionDef,
        comments: _t.List[_Directive],
        directives: _Directives,
        disabled: list[_Message],
        path: _Path | None = None,
        ignore_args: bool = False,
        ignore_kwargs: bool = False,
        check_class_constructor: bool = False,
    ) -> None:
        super().__init__(
            node,
            directives,
            path,
            ignore_args,
            ignore_kwargs,
            check_class_constructor,
        )
        self._node = node
        self._directives = comments
        self._disabled = disabled
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
    def disabled(self) -> list[_Message]:
        """List of disabled checks specific to this function."""
        return self._disabled

    @property
    def directives(self) -> _t.List[_Directive]:
        """Directive, if any, belonging to this function."""
        return self._directives


class Modules(_t.List[Parent]):
    """Sequence of ``Module`` objects parsed from Python modules or str.

    Recursively collect Python files from within all dirs that exist
    under paths provided.

    If string is provided, ignore paths.

    :param paths: Path(s) to parse ``Module``(s) from.
    :param disable: List of checks to disable.
    :param excludes: List pf regular expression of files and dirs to
        exclude from checks.
    :param string: String to parse if provided.
    :param ignore_args: Ignore args prefixed with an asterisk.
    :param ignore_kwargs: Ignore kwargs prefixed with two asterisks.
    :param check_class_constructor: Check the class constructor's
        docstring. Otherwise, expect the constructor's documentation to
        be on the class level docstring.
    :param verbose: increase output verbosity.
    """

    # handle errors here before appending a module
    def _add_module(  # pylint: disable=too-many-arguments
        self,
        disable: list[_Message],
        string: str | None = None,
        root: _Path | None = None,
        ignore_args: bool = False,
        ignore_kwargs: bool = False,
        check_class_constructor: bool = False,
    ) -> None:
        try:
            if root is not None:
                string = root.read_text(encoding="utf-8")

            # empty string won't happen but keeps the
            # typechecker happy
            string = string or ""
            self.append(
                Parent(
                    _ast.parse(string),
                    _Directives(string, disable),
                    root,
                    ignore_args,
                    ignore_kwargs,
                    check_class_constructor,
                )
            )
        except (_AstroidSyntaxError, UnicodeDecodeError) as err:
            if root is not None and root.name.endswith(".py"):
                # keep raising errors for .py files as was done prior to
                # this change
                # pass by silently for files that do not end with .py,
                # which were not checked at all prior (these may result
                # in a 123 syntax error exit status in the future)
                # with this there should be no breaking change, and
                # files that are supposed to be python, files evident by
                # their suffix, will continue to fail
                raise err

            _vprint(
                _FILE_INFO.format(
                    path=root or "stdin", msg=str(err).replace("\n", " ")
                ),
                self._verbose,
            )

    def __init__(  # pylint: disable=too-many-arguments
        self,
        *paths: _Path,
        disable: list[_Message],
        excludes: list[str],
        string: str | None = None,
        ignore_args: bool = False,
        ignore_kwargs: bool = False,
        check_class_constructor: bool = False,
        verbose: bool = False,
    ) -> None:
        super().__init__()
        self._disable = disable
        self._excludes = excludes
        self._ignore_args = ignore_args
        self._ignore_kwargs = ignore_kwargs
        self.check_class_constructor = check_class_constructor
        self._verbose = verbose
        if string is not None:
            self._add_module(
                disable,
                string=string,
                ignore_args=ignore_args,
                ignore_kwargs=ignore_kwargs,
                check_class_constructor=check_class_constructor,
            )
        else:
            for path in paths:
                self._populate(path)

    def _populate(self, root: _Path) -> None:
        if not root.exists():
            raise FileNotFoundError(root)

        if str(root) != "." and any(
            _re.match(i, root.name) for i in self._excludes
        ):
            _vprint(
                _FILE_INFO.format(path=root, msg="in exclude list, skipping"),
                self._verbose,
            )
            return

        if root.is_file():
            self._add_module(
                self._disable,
                root=root,
                ignore_args=self._ignore_args,
                ignore_kwargs=self._ignore_kwargs,
                check_class_constructor=self.check_class_constructor,
            )

        if root.is_dir():
            for path in root.iterdir():
                self._populate(path)
