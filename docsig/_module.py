"""
docsig._module
==============
"""
from __future__ import annotations

import typing as _t
from pathlib import Path as _Path

import astroid as _ast

from ._function import Function as _Function
from ._objects import MutableSequence as _MutableSequence


class Parent(_MutableSequence[_Function]):
    """Represents an object that contains functions/methods.

    :param path: Path that node is parsed from.
    :param node: Abstract syntax tree.
    :param method: Boolean for whether functions are class methods.
    """

    def __init__(
        self,
        path: _Path,
        node: _ast.Module | _ast.ClassDef,
        method: bool = False,
    ) -> None:
        super().__init__()
        self._node = node
        self._name = str(path)
        for item in self._node.body:
            if isinstance(item, _ast.FunctionDef) and not str(
                item.name
            ).startswith("_"):
                overridden = False
                if isinstance(item.parent.frame(), _ast.ClassDef):
                    for ancestor in item.parent.frame().ancestors():
                        if item.name in ancestor and isinstance(
                            ancestor[item.name], _ast.nodes.FunctionDef
                        ):
                            overridden = True

                if not overridden:
                    self.append(_Function(item, method))

    @property
    def name(self) -> str:
        """Name of parent."""
        return self._name


class Class(Parent):  # pylint: disable=too-few-public-methods
    """Represents a class with method parameters.

    :param path: Path that node is parsed from.
    :param node: Abstract syntax tree.
    """

    def __init__(self, path: _Path, node: _ast.ClassDef) -> None:
        super().__init__(path, node, method=True)
        self._name = f"{self._name}::{node.name}"


class Module(Parent):
    """Represents a module with function parameters.

    :param path: Path to compile function data from.
    """

    def __init__(self, path: _Path) -> None:
        node = _ast.parse(path.read_text())
        super().__init__(path, node)
        self._classes = [
            Class(path, f)
            for f in node.body
            if isinstance(f, _ast.ClassDef) and not str(f.name).startswith("_")
        ]

    @property
    def classes(self) -> _t.List[Class]:
        """List of ``Class`` objects."""
        return self._classes
