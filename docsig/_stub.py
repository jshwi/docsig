"""
docsig._stub
============

Stub types for parsed docstrings and signatures.
"""

from __future__ import annotations as _

import re as _re
import textwrap as _textwrap
import typing as _t
from collections import Counter as _Counter
from enum import Enum as _Enum

import astroid as _ast
import sphinx.ext.napoleon as _s

from ._config import Ignore as _Ignore

# no function will accidentally have this name
UNNAMED = "-1000"

# an example of valid parameter description
VALID_DESCRIPTION = " A valid description."


class RetType(_Enum):
    """Possible types of return annotation."""

    NONE = 1
    SOME = 2
    UNTYPED = 3

    @classmethod
    def from_ast(cls, returns: _ast.nodes.NodeNG | None) -> RetType:
        """Build return type from the function's return AST node.

        :param returns: Return annotation AST node or None.
        :return: RetType.NONE, RetType.SOME, or RetType.UNTYPED.
        """
        if isinstance(returns, _ast.nodes.Const) and returns.value is None:
            return cls.NONE

        if isinstance(
            returns,
            (
                _ast.nodes.Const,
                _ast.nodes.Name,
                _ast.nodes.Attribute,
                _ast.nodes.Subscript,
                _ast.nodes.BinOp,
            ),
        ):
            return cls.SOME

        return cls.UNTYPED


class DocType(_Enum):
    """Type of docstring parameter."""

    PARAM = 1
    ARG = 2
    KWARG = 3
    UNKNOWN = 4

    @classmethod
    def from_str(cls, docstring: str) -> DocType:
        """Map a docstring keyword to docstring type.

        :param docstring: Keyword from docstring (param, arg, etc.).
        :return: Corresponding DocType or DocType.UNKNOWN.
        """
        try:
            return cls[docstring.upper()]
        except KeyError:
            if docstring in ("key", "keyword"):
                return cls.KWARG

        return cls.UNKNOWN


# todo: consider a parent object that can be used for returns that do
# todo: not include the name attribute
class Param:
    """Single parameter from a docstring or function signature.

    :param type_: The type of the parameter.
    :param name: Parameter name.
    :param description: Optional description text.
    :param indent: Indent width in spaces.
    :param closing_token: Token after the name (colon by default).
    """

    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def __init__(
        self,
        type_: DocType = DocType.PARAM,
        name: str | None = None,
        description: str | None = None,
        indent: int = 0,
        closing_token: str = ":",
    ) -> None:
        self._type = type_
        self._name = name
        self._description = description
        self._indent = indent
        self._closing_token = closing_token

    def __eq__(self, other: object) -> bool:
        iseq = False
        if isinstance(other, Param):
            args = self, other
            iseq = all(i.type == DocType.KWARG for i in args) or (
                self.name == other.name
                and all(i.name is not None for i in args)
            )

        return iseq

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    @property
    def isprotected(self) -> bool:
        """True if the parameter name starts with an underscore."""
        return str(self.name).startswith("_")

    @property
    def type(self) -> DocType:
        """Type of the param."""
        return self._type

    @property
    def name(self) -> str | None:
        """Name of the param."""
        return self._name

    @property
    def description(self) -> str | None:
        """Description of param."""
        return self._description

    @property
    def indent(self) -> int:
        """Number of spaces in the indent."""
        return self._indent

    @property
    def closing_token(self) -> str:
        """Token used to terminate the param name definition."""
        return self._closing_token


class Params(_t.List[Param]):
    """A list-like collection of params.

    :param ignore: Configuration object for what to ignore.
    """

    def __init__(self, ignore: _Ignore) -> None:
        super().__init__()
        self._ignore = ignore
        self._duplicates: list[Param] = []

    def append(self, value: Param) -> None:
        if not value.isprotected and any(
            (
                value.type == DocType.PARAM,
                (value.type == DocType.ARG and not self._ignore.args),
                (
                    value.type == DocType.KWARG
                    and not (
                        self._ignore.kwargs
                        or any(i.type == DocType.KWARG for i in self)
                    )
                ),
            ),
        ):
            super().append(value)

    def get(self, index: int) -> Param:
        """Return Param at index, or a Param with name None if missing.

        :param index: Index into this list.
        :return: Param at that index or an empty Param.
        """
        try:
            return self[index]
        except IndexError:
            return Param()

    @property
    def names(self) -> list[str | None]:
        """Parameter names in order."""
        return [i.name for i in self]

    @property
    def duplicated(self) -> bool:
        """True if any parameter name appears more than once.

        Only names are compared; descriptions are ignored.
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
        """Params that share a name."""
        return self._duplicates


class _Stub:
    def __init__(self, ignore: _Ignore | None = None) -> None:
        self._args = Params(ignore or _Ignore())
        self._returns = False

    @property
    def args(self) -> Params:
        """Params for this stub (signature or docstring)."""
        return self._args

    @property
    def returns(self) -> bool:
        """True if a return (or yield) is declared or documented."""
        return self._returns


class Signature(_Stub):
    """Parsed function signature (args and return type).

    :param rettype: Kind of return (none, some, untyped).
    :param returns: True if return is declared in the signature.
    :param ignore: Configuration object for what to ignore.
    """

    def __init__(
        self,
        rettype: RetType = RetType.NONE,
        returns: bool = False,
        ignore: _Ignore | None = None,
    ) -> None:
        super().__init__(ignore or _Ignore())
        self._rettype = rettype
        self._returns = returns

    @classmethod
    def from_ast(
        cls,
        node: _ast.nodes.Module | _ast.nodes.ClassDef | _ast.nodes.FunctionDef,
        ignore: _Ignore,
    ) -> Signature:
        """Build Signature from a function or class AST node.

        :param node: AST node (function, class, or module).
        :param ignore: Configuration object for what to ignore.
        :return: Signature with args and return type.
        """
        rettype = RetType.from_ast(node.returns)
        returns = rettype == RetType.SOME
        signature = cls(rettype, returns, ignore)
        # noinspection PyUnresolvedReferences
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
        """Return annotation kind (none, some, or untyped)."""
        return self._rettype

    def overload(self, rettype: RetType) -> None:
        """Set this signature's return type (for overloads).

        :param rettype: Return type for the overloaded variant.
        """
        self._rettype = rettype
        self._returns = rettype != RetType.NONE


class Docstring(_Stub):
    """Parsed function docstring (params and return section).

    :param string: Raw docstring text after normalization.
    :param returns: True if a return or yield section is present.
    :param ret_description_missing: True if return has no description.
    """

    @staticmethod
    def _indent_anomaly(string: str) -> bool:
        # strip double dot directives from docstring, which can be
        # indented arbitrarily
        string = _re.sub(
            r"^[ \t]*\.\..*\n(?:[ \t]+.*\n)*",
            "",
            string,
            flags=_re.MULTILINE,
        )
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
        # convert Google and numpy style docstrings to parse docstrings
        # as restructured text
        return str(
            _s.NumpyDocstring(
                str(
                    _s.GoogleDocstring(
                        _textwrap.dedent(
                            "\n".join(string.splitlines()[1:]),
                        ).replace("*", ""),
                    ),
                ),
            ),
        )

    def __init__(
        self,
        string: str | None = None,
        returns: bool = False,
        ret_description_missing: bool = False,
    ) -> None:
        super().__init__()
        self._string = string
        self._returns = returns
        self._ret_description_missing = ret_description_missing

    @classmethod
    def from_ast(cls, node: _ast.Const) -> Docstring:
        """Build Docstring from the function's docstring AST node.

        :param node: Const node holding the docstring string.
        :return: Docstring with args and return flag.
        """
        indent_anomaly = cls._indent_anomaly(node.value)
        string = cls._normalize_docstring(node.value)
        # todo: we can start building return objects for more detailed
        # todo: checks that are in common with the params class
        match = _re.search(
            ":(?:returns?|yields?):(.*)?",
            string,
            _re.IGNORECASE,
        )
        returns = bool(match)
        ret_description_missing = False
        if match:
            ret_description_missing = not match.group(1)

        docstring = cls(string, returns, ret_description_missing)
        for match in _re.findall(
            r":([\w\s]+(?:\s\|\s[\w\s]+|\w+))([^\w\s])((?:.|\n)*?)(?=\n:|$)",
            string,
        ):
            if match:
                types = match[0].split()
                if types:
                    docstring.args.append(
                        Param(
                            DocType.from_str(types[0]),
                            UNNAMED if len(types) == 1 else types[-1],
                            match[2] or None,
                            int(indent_anomaly),
                            match[1],
                        ),
                    )

        return docstring

    @property
    def string(self) -> str | None:
        """Raw docstring text after normalization, or None."""
        return self._string

    @property
    def bare(self) -> bool:
        """True if docstring exists but has no params and no return.

        Used when the function has a docstring but documents nothing.
        """
        return self._string is not None and not self._args and not self.returns

    @property
    def ret_description_missing(self) -> bool:
        """True if a return section exists but has no description."""
        return self._ret_description_missing
