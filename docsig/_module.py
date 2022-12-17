"""
docsig._module
==============
"""
from __future__ import annotations

from pathlib import Path as _Path

import astroid as _ast

from ._function import Function as _Function
from ._objects import MutableSequence as _MutableSequence
from ._utils import isprotected as _isprotected


class Parent(_MutableSequence[_Function]):
    """Represents an object that contains functions or methods.

    :param node: Parent's abstract syntax tree.
    :param path: Path to base path representation on.
    :param ignore_args: Ignore args prefixed with an asterisk.
    :param ignore_kwargs: Ignore kwargs prefixed with two asterisks.
    """

    def __init__(
        self,
        node: _ast.Module | _ast.ClassDef,
        path: _Path | None = None,
        ignore_args: bool = False,
        ignore_kwargs: bool = False,
    ) -> None:
        super().__init__()
        self._name = node.name
        self._path = f"{path}:" if path is not None else ""
        for subnode in node.body:
            if isinstance(subnode, _ast.FunctionDef):
                self.append(_Function(subnode, ignore_args, ignore_kwargs))

    @property
    def path(self) -> str:
        """Representation of path to parent."""
        return self._path

    @property
    def isprotected(self) -> bool:
        """Boolean value for whether class is protected."""
        return _isprotected(self._name)


class _Module(_MutableSequence[Parent]):
    """Represents a module with top level functions and classes.

    :param node: Module's abstract syntax tree.
    :param path: Path for naming module and classes.
    """

    def __init__(
        self,
        node: _ast.Module,
        path: _Path | None = None,
        ignore_args: bool = False,
        ignore_kwargs: bool = False,
    ) -> None:
        super().__init__()
        self.append(Parent(node, path, ignore_args, ignore_kwargs))
        for subnode in node.body:
            if isinstance(subnode, _ast.ClassDef):
                self.append(Parent(subnode, path, ignore_args, ignore_kwargs))


class Modules(_MutableSequence[_Module]):
    """Sequence of ``Module`` objects parsed from Python modules or str.

    Recursively collect Python files from within all dirs that exist
    under paths provided.

    If string is provided, ignore paths.

    :param paths: Path(s) to pase ``Module``(s) from.
    :param string: String to parse if provided.
    :param ignore_args: Ignore args prefixed with an asterisk.
    :param ignore_kwargs: Ignore kwargs prefixed with two asterisks.
    """

    def __init__(
        self,
        *paths: _Path,
        string: str | None = None,
        ignore_args: bool = False,
        ignore_kwargs: bool = False,
    ) -> None:
        super().__init__()
        self._ignore_args = ignore_args
        self._ignore_kwargs = ignore_kwargs
        if string is not None:
            self.append(
                _Module(
                    _ast.parse(string),
                    ignore_args=ignore_args,
                    ignore_kwargs=ignore_kwargs,
                )
            )
        else:
            for path in paths:
                self._populate(path)

    def _populate(self, root: _Path) -> None:
        if root.is_file() and root.name.endswith(".py"):
            self.append(
                _Module(
                    _ast.parse(root.read_text()),
                    root,
                    self._ignore_args,
                    self._ignore_kwargs,
                )
            )

        if root.is_dir():
            for path in root.iterdir():
                self._populate(path)
