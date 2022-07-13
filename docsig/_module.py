"""
docsig._module
==============
"""
from __future__ import annotations

from pathlib import Path as _Path

import astroid as _ast

from ._function import Function as _Function
from ._objects import MutableSequence as _MutableSequence


class Parent(_MutableSequence[_Function]):
    """Represents an object that contains functions or methods.

    :param node: Parent's abstract syntax tree.
    :param path: Path to base path representation on.
    :param method: Boolean for whether functions are class methods.
    """

    def __init__(
        self,
        node: _ast.Module | _ast.ClassDef,
        path: _Path | None = None,
        method: bool = False,
    ) -> None:
        super().__init__()
        self._name = node.name
        self._path = f"{path}::" if path is not None else ""
        for subnode in node.body:
            if isinstance(subnode, _ast.FunctionDef) and not str(
                subnode.name
            ).startswith("_"):
                overridden = False
                if isinstance(subnode.parent.frame(), _ast.ClassDef):
                    for ancestor in subnode.parent.frame().ancestors():
                        if subnode.name in ancestor and isinstance(
                            ancestor[subnode.name], _ast.nodes.FunctionDef
                        ):
                            overridden = True

                if not overridden:
                    self.append(_Function(subnode, method=method))

    @property
    def name(self) -> str:
        """Name of parent."""
        return self._name

    @property
    def path(self) -> str:
        """Representation of path to parent."""
        return self._path


class Class(Parent):
    """Represents a class and its methods.

    :param node: Class's abstract syntax tree.
    :param path: Path to base path representation on.
    """

    def __init__(self, node: _ast.ClassDef, path: _Path | None = None) -> None:
        super().__init__(node, path, method=True)
        self._name = node.name
        self._path = f"{self._path}{self.name}::"
        for subnode in node.body:
            if (
                isinstance(subnode, _ast.FunctionDef)
                and str(subnode.name) == "__init__"
            ):
                self.append(_Function(subnode, node.doc_node, method=True))


class Module(_MutableSequence[Parent]):
    """Represents a module with top level functions and classes.

    :param node: Module's abstract syntax tree.
    :param path: Path for naming module and classes.
    """

    def __init__(self, node: _ast.Module, path: _Path | None = None) -> None:
        super().__init__()
        self.append(Parent(node, path))
        for subnode in node.body:
            if isinstance(subnode, _ast.ClassDef) and not str(
                subnode.name
            ).startswith("_"):
                self.append(Class(subnode, path))


class Modules(_MutableSequence[Module]):
    """Sequence of ``Module`` objects parsed from Python modules or str.

    Recursively collect Python files from within all dirs that exist
    under paths provided.

    If string is provided, ignore paths.

    :param paths: Path(s) to pase ``Module``(s) from.
    :param string: String to parse if provided.
    """

    def __init__(self, *paths: _Path, string: str | None = None) -> None:
        super().__init__()
        if string is not None:
            self.append(Module(_ast.parse(string)))
        else:
            for path in paths:
                self._populate(path)

    def _populate(self, root: _Path) -> None:
        if root.is_file() and root.name.endswith(".py"):
            self.append(Module(_ast.parse(root.read_text()), root))

        if root.is_dir():
            for path in root.iterdir():
                self._populate(path)
