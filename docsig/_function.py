"""
docsig._function
================
"""
import ast as _ast
import typing as _t

from ._utils import get_index as _get_index


class Docstring:
    """Represents docstring parameters.

    :param func: ``ast.FunctionDef`` object from which the
        docstring can be parsed.
    """

    def __init__(self, func: _ast.FunctionDef) -> None:
        self._docstring: _t.Optional[str] = _ast.get_docstring(func)
        self._is_doc = bool(self._docstring is not None)
        self._args: _t.Tuple[_t.Optional[str], ...] = tuple()
        self._returns = False
        if self._is_doc:
            self._parse_docstring()

    def _parse_docstring(self):
        self._returns = bool(":return:" in self._docstring)
        self._args = tuple(
            _get_index(1, s.split())
            for s in self._docstring.split(":")
            if s.startswith("param")
        )

    @property
    def is_doc(self) -> bool:
        """Check that docstring exists."""
        return self._is_doc

    @property
    def args(self) -> _t.Tuple[_t.Optional[str], ...]:
        """Docstring args."""
        return self._args

    @property
    def returns(self) -> bool:
        """Check that docstring return is documented."""
        return self._returns
