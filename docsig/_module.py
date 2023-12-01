"""
docsig._module
==============
"""
from __future__ import annotations as _

import typing as _t
from pathlib import Path as _Path

import astroid as _ast

from ._directives import Directives as _Directives
from ._function import Function as _Function
from ._message import Message as _Message
from ._utils import isprotected as _isprotected


class Parent(_t.List[_Function]):
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
        node: _ast.Module | _ast.ClassDef,
        directives: _Directives,
        path: _Path | None = None,
        ignore_args: bool = False,
        ignore_kwargs: bool = False,
        check_class_constructor: bool = False,
    ) -> None:
        super().__init__()
        self._name = node.name
        self._path = f"{path}:" if path is not None else ""
        overloads = []
        returns = None
        parent_comments, parent_disabled = directives.get(
            node.lineno, ([], [])
        )
        for subnode in node.body:
            comments, disabled = directives.get(subnode.lineno, ([], []))
            comments.extend(parent_comments)
            disabled.extend(parent_disabled)
            if isinstance(subnode, _ast.FunctionDef):
                func = _Function(
                    subnode,
                    comments,
                    disabled,
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

    @property
    def path(self) -> str:
        """Representation of path to parent."""
        return self._path

    @property
    def isprotected(self) -> bool:
        """Boolean value for whether class is protected."""
        return _isprotected(self._name)


class _Module(_t.List[Parent]):
    def __init__(  # pylint: disable=too-many-arguments
        self,
        string: str,
        disable: list[_Message],
        path: _Path | None = None,
        ignore_args: bool = False,
        ignore_kwargs: bool = False,
        check_class_constructor: bool = False,
    ) -> None:
        super().__init__()
        ast = _ast.parse(string)
        directives = _Directives(string, disable)
        self.append(Parent(ast, directives, path, ignore_args, ignore_kwargs))
        for subnode in ast.body:
            if isinstance(subnode, _ast.ClassDef):
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


class Modules(_t.List[_Module]):
    """Sequence of ``Module`` objects parsed from Python modules or str.

    Recursively collect Python files from within all dirs that exist
    under paths provided.

    If string is provided, ignore paths.

    :param paths: Path(s) to parse ``Module``(s) from.
    :param disable: List of checks to disable.
    :param string: String to parse if provided.
    :param ignore_args: Ignore args prefixed with an asterisk.
    :param ignore_kwargs: Ignore kwargs prefixed with two asterisks.
    :param check_class_constructor: Check the class constructor's
        docstring. Otherwise, expect the constructor's documentation to
        be on the class level docstring.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        *paths: _Path,
        disable: list[_Message],
        string: str | None = None,
        ignore_args: bool = False,
        ignore_kwargs: bool = False,
        check_class_constructor: bool = False,
    ) -> None:
        super().__init__()
        self._disable = disable
        self._ignore_args = ignore_args
        self._ignore_kwargs = ignore_kwargs
        self.check_class_constructor = check_class_constructor
        if string is not None:
            self.append(
                _Module(
                    string,
                    disable,
                    ignore_args=ignore_args,
                    ignore_kwargs=ignore_kwargs,
                    check_class_constructor=check_class_constructor,
                )
            )
        else:
            for path in paths:
                self._populate(path)

    def _populate(self, root: _Path) -> None:
        if not root.exists():
            raise FileNotFoundError(root)

        if root.is_file() and root.name.endswith(".py"):
            self.append(
                _Module(
                    root.read_text(encoding="utf-8"),
                    self._disable,
                    root,
                    self._ignore_args,
                    self._ignore_kwargs,
                    self.check_class_constructor,
                )
            )

        if root.is_dir():
            for path in root.iterdir():
                self._populate(path)
