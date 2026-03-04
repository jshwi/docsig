"""
docsig._directives
==================

Parsing and storage for docsig comment directives.
"""

from __future__ import annotations as _

import tokenize as _tokenize
import typing as _t
from io import StringIO as _StringIO

from .messages import E as _E
from .messages import Messages as _Messages


class Comment(_Messages):
    """A single comment directive.

    :param string: Text to construct the directive from.
    :param col: Column for directive (0 means module-level).
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
        """Whether this directive is valid."""
        return self._kind in self._valid_kinds

    @property
    def ismodule(self) -> bool:
        """Whether this is a module-level directive."""
        return self._ismodule

    @property
    def enable(self) -> bool:
        """Whether this is an enable directive."""
        return self._kind == self._valid_kinds[0]

    @property
    def disable(self) -> bool:
        """Whether this is a disable directive."""
        return self._kind == self._valid_kinds[1]

    @classmethod
    def parse(cls, comment: str, col: int) -> Comment | None:
        """Parse a comment into a docsig directive when present.

        :param comment: Raw comment text from the tokenizer.
        :param col: Column at which the comment appears.
        :return: Comment instance if valid; None otherwise.
        """
        if comment[1:].strip().startswith(f"{__package__}:"):
            return cls(comment.split(":")[1].strip(), col)

        return None


class Comments(_t.List[Comment]):
    """List of comments."""


class Directives(_t.Dict[int, _t.Tuple[Comments, _Messages]]):
    """Map line number to comments and disabled messages for that line.

    Keys are line numbers; values are tuples of comment directives and
    the messages to disable at that line. Used when running checks to
    respect inline and module-level docsig enable/disable directives.
    """

    @classmethod
    def from_text(cls, text: str, messages: _Messages) -> Directives:
        """Build a directives map from docsig directives in the code.

        :param text: Python source code to scan for directives.
        :param messages: Initial list of messages to disable.
        :return: Directives instance keyed by line number.
        """
        directives = cls()
        fin = _StringIO(text)
        comments = Comments()
        for line in _tokenize.generate_tokens(fin.readline):
            # do nothing for these line types
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

                    # if module level directive, then make changes
                    # globally
                    if comment.ismodule:
                        messages = scoped_messages
                        comments = scoped_comments

            # check that a scoped message has not updated this first, as
            # they take precedence over global messages
            if lineno not in directives:
                directives[lineno] = scoped_comments, scoped_messages

        return directives
