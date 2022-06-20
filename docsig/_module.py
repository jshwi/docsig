"""
docsig._module
==============
"""
import ast as _ast
import typing as _t
from pathlib import Path as _Path

from ._function import Function as _Function


class Parent:  # pylint: disable=too-few-public-methods
    """Represents an object that contains functions/methods.

    :param node: Abstract syntax tree.
    """

    def __init__(self, node: _ast.AST, method: bool = False) -> None:
        self._node = node
        self._funcs = [
            _Function(f, method)
            for f in self._node.body  # type: ignore
            if isinstance(f, _ast.FunctionDef)
            and not str(f.name).startswith("_")
        ]

    @property
    def funcs(self) -> _t.List[_Function]:
        """List of functions contained within the module."""
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
        node = _ast.parse(path.read_text(), filename=str(path))
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
