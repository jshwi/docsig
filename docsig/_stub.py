"""
docsig._stub
============

Stub types for parsed docstrings and signatures.
"""

from __future__ import annotations as _

import inspect as _inspect
import re as _re
import typing as _t
from collections import Counter as _Counter
from dataclasses import dataclass as _dataclass
from enum import Enum as _Enum

import astroid as _ast

from ._config import Ignore as _Ignore
from ._vendor.sphinx.ext import napoleon as _s

# no function will accidentally have this name
UNNAMED = "-1000"

# an example of valid parameter description
VALID_DESCRIPTION = " A valid description."

# annotations meaning the function never returns a value, treated the
# same as ``-> None`` for documentation purposes
_NO_RETURN = ("NoReturn", "Never")

#: a word in a param field after the leading keyword: a (possibly
#: starred) name or type expression, in which ``. , | [ ]`` join word
#: characters so types such as ``list[str]``, ``t.Any``, ``int|str``,
#: and the split words of ``dict[str, int]`` hold together; a trailing
#: ``,`` or bracket belongs to a bracketed type, while a trailing ``.``
#: or ``|`` stays outside the word so it is still read as a bad
#: closing token
_FIELD_WORD = r"(?:\\?\*){0,2}\w+(?:[.,|\[\]]+\w+)*[,\[\]]*"

#: a ``..`` directive and its indented block, which may be indented
#: arbitrarily and so never counts as a param indent anomaly
_DIRECTIVE = _re.compile(r"^[ \t]*\.\..*\n(?:[ \t]+.*\n)*", _re.MULTILINE)

#: an rst field such as ``:param:``, marking a docstring as already rst
_RST_FIELD = _re.compile(r"^:\w+", _re.MULTILINE)

#: a numpy section header such as ``Returns`` underlined with dashes
_NUMPY_SECTION = _re.compile(
    r"^(Parameters|Other Parameters|Returns|Yields|Raises|"
    r"See Also|Notes|Examples|Attributes|Methods)\n"
    r"\s*-{3,}\s*$",
    _re.MULTILINE,
)

#: a Google section header such as ``Args:``
_GOOGLE_SECTION = _re.compile(
    r"^(Args|Arguments|Keyword Args|Keyword Arguments|Parameters|"
    r"Returns|Yields|Raises|Attributes|Example|Examples):\s*$",
    _re.MULTILINE,
)

#: a return field such as ``:return:``, capturing its description
_RETURN_FIELD = _re.compile(
    r"^[ \t]*:(?:returns?|yields?|rtype):\s*(.*)",
    _re.IGNORECASE | _re.MULTILINE,
)

#: a param field such as ``:param name: description``, in three groups:
#: the keyword with the (possibly starred) name, the token closing the
#: name (a colon when written correctly), and the description running
#: up to the next field or the end of the docstring
# the suggestion is broken
# noinspection RegExpSingleCharAlternation
_PARAM_FIELD = _re.compile(
    r"^[ \t]*:((?:\\?\*){0,2}[\w]+"
    rf"(?:\s+{_FIELD_WORD}|"
    rf"\s\|\s{_FIELD_WORD})*)"
    r"([^\w\s\\*])"
    r"((?:.|\n)*?)(?=\n[ \t]*:|\Z)",
    _re.MULTILINE,
)


class RetType(_Enum):
    """Possible kinds of return annotation."""

    NONE = 1
    SOME = 2
    UNTYPED = 3

    @staticmethod
    def _annotates_none(returns: _ast.nodes.NodeNG | None) -> bool:
        if isinstance(returns, _ast.nodes.Const):
            return returns.value is None

        if isinstance(returns, _ast.nodes.Name):
            return returns.name in _NO_RETURN

        if isinstance(returns, _ast.nodes.Attribute):
            return returns.attrname in _NO_RETURN

        return False

    @classmethod
    def from_ast(cls, returns: _ast.nodes.NodeNG | None) -> RetType:
        """Build return type from the function's return AST node.

        :param returns: Return annotation AST node or None.
        :return: RetType.NONE, RetType.SOME, or RetType.UNTYPED.
        """
        if cls._annotates_none(returns):
            return cls.NONE

        annotation_nodes = (
            _ast.nodes.Const,
            _ast.nodes.Name,
            _ast.nodes.Attribute,
            _ast.nodes.Subscript,
            _ast.nodes.BinOp,
        )
        if isinstance(returns, annotation_nodes):
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


@_dataclass(frozen=True, eq=False)
class Param:
    """Single parameter from a docstring or function signature.

    Two params are equal if they share a (non-None) name, or if both
    are ``**kwargs``, which match regardless of how they are named.

    :param kind: The type of the parameter.
    :param name: Parameter name.
    :param description: Optional description text.
    :param indent: Indent width in spaces.
    :param closing_token: Token after the name (colon by default).
    """

    kind: DocType = DocType.PARAM
    name: str | None = None
    description: str | None = None
    indent: int = 0
    closing_token: str = ":"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Param) and (
            self.kind == other.kind == DocType.KWARG
            or (self.name is not None and self.name == other.name)
        )

    @property
    def isprotected(self) -> bool:
        """True if the parameter name starts with an underscore."""
        return str(self.name).startswith("_")


# single return from a docstring or function signature
class _Return(_t.NamedTuple):
    returns: bool = False
    type: RetType = RetType.UNTYPED
    description_missing: bool = False


class Params(list[Param]):
    """A list-like collection of params.

    Appends are filtered: protected params, and param kinds the
    configuration says to ignore, are silently dropped.

    :param ignore: Configuration object for what to ignore.
    """

    def __init__(self, ignore: _Ignore) -> None:
        super().__init__()
        self._ignore = ignore

    def _accepts(self, value: Param) -> bool:
        if value.isprotected:
            return False

        if value.kind == DocType.ARG:
            return not self._ignore.args

        if value.kind == DocType.KWARG:
            # only one **kwargs can exist, so only the first is kept
            return not self._ignore.kwargs and not any(
                i.kind == DocType.KWARG for i in self
            )

        return value.kind == DocType.PARAM

    def append(self, value: Param) -> None:
        if self._accepts(value):
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
        return any(v > 1 for v in _Counter(i.name for i in self).values())


class _Stub:
    def __init__(
        self,
        returns: _Return | None = None,
        ignore: _Ignore | None = None,
    ) -> None:
        self._args = Params(ignore or _Ignore())
        self._returns = returns or _Return()

    @property
    def args(self) -> Params:
        """Params for this stub (signature or docstring)."""
        return self._args

    @property
    def returns(self) -> _Return:
        """True if a return (or yield) is declared or documented."""
        return self._returns


class Signature(_Stub):
    """Parsed function signature (args and return type)."""

    @classmethod
    def from_ast(
        cls,
        node: _ast.nodes.FunctionDef,
        ignore: _Ignore,
        skip_bound_arg: bool = False,
    ) -> Signature:
        """Build Signature from a function or class AST node.

        :param node: AST node (function, class, or module).
        :param ignore: Configuration object for what to ignore.
        :param skip_bound_arg: Drop the first positional argument (self
            or cls) without mutating the AST node.
        :return: Signature with args and return type.
        """
        rettype = RetType.from_ast(node.returns)
        returns = _Return(rettype == RetType.SOME, rettype)
        signature = cls(returns, ignore)
        posonlyargs = list(node.args.posonlyargs)
        if node.args.args is not None:
            args = list(node.args.args)
            if skip_bound_arg:
                if posonlyargs:
                    posonlyargs = posonlyargs[1:]
                elif args:
                    args = args[1:]

            # noinspection PyUnresolvedReferences
            for i in [
                a if isinstance(a, Param) else Param(name=a.name)
                for a in [
                    *posonlyargs,
                    *args,
                    Param(DocType.ARG, name=node.args.vararg),
                    *node.args.kwonlyargs,
                    Param(DocType.KWARG, name=node.args.kwarg),
                ]
                if a is not None and a.name
            ]:
                signature.args.append(i)

        return signature

    def overload(self, rettype: RetType) -> None:
        """Set this signature's return type (for overloads).

        :param rettype: Return type for the overloaded variant.
        """
        self._returns = _Return(rettype != RetType.NONE, rettype)


class Docstring(_Stub):
    """Parsed function docstring (params and return section).

    :param string: Raw docstring text after normalization.
    :param returns: True if a return or yield section is present.
    """

    @staticmethod
    def _indent_anomaly(string: str) -> bool:
        string = _DIRECTIVE.sub("", string)
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
    def _docstring_style(string: str) -> str:
        # prefer existing rst fields over napoleon section headers
        if _RST_FIELD.search(string):
            return "rst"

        if _NUMPY_SECTION.search(string):
            return "numpy"

        if _GOOGLE_SECTION.search(string):
            return "google"

        return "rst"

    @staticmethod
    def _normalize_docstring(string: str) -> str:
        # convert Google or numpy style to rst when detected
        # leave rst (including field lists) unchanged
        string = _inspect.cleandoc(string)
        style = Docstring._docstring_style(string)
        if style == "google":
            return str(_s.GoogleDocstring(string))  # type: ignore

        if style == "numpy":
            return str(_s.NumpyDocstring(string))  # type: ignore

        return string

    def __init__(
        self,
        string: str | None = None,
        returns: _Return | None = None,
    ) -> None:
        super().__init__(returns)
        self._string = string

    @classmethod
    def from_ast(cls, node: _ast.Const) -> Docstring:
        """Build Docstring from the function's docstring AST node.

        :param node: Const node holding the docstring string.
        :return: Docstring with args and return flag.
        """
        indent_anomaly = cls._indent_anomaly(node.value)
        string = cls._normalize_docstring(node.value)
        match = _RETURN_FIELD.search(string)
        returns = _Return(
            bool(match),
            description_missing=not match or not match.group(1),
        )
        docstring = cls(string, returns)
        for match in _PARAM_FIELD.findall(string):
            if match:
                kinds = match[0].split()
                if kinds:
                    name = None
                    if len(kinds) > 1:
                        # drop * / ** / napoleon-escaped stars on the name
                        name = kinds[-1].lstrip("\\*")
                    docstring.args.append(
                        Param(
                            DocType.from_str(kinds[0]),
                            UNNAMED if name is None else name,
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
        return (
            self._string is not None
            and not self._args
            and not self.returns.returns
        )
