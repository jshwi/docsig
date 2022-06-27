"""
docsig._module
==============
"""
from __future__ import annotations

import typing as _t
from pathlib import Path as _Path

import astroid as _ast

from ._function import Function as _Function


class Parent:  # pylint: disable=too-few-public-methods
    """Represents an object that contains functions/methods.

    :param node: Abstract syntax tree.
    """

    def __init__(
        self, node: _ast.Module | _ast.ClassDef, method: bool = False
    ) -> None:
        self._node = node
        self._funcs = []
        for item in self._node.body:  # type: ignore
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
                    self._funcs.append(_Function(item, method))

    @property
    def funcs(self) -> _t.List[_Function]:
        """List of functions contained within the module.

        :param:
        """
        return self._funcs


class Class(Parent):  # pylint: disable=too-few-public-methods
    """Represents a class with method parameters.

    :param node: Abstract syntax tree.
    """

    def __init__(self, node: _ast.ClassDef) -> None:
        super().__init__(node, method=True)

    @property
    def name(self) -> str:
        """Name of module."""
        return self._node.name  # type: ignore


class Module(Parent):
    """Represents a module with function parameters.

    :param path: Path to compile function data from.
    """

    def __init__(self, path: _Path) -> None:
        node = _ast.parse(path.read_text())
        super().__init__(node)
        self._path = path
        self._classes = [
            Class(f)
            for f in node.body  # type: ignore
            if isinstance(f, _ast.ClassDef) and not str(f.name).startswith("_")
        ]

    @property
    def name(self) -> str:
        """Name of module."""
        return str(self._path)

    @property
    def classes(self) -> _t.List[Class]:
        """List of ``Class`` objects."""
        return self._classes
