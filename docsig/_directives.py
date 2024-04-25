"""
docsig._disable
===============
"""

from __future__ import annotations as _

import re as _re
import tokenize as _tokenize
import typing as _t
from io import StringIO as _StringIO

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


class Comment:
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
    def parse(cls, comment: str, col: int) -> Comment | None:
        """Parse string into directive object if possible.

        :param comment: Comment to parse.
        :param col: Column of comment to instantiate directive.
        :return: Instantiated directive object if valid directive or
            None if not a valid directive.
        """
        if comment[1:].strip().startswith(f"{__package__}:"):
            return cls(comment.split(":")[1].strip(), col)

        return None


class Directives(_t.Dict[int, _t.Tuple[_t.List[Comment], _t.List[_Message]]]):
    """Data for directives:

    Dict like object with the line number of directive as the key and
    total errors which are excluded from function checks.

    :param text: Python code.
    :param messages: List of checks to disable.
    """

    def __init__(self, text: str, messages: list[_Message]) -> None:
        super().__init__()
        fin = _StringIO(text)
        module_messages = list(messages)
        module_comments: list[Comment] = []
        comment = None
        for line in _tokenize.generate_tokens(fin.readline):
            if line.type in (_tokenize.NAME, _tokenize.OP, _tokenize.DEDENT):
                continue

            lineno, col = line.start
            if line.type == _tokenize.COMMENT:
                # ensure previous directive as backup assignment because
                # if this is just a regular comment it will override a
                # valid module directive, making it None
                comment = Comment.parse(line.string, col) or comment
                if comment is not None:
                    update_comments = [comment] + module_comments
                    update_messages = module_messages
                    if comment.isvalid:
                        if comment.disable:
                            update_messages = comment.rules + module_messages
                        elif comment.enable:
                            update_messages = [
                                i
                                for i in module_messages
                                if i not in comment.rules
                            ]

                    if comment.ismodule:
                        module_messages = update_messages
                        module_comments = update_comments
                    else:
                        self[lineno] = update_comments, update_messages

            if lineno not in self:
                self[lineno] = list(module_comments), list(module_messages)
