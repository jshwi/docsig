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


class Signature:
    """Represents signature parameters.

    :param func: ``ast.FunctionDef`` object from which the params can be
        parsed.
    """

    def __init__(self, func: _ast.FunctionDef, method: bool = False) -> None:
        self._func = func
        self._args = [a.arg for a in self._func.args.args if a.arg != "_"]
        self._returns: _t.Optional[str] = None
        self._get_args_kwargs()
        self._get_returns()
        if method:
            for dec in func.decorator_list:
                if isinstance(dec, _ast.Name) and dec.id == "property":
                    self._returns = None

            if self._args and self._args[0] in ("self", "cls"):
                self._args.pop(0)

    def _get_args_kwargs(self) -> None:
        if self._func.args.vararg is not None:
            self._args.append(f"*{self._func.args.vararg.arg}")

        if self._func.args.kwarg is not None:
            self._args.append(f"**{self._func.args.kwarg.arg}")

    def _get_returns(self) -> None:
        if self._func.returns is not None:
            if isinstance(self._func.returns, _ast.Name):
                self._returns = self._func.returns.id

            elif isinstance(self._func.returns, _ast.Subscript):
                if isinstance(self._func.returns.value, _ast.Name):
                    self._returns = self._func.returns.value.id

                elif isinstance(self._func.returns.value, _ast.Attribute):
                    self._returns = self._func.returns.value.attr

    @property
    def args(self) -> _t.Tuple[str, ...]:
        """Tuple of signature parameters."""
        return tuple(self._args)

    @property
    def returns(self) -> _t.Optional[str]:
        """Return type:"""
        return self._returns


class Function:
    """Represents a function with signature and docstring parameters.

    :param func: ``ast.FunctionDef`` object from which the params can be
        parsed.
    """

    def __init__(self, func: _ast.FunctionDef, method: bool = False) -> None:
        self._name = func.name
        self._signature = Signature(func, method=method)
        self._docstring = Docstring(func)

    @property
    def name(self) -> str:
        """The name of the function."""
        return self._name

    @property
    def signature(self) -> Signature:
        """The function's signature parameters."""
        return self._signature

    @property
    def docstring(self) -> Docstring:
        """The function's docstring parameters."""
        return self._docstring
