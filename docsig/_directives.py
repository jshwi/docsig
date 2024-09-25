"""
docsig._directives
==================
"""

from __future__ import annotations as _

import tokenize as _tokenize
import typing as _t
from io import StringIO as _StringIO

from .messages import E as _E
from .messages import Messages as _Messages


class Comment(_Messages):
    """Represents a comment directive.

    :param string: Text to construct comment from.
    :param col: The column this directive is positioned at.
    """

    _valid_kinds = "enable", "disable"

    def __init__(self, string: str, col: int) -> None:
        super().__init__()
        self._ismodule = col == 0
        parts = string.split("=")
        self._kind = parts[0]
        if len(parts) == 1:
            self.extend(_E.all)
        else:
            self.extend(_E.from_ref(i) for i in parts[1].split(","))

    @property
    def kind(self) -> str:
        """The type of this directive."""
        return self._kind

    @property
    def isvalid(self) -> bool:
        """Whether this directive is valid or not."""
        return self._kind in self._valid_kinds

    @property
    def ismodule(self) -> bool:
        """Whether this is a module level directive or not."""
        return self._ismodule

    @property
    def enable(self) -> bool:
        """Whether this is an enable directive or not."""
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


class Comments(_t.List[Comment]):
    """List of comments."""


class Directives(_t.Dict[int, _t.Tuple[Comments, _Messages]]):
    """Data for directives:

    Dict like object with the line number of directive as the key a
    tuple containing comments and messages.

    Comments can be either disable or enable comments, and messages are
    what messages are to be disabled.

    Comments influence what messages can be added to the list, but are
    different in that they communicate the directive, but the messages
    are the final product of messages to disable.

    Comments are collected here for later analysis.
    """

    @classmethod
    def from_text(cls, text: str, messages: _Messages) -> Directives:
        """Create directives from text.

        :param text: Python code.
        :param messages: List of checks to disable.
        :return: Instantiated directives object.
        """
        directives = cls()
        fin = _StringIO(text)
        comments = Comments()
        for line in _tokenize.generate_tokens(fin.readline):
            # do nothing for these lines types
            if line.type in (_tokenize.NAME, _tokenize.OP, _tokenize.DEDENT):
                continue

            # inherit the comments and messages defined in the global
            # scope, but do not update the global comments and messages
            # unless it is confirmed that the comment is a module level
            # directive
            scoped_comments = Comments(comments)
            scoped_messages = _Messages(messages)
            lineno, col = line.start
            if line.type == _tokenize.COMMENT:
                comment = Comment.parse(line.string, col)
                if comment is not None:
                    scoped_comments.append(comment)
                    if comment.disable:
                        scoped_messages.extend(comment)
                    elif comment.enable:
                        scoped_messages = _Messages(
                            i for i in messages if i not in comment
                        )

                    # if module level directive then make changes
                    # globally
                    if comment.ismodule:
                        messages = scoped_messages
                        comments = scoped_comments

            # check that a scoped message has not updated this first, as
            # they take precedence over global messages
            if lineno not in directives:
                directives[lineno] = scoped_comments, scoped_messages

        return directives
