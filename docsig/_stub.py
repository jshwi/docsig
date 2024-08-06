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
UNNAMED = -1000

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


class _Matches(_t.List[Param]):
    _pattern = _re.compile(":(.*?):")

    def __init__(
        self, string: str, indent_anomaly: bool, missing_descriptions: bool
    ) -> None:
        super().__init__()
        for line in string.splitlines():
            strip_line = line.lstrip()
            match = self._pattern.split(strip_line)[1:]
            if match:
                description = None
                kinds = match[0].split()
                if kinds:
                    kind = DocType.from_str(kinds[0])

                    if len(kinds) > 1:
                        name = kinds[1]
                    else:
                        # name could not be parsed
                        name = UNNAMED

                    if len(match) > 1:
                        second = match[1]
                        if second != "" or not missing_descriptions:
                            description = second

                    super().append(
                        Param(
                            kind,
                            name,
                            description,
                            int(indent_anomaly),
                        )
                    )


class _Params(_t.List[Param]):
    def __init__(
        self, ignore_args: bool = False, ignore_kwargs: bool = False
    ) -> None:
        super().__init__()
        self._ignore_args = ignore_args
        self._ignore_kwargs = ignore_kwargs
        self._duplicates: list[Param] = []

    # pylint: disable=too-many-boolean-expressions
    def append(self, value: Param) -> None:
        if not value.isprotected and (
            value.kind == DocType.PARAM
            or (value.kind == DocType.ARG and not self._ignore_args)
            or (
                value.kind == DocType.KWARG
                and not self._ignore_kwargs
                and not any(i.kind == DocType.KWARG for i in self)
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
                Param(DocType.ARG, name=arguments.vararg),
                *arguments.kwonlyargs,
                Param(DocType.KWARG, name=arguments.kwarg),
            ]
            if a is not None and a.name
        ]:
            self.args.append(i)

        self._rettype = RetType.from_ast(returns)
        self._returns = self._rettype == RetType.SOME

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

    :param node: Docstring ast node.
    :param ignore_args: Ignore args prefixed with an asterisk.
    :param ignore_kwargs: Ignore kwargs prefixed with two asterisks.
    """

    @staticmethod
    def _indent_anomaly(string: str) -> bool:
        leading_spaces = []
        for line in string.splitlines():
            # only check params
            # description or anything else is out of scope
            if line.lstrip().startswith(":"):
                match = _re.match(r"^\s*", line)
                if match is not None:
                    spaces = len(match.group())
                    if spaces > 0:
                        leading_spaces.append(spaces)

        # look for spaces in odd intervals
        return bool(any(i % 2 != 0 for i in leading_spaces))

    @staticmethod
    def _missing_descriptions(string: str) -> bool:
        # find out if parameter is missing a description
        new = ""
        for line in string.strip().splitlines()[2:]:
            line = line.lstrip()
            if not line.startswith(":"):
                # it is not a parameter, it is a next line description
                # append the next entry to the same line
                new = f"{new[:-1]} "
            new += f"{line}\n"
        if not new:
            return True

        # if it ends with a colon, it's a parameter without a
        # description
        return any(i.endswith(":") for i in new.splitlines())

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
        self,
        node: _ast.Const | None = None,
        ignore_args: bool = False,
        ignore_kwargs: bool = False,
    ) -> None:
        super().__init__(ignore_args, ignore_kwargs)
        self._string = None
        if node is not None:
            self._string = self._normalize_docstring(node.value)
            for i in _Matches(
                self._string,
                self._indent_anomaly(node.value),
                self._missing_descriptions(node.value),
            ):
                self._args.append(i)

        self._returns = self._string is not None and bool(
            _re.search(":returns?:", self._string)
        )

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
