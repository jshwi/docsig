"""
docsig._signature
=================
"""
from __future__ import annotations

import astroid as _ast

from ._params import Param as _Param
from ._params import Params as _Params
from ._utils import isprotected as _isprotected


class Signature:
    """Represents signature parameters.

    :param arguments: Argument's abstract syntax tree.
    :param returns: Function's return value.
    :param ismethod: Boolean value for whether this signature is for a
        class method or not.
    :param isstaticmethod: Boolean value for whether this signature is
        for a static method or not.
    """

    _param = "param"

    def __init__(
        self,
        arguments: _ast.Arguments,
        returns: _ast.Module,
        ismethod: bool = False,
        isstaticmethod: bool = False,
    ) -> None:
        self._arguments = arguments
        self._args = _Params()
        self._args.extend(
            _Param(self._param, a.name, None, 0)
            for a in self._arguments.args
            if not _isprotected(a.name)
        )
        self._return_value = self._get_returns(returns)
        self._returns = (
            self._return_value is not None and self._return_value != "None"
        )
        self._get_args_kwargs()
        if ismethod and not isstaticmethod and self._args:
            self._args.pop(0)

    def _get_args_kwargs(self) -> None:
        vararg = self._arguments.vararg
        if vararg is not None and not _isprotected(vararg):
            self._args.append(_Param(self._param, f"*{vararg}", None, 0))

        if self._arguments.kwonlyargs:
            self._args.extend(
                _Param(self._param, k.name, None, 0)
                for k in self._arguments.kwonlyargs
            )

        kwarg = self._arguments.kwarg
        if kwarg is not None and not _isprotected(kwarg):
            self._args.append(_Param(self._param, f"**{kwarg}", None, 0))

    def _get_returns(self, returns: _ast.NodeNG | None) -> str | None:
        if isinstance(returns, _ast.Name):
            return returns.name

        if isinstance(returns, _ast.Attribute):
            return returns.attrname

        if isinstance(returns, _ast.Const):
            return str(returns.kind)

        if isinstance(returns, _ast.Subscript):
            return "{}[{}]".format(
                self._get_returns(returns.value),
                self._get_returns(returns.slice),
            )

        if isinstance(returns, _ast.BinOp):
            return "{} | {}".format(
                self._get_returns(returns.left),
                self._get_returns(returns.right),
            )

        return None

    @property
    def args(self) -> _Params:
        """Tuple of signature parameters."""
        return self._args

    @property
    def return_value(self) -> str | None:
        """Function's return value.

        If a function is typed to return None, return str(None). If no
        typehint exists then return None (NoneType).
        """
        return self._return_value

    @property
    def returns(self) -> bool:
        """Check that a function returns a value."""
        return self._returns
