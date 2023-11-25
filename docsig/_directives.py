"""
docsig._disable
===============
"""
from __future__ import annotations as _

import re as _re
import tokenize as _tokenize
import typing as _t
from io import StringIO as _StringIO

from typing_extensions import Self as _Self

from ._message import Message as _Message
from .messages import E as _E


class _Rules(_t.List[_Message]):
    def __init__(self, kind: str) -> None:
        super().__init__()
        self._unknown = []
        self._kind = kind
        delimiter = _re.search(r"\W+", kind)
        if delimiter and delimiter[0] == "=":
            self._kind, option = kind.split("=")
            message = _E.fromref(option)
            if "," in option:
                values = option.split(",")
                for value in values:
                    message = _E.fromref(value)
                    if message.isknown:
                        self.append(message)
                    else:
                        self._unknown.append(message)
            elif message.isknown:
                self.append(message)
            else:
                self._unknown.append(message)
        else:
            self.extend(_E.all(1))

    @property
    def kind(self) -> str:
        """The type of the directive these rules belong to."""
        return self._kind

    @property
    def unknown(self) -> list[_Message]:
        """List of unknown directive options if any."""
        return self._unknown


class Directive:
    """Represents a comment directive.

    :param kind: The type of this directive.
    :param col: The column this directive is positioned at.
    """

    _valid_kinds = "enable", "disable"

    def __init__(self, kind: str, col: int) -> None:
        self._ismodule = col == 0
        self._rules = _Rules(kind)
        self._kind = self._rules.kind

    @property
    def kind(self) -> str:
        """The type of this directive."""
        return self._kind

    @property
    def isvalid(self) -> bool:
        """Whether this directive is valid or not."""
        return self._kind in self._valid_kinds

    @property
    def rules(self) -> _Rules:
        """The rules, if any, associated with this directive."""
        return self._rules

    @property
    def ismodule(self) -> bool:
        """Whether this is a module level directive or not."""
        return self._ismodule

    @property
    def enable(self) -> bool:
        """Whether this is a enable directive or not."""
        return self._kind == self._valid_kinds[0]

    @property
    def disable(self) -> bool:
        """Whether this is a disable directive or not."""
        return self._kind == self._valid_kinds[1]

    @classmethod
    def parse(cls, comment: str, col: int) -> _Self | None:
        """Parse string into directive object if possible.

        :param comment: Comment to parse.
        :param col: Column of comment to instantiate directive.
        :return: Instantiated directive object if valid directive or
            None if not a valid directive.
        """
        if comment[1:].strip().startswith(f"{__package__}:"):
            return cls(comment.split(":")[1].strip(), col)

        return None


class Directives(
    _t.Dict[int, _t.Tuple[_t.List[Directive], _t.List[_Message]]]
):
    """Data for directives:

    Dict like object with the line number of directive as the key and
    total errors which are excluded from function checks.

    :param text: Python code.
    :param disable: List of checks to disable.
    """

    def __init__(self, text: str, disable: list[_Message]) -> None:
        super().__init__()
        fin = _StringIO(text)
        module_disables = list(disable)
        module_directives: list[Directive] = []
        directive = None
        for line in _tokenize.generate_tokens(fin.readline):
            if line.type in (_tokenize.NAME, _tokenize.OP, _tokenize.DEDENT):
                continue

            lineno, col = line.start
            if line.type == _tokenize.COMMENT:
                # ensure previous directive as backup assignment because
                # if this is just a regular comment it will override a
                # valid module directive, making it None
                directive = Directive.parse(line.string, col) or directive
                if directive is not None:
                    update_directives = [directive] + module_directives
                    update = module_disables
                    if directive.isvalid:
                        if directive.disable:
                            update = directive.rules + module_disables
                        elif directive.enable:
                            update = [
                                i
                                for i in module_disables
                                if i not in directive.rules
                            ]

                    if directive.ismodule:
                        module_disables = update
                        module_directives = update_directives
                    else:
                        self[lineno] = update_directives, update

            if lineno not in self:
                self[lineno] = list(module_directives), list(module_disables)
