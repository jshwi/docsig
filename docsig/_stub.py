"""
docsig._stub
============
"""

from __future__ import annotations as _

import re as _re
import textwrap as _textwrap
import typing as _t
from collections import Counter as _Counter
from enum import Enum as _Enum

import astroid as _ast
import sphinx.ext.napoleon as _s

# no function will accidentally have this name
UNNAMED = "-1000"

# an example of valid parameter description
VALID_DESCRIPTION = " A valid description."


class RetType(_Enum):
    """Defines the possible types of a return annotation."""

    NONE = 1
    SOME = 2
    UNTYPED = 3

    @classmethod
    def from_ast(cls, returns: _ast.NodeNG | None) -> RetType:
        """Construct a return type object from an AST node.

        :param returns: Ast node or None.
        :return: Constructed return type.
        """
        if isinstance(returns, _ast.Const) and returns.value is None:
            return cls.NONE

        if isinstance(
            returns,
            (
                _ast.Const,
                _ast.Name,
                _ast.Attribute,
                _ast.Subscript,
                _ast.BinOp,
            ),
        ):
            return cls.SOME

        return cls.UNTYPED


class DocType(_Enum):
    """Defines the possible types of a docstring."""

    PARAM = 1
    ARG = 2
    KWARG = 3
    UNKNOWN = 4

    @classmethod
    def from_str(cls, docstring: str) -> DocType:
        """Construct a doc type object from a docstring.

        :param docstring: Docstring string.
        :return: Constructed doc type.
        """
        try:
            return cls[docstring.upper()]
        except KeyError:
            if docstring in ("key", "keyword"):
                return cls.KWARG

        return cls.UNKNOWN


class Param(_t.NamedTuple):
    """A tuple of param types and their names."""

    kind: DocType = DocType.PARAM
    name: str | None = None
    description: str | None = None
    indent: int = 0
    closing_token: str = ":"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Param):
            return False

        args = self, other
        return all(i.kind == DocType.KWARG for i in args) or (
            self.name == other.name and all(i.name is not None for i in args)
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    @property
    def isprotected(self) -> bool:
        """Boolean value for whether parameter is protected."""
        return str(self.name).startswith("_")


class _Params(_t.List[Param]):
    def __init__(
        self, ignore_args: bool = False, ignore_kwargs: bool = False
    ) -> None:
        super().__init__()
        self._ignore_args = ignore_args
        self._ignore_kwargs = ignore_kwargs
        self._duplicates: list[Param] = []

    def append(self, value: Param) -> None:
        if not value.isprotected and any(
            (
                value.kind == DocType.PARAM,
                (value.kind == DocType.ARG and not self._ignore_args),
                (
                    value.kind == DocType.KWARG
                    and not (
                        self._ignore_kwargs
                        or any(i.kind == DocType.KWARG for i in self)
                    )
                ),
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
    def names(self) -> list[str | None]:
        """Get names of params."""
        return [i.name for i in self]

    @property
    def duplicated(self) -> bool:
        """Boolean value for whether there are duplicate parameters.

        Ensure only the names of the parameters are needed to be
        considered duplicates. It is not relevant whether the
        descriptions match.
        """
        for k, v in _Counter(i.name for i in self).items():
            if v > 1:
                for i in self:
                    if i.name == k:
                        # record the duplicates for later analysis
                        self._duplicates.append(i)
                        return True

        return False

    @property
    def duplicates(self) -> list[Param]:
        """Duplicated parameters."""
        return self._duplicates


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

    :param rettype: The return type.
    :param returns: Returns declared in signature.
    :param ignore_args: Ignore args prefixed with an asterisk.
    :param ignore_kwargs: Ignore kwargs prefixed with two asterisks.
    """

    def __init__(
        self,
        rettype: RetType = RetType.NONE,
        returns: bool = False,
        ignore_args: bool = False,
        ignore_kwargs: bool = False,
    ) -> None:
        super().__init__(ignore_args, ignore_kwargs)
        self._rettype = rettype
        self._returns = returns

    @classmethod
    def from_ast(
        cls,
        node: _ast.Module | _ast.ClassDef | _ast.FunctionDef,
        ignore_args: bool = False,
        ignore_kwargs: bool = False,
    ) -> Signature:
        """Parse signature from ast.

        :param node: Abstract syntax tree.
        :param ignore_args: Ignore args prefixed with an asterisk.
        :param ignore_kwargs: Ignore kwargs prefixed with two asterisks.
        :return: Instantiated signature object.
        """
        rettype = RetType.from_ast(node.returns)
        returns = rettype == RetType.SOME
        signature = cls(rettype, returns, ignore_args, ignore_kwargs)
        for i in [
            a if isinstance(a, Param) else Param(name=a.name)
            for a in [
                *node.args.posonlyargs,
                *node.args.args,
                Param(DocType.ARG, name=node.args.vararg),
                *node.args.kwonlyargs,
                Param(DocType.KWARG, name=node.args.kwarg),
            ]
            if a is not None and a.name
        ]:
            signature.args.append(i)

        return signature

    @property
    def rettype(self) -> RetType:
        """Function's return value.

        If a function is typed to return None, return str(None). If no
        typehint exists then return None (NoneType).
        """
        return self._rettype

    def overload(self, rettype: RetType) -> None:
        """Overload signature with a ret type.

        :param rettype: Return type of overloaded signature.
        """
        self._rettype = rettype
        self._returns = rettype != RetType.NONE


class Docstring(_Stub):
    """Represents a function docstring.

    :param string: The raw docstring.
    :param returns: Whether this docstring has a return.
    """

    @staticmethod
    def _indent_anomaly(string: str) -> bool:
        for line in string.splitlines():
            # only check params
            # description or anything else is out of scope
            if line.lstrip().startswith(":"):
                match = _re.match(r"^\s*", line)
                if match is not None:
                    spaces = len(match.group())
                    if spaces > 0:
                        return spaces % 2 != 0

        return False

    @staticmethod
    def _normalize_docstring(string: str) -> str:
        # convert google and numpy style docstrings to parse docstrings
        # as restructured text
        return str(
            _s.NumpyDocstring(
                str(
                    _s.GoogleDocstring(
                        _textwrap.dedent(
                            "\n".join(string.splitlines()[1:])
                        ).replace("*", "")
                    )
                )
            )
        )

    def __init__(
        self, string: str | None = None, returns: bool = False
    ) -> None:
        super().__init__()
        self._string = string
        self._returns = returns

    @classmethod
    def from_ast(cls, node: _ast.Const) -> Docstring:
        """Parse function docstring from ast.

        :param node: Docstring ast node.
        :return: Instantiated docstring object.
        """
        indent_anomaly = cls._indent_anomaly(node.value)
        string = cls._normalize_docstring(node.value)
        returns = bool(_re.search(r":returns?:", string))
        docstring = cls(string, returns)
        for match in _re.findall(
            r":(.*?)([^\w\s])((?:.|\n)*?)(?=\n:|$)", string
        ):
            if match:
                kinds = match[0].split()
                if kinds:
                    docstring.args.append(
                        Param(
                            DocType.from_str(kinds[0]),
                            UNNAMED if len(kinds) == 1 else kinds[1],
                            match[2] or None,
                            int(indent_anomaly),
                            match[1],
                        )
                    )

        return docstring

    @property
    def string(self) -> str | None:
        """The raw documentation string, if it exists, else None."""
        return self._string

    @property
    def bare(self) -> bool:
        """Boolean value for whether params are documented.

        Docstring has to exist for docstring to be considered bare.
        """
        return self._string is not None and not self._args and not self.returns
