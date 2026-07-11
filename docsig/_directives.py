"""
docsig._directives
==================

Parsing and storage for docsig comment directives.
"""

from __future__ import annotations as _

import tokenize as _tokenize
from io import StringIO as _StringIO

from .messages import E as _E
from .messages import Messages as _Messages


class Comments(list["Comment"]):
    """List of comments."""


class Comment(_Messages):
    """A single comment directive.

    :param string: Text to construct the directive from.
    :param col: Column for directive (0 means module-level).
    """

    _valid_kinds = "enable", "disable"
    _valid_flags = ("next",)

    def __init__(self, string: str, col: int) -> None:
        super().__init__()
        self._ismodule = col == 0
        parts = string.split("=")
        subparts = parts[0].split("-")
        self._kind = subparts[0]
        self._flag = None if len(subparts) == 1 else subparts[1]
        self._isnext = self._flag == "next"

        # if the flag is not valid, the preceding directive is not valid
        # either
        # at first it seems like the directive should be valid, i.e.
        # `docsig: disable-next: SIG101` should still at least disable
        # `SIG101`, but this causes more problems than it solves, at the
        # module level
        # disabling the check for the whole file is likely
        # unexpected, confusing, and the opposite of what was intended
        # better not disable the commented function than disable the
        # whole file
        # note that no directive flag at all is still a valid flag
        if self.isvalidflag:
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

    @property
    def isnext(self) -> bool:
        """Whether this directive applies to the next line only."""
        return self._isnext

    @property
    def isvalidflag(self) -> bool:
        """Whether the directive flag (if any) is valid."""
        return self._flag is None or self._flag in self._valid_flags

    @property
    def flag(self) -> str | None:
        """Flag for this directive (e.g. next), or None."""
        return self._flag

    @classmethod
    def parse(cls, comment: str, col: int) -> Comment | None:
        """Parse a comment into a docsig directive when present.

        :param comment: Raw comment text from the tokenizer.
        :param col: Column at which the comment appears.
        :return: Comment instance if valid; None otherwise.
        """
        if comment[1:].strip().startswith(f"{__package__}:"):
            return cls(comment.split(":", maxsplit=1)[1].strip(), col)

        return None


class Directives(dict[int, tuple[Comments, _Messages]]):
    """Map line number to comments and disabled messages for that line.

    Keys are line numbers; values are tuples of comment directives and
    the messages to disable at that line. Used when running checks to
    respect inline and module-level docsig enable/disable directives.
    """

    @classmethod
    def from_text(  # pylint: disable=too-many-locals
        cls,
        text: str,
        messages: _Messages,
    ) -> Directives:
        """Build a directives map from docsig directives in the code.

        :param text: Python source code to scan for directives.
        :param messages: Initial list of messages to disable.
        :return: Directives instance keyed by line number.
        """
        directives = cls()
        fin = _StringIO(text)
        comments = Comments()
        enable_next = False
        next_comments = Comments(comments)
        next_messages = _Messages(messages)
        pending_inline: tuple[Comments, _Messages] | None = None
        pending_inline_lineno: int | None = None
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

                    # if directive has a 'next' flag then alter the
                    # module level scope, not the inline scope (which
                    # behaves similar to next), so that inline
                    # directives are included and not overwritten
                    if comment.isnext and not enable_next:
                        enable_next = True
                        next_comments = Comments(comments)
                        next_messages = _Messages(messages)

                    # if module level directive, then make changes
                    # globally
                    if comment.ismodule:
                        comments = scoped_comments
                        messages = scoped_messages
                    else:
                        # keep disable on this line even if an earlier
                        # token already recorded an empty entry (e.g.
                        # a string arg before an inline comment)
                        directives[lineno] = (
                            Comments(scoped_comments),
                            _Messages(scoped_messages),
                        )

                        # defer scoped state for the next line without
                        # changing module-level messages
                        pending_inline = (
                            Comments(scoped_comments),
                            _Messages(scoped_messages),
                        )
                        pending_inline_lineno = lineno

            # if in a 'next' module level scope and the line type is a
            # newline (not a comment to allow 'next' directives to be
            # stacked) then leave the 'next' module level scope and
            # reset the global messages to before the 'next' directive
            elif enable_next and line.type != _tokenize.NL:
                enable_next = False
                comments = next_comments
                messages = next_messages

            # inherit deferred inline scope on the first line after
            # the comment (e.g. an indented def on the following line)
            if (
                pending_inline is not None
                and pending_inline_lineno is not None
                and lineno > pending_inline_lineno
            ):
                scoped_comments, scoped_messages = pending_inline
                pending_inline = None
                pending_inline_lineno = None

            # check that a scoped message has not updated this first, as
            # they take precedence over global messages
            if lineno not in directives:
                directives[lineno] = scoped_comments, scoped_messages

        return directives
