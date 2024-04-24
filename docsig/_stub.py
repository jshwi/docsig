"""
docsig._function
================
"""

from __future__ import annotations as _

import re as _re
import textwrap as _textwrap
import typing as _t
from collections import Counter as _Counter

import astroid as _ast
import sphinx.ext.napoleon as _s

PARAM = "param"
KEYWORD = "keyword"
KEY = "key"
RETURN = "return"
ARG = "arg"


# noinspection PyTypeChecker
class _GoogleDocstring(str):
    def __new__(cls, string: str) -> _GoogleDocstring:
        return super().__new__(cls, str(_s.GoogleDocstring(string)))


# noinspection PyTypeChecker
class _NumpyDocstring(str):
    def __new__(cls, string: str) -> _NumpyDocstring:
        return super().__new__(cls, str(_s.NumpyDocstring(string)))


# noinspection PyTypeChecker
class _DocFmt(str):
    def __new__(cls, string: str) -> _DocFmt:
        return super().__new__(
            cls,
            _textwrap.dedent("\n".join(string.splitlines()[1:])).replace(
                "*", ""
            ),
        )


# noinspection PyTypeChecker
class _RawDocstring(str):
    def __new__(cls, string: str) -> _RawDocstring:
        return super().__new__(
            cls, _NumpyDocstring(_GoogleDocstring(_DocFmt(string)))
        )


class Param(_t.NamedTuple):
    """A tuple of param types and their names."""

    kind: str = PARAM
    name: str | None = None
    description: str | None = None
    indent: int = 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Param):
            return False

        args = self, other
        return all(i.kind == KEY for i in args) or (
            self.name == other.name and all(i.name is not None for i in args)
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    @property
    def isprotected(self) -> bool:
        """Boolean value for whether parameter is protected."""
        return str(self.name).startswith("_")


class _Matches(_t.List[Param]):
    _pattern = _re.compile(":(.*?):")
    _normalize = {KEYWORD: KEY}

    def __init__(self, string: str) -> None:
        super().__init__()
        for line in string.splitlines():
            strip_line = line.lstrip()
            match = self._pattern.split(strip_line)[1:]
            if match:
                name = description = None
                kinds = match[0].split()
                if kinds:
                    kind = kinds[0]
                    for substring, replace in self._normalize.items():
                        kind = kind.replace(substring, replace)

                    if len(kinds) > 1:
                        name = kinds[1]

                    if len(match) > 1:
                        description = match[1]

                    super().append(
                        Param(
                            kind,
                            name,
                            description,
                            len(line) - len(strip_line),
                        )
                    )


class _Params(_t.List[Param]):
    def __init__(
        self, ignore_args: bool = False, ignore_kwargs: bool = False
    ) -> None:
        super().__init__()
        self._ignore_args = ignore_args
        self._ignore_kwargs = ignore_kwargs

    # pylint: disable=too-many-boolean-expressions
    def append(self, value: Param) -> None:
        if not value.isprotected and (
            value.kind == PARAM
            or (value.kind == ARG and not self._ignore_args)
            or (
                value.kind == KEY
                and not self._ignore_kwargs
                and not any(i.kind == KEY for i in self)
            )
        ):
            super().append(value)

    def get(self, index: int) -> Param:
        """Get a param.

        If the index does not exist return a `Param` with None as
        `Param.name`.

        :param index: Index of param to get.
        :return: Param belonging to the index.
        """
        try:
            return self[index]
        except IndexError:
            return Param()

    @property
    def duplicated(self) -> bool:
        """Boolean value for whether there are duplicate parameters."""
        return any(k for k, v in _Counter(self).items() if v > 1)


class _Stub:
    def __init__(
        self, ignore_args: bool = False, ignore_kwargs: bool = False
    ) -> None:
        self._args = _Params(ignore_args, ignore_kwargs)
        self._returns = False

    @property
    def args(self) -> _Params:
        """Collection of `Param` types."""
        return self._args

    @property
    def returns(self) -> bool:
        """Boolean value for whether this returns a value."""
        return self._returns


class Signature(_Stub):
    """Represents a function signature.

    :param arguments: Arguments provided to signature.
    :param returns: Returns declared in signature.
    :param ismethod: Whether this signature belongs to a method.
    :param isstaticmethod: Whether this signature belongs to a static
        method.
    :param ignore_args: Ignore args prefixed with an asterisk.
    :param ignore_kwargs: Ignore kwargs prefixed with two asterisks.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        arguments: _ast.Arguments,
        returns: _ast.Module | str,
        ismethod: bool = False,
        isstaticmethod: bool = False,
        ignore_args: bool = False,
        ignore_kwargs: bool = False,
    ) -> None:
        super().__init__(ignore_args, ignore_kwargs)

        if ismethod and not isstaticmethod:
            if arguments.posonlyargs:
                arguments.posonlyargs.pop(0)
            elif arguments.args:
                arguments.args.pop(0)

        for i in [
            a if isinstance(a, Param) else Param(name=a.name)
            for a in [
                *arguments.posonlyargs,
                *arguments.args,
                Param(ARG, name=arguments.vararg),
                *arguments.kwonlyargs,
                Param(KEY, name=arguments.kwarg),
            ]
            if a is not None and a.name
        ]:
            self.args.append(i)

        self._rettype = (
            returns if isinstance(returns, str) else self._get_rettype(returns)
        )
        self._returns = str(self._rettype) != "None"

    def _get_rettype(self, returns: _ast.NodeNG | None) -> str | None:
        if isinstance(returns, _ast.Name):
            return returns.name

        if isinstance(returns, _ast.Attribute):
            return returns.attrname

        if isinstance(returns, _ast.Const):
            return str(returns.value)

        if isinstance(returns, _ast.Subscript):
            return "{}[{}]".format(
                self._get_rettype(returns.value),
                self._get_rettype(returns.slice),
            )

        if isinstance(returns, _ast.BinOp):
            return "{} | {}".format(
                self._get_rettype(returns.left),
                self._get_rettype(returns.right),
            )

        return None

    @property
    def rettype(self) -> str | None:
        """Function's return value.

        If a function is typed to return None, return str(None). If no
        typehint exists then return None (NoneType).
        """
        return self._rettype

    def overload(self, rettype: str | None) -> None:
        """Overload signature with a ret type.

        :param rettype: Return type of overloaded signature.
        """
        self._rettype = (
            rettype if isinstance(rettype, str) else self._get_rettype(rettype)
        )
        self._returns = str(rettype) != "None"


class Docstring(_Stub):
    """Represents a function docstring.

    :param node: Docstring ast node.
    :param ignore_args: Ignore args prefixed with an asterisk.
    :param ignore_kwargs: Ignore kwargs prefixed with two asterisks.
    """

    def __init__(
        self,
        node: _ast.Const | None = None,
        ignore_args: bool = False,
        ignore_kwargs: bool = False,
    ) -> None:
        super().__init__(ignore_args, ignore_kwargs)
        self._string = None
        if node is not None:
            self._string = _RawDocstring(node.value)
            for i in _Matches(self._string):
                self._args.append(i)

        self._returns = self._string is not None and bool(
            _re.search(":returns?:", self._string)
        )

    @property
    def string(self) -> _RawDocstring | None:
        """The raw documentation string, if it exists, else None."""
        return self._string

    @property
    def bare(self) -> bool:
        """Boolean value for whether params are documented.

        Docstring has to exist for docstring to be considered bare.
        """
        return self._string is not None and not self._args and not self.returns
