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
        directive = parts[0].split("-")
        self._kind = directive[0]
        self._flag = directive[1] if len(directive) > 1 else None

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
        return self._kind == "enable"

    @property
    def disable(self) -> bool:
        """Whether this is a disable directive."""
        return self._kind == "disable"

    @property
    def isnext(self) -> bool:
        """Whether this directive applies to the next line only."""
        return self._flag == "next"

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


class _Scanner:
    """Scan source tokens for directives, tracking scope per line.

    :param messages: Initial list of messages to disable.
    """

    def __init__(self, messages: _Messages) -> None:
        self._directives = Directives()
        self._comments = Comments()
        self._messages = _Messages(messages)

        # module scope from before a 'next' directive, to restore after
        # the next statement
        self._next_scope: tuple[Comments, _Messages] | None = None

        # scope of an inline directive, deferred to the following line
        self._pending_inline: tuple[int, Comments, _Messages] | None = None

    @property
    def directives(self) -> Directives:
        """Directives collected from the scanned source."""
        return self._directives

    def scan(self, text: str) -> None:
        """Collect scope for each line of the given source.

        :param text: Python source code to scan for directives.
        """
        for line in _tokenize.generate_tokens(_StringIO(text).readline):
            # do nothing for these line types
            if line.type in (_tokenize.NAME, _tokenize.OP, _tokenize.DEDENT):
                continue

            # inherit the comments and messages defined in the module
            # scope, but do not update the module comments and messages
            # unless it is confirmed that the comment is a module level
            # directive
            scoped_comments = Comments(self._comments)
            scoped_messages = _Messages(self._messages)
            lineno, col = line.start
            if line.type == _tokenize.COMMENT:
                comment = Comment.parse(line.string, col)
                if comment is not None:
                    scoped_comments.append(comment)
                    if comment.disable:
                        scoped_messages.extend(comment)
                    elif comment.enable:
                        scoped_messages = _Messages(
                            i for i in self._messages if i not in comment
                        )

                    # if directive has a 'next' flag then save the
                    # module scope from before it, so it can be
                    # restored after the next statement
                    # stacked 'next' directives keep the first snapshot
                    if comment.isnext and self._next_scope is None:
                        self._next_scope = (
                            Comments(self._comments),
                            _Messages(self._messages),
                        )

                    # if module level directive, then make changes
                    # globally
                    if comment.ismodule:
                        self._comments = scoped_comments
                        self._messages = scoped_messages
                    else:
                        # keep disable on this line even if an earlier
                        # token already recorded an empty entry (e.g.
                        # a string arg before an inline comment)
                        self._directives[lineno] = (
                            Comments(scoped_comments),
                            _Messages(scoped_messages),
                        )

                        # defer scoped state for the next line without
                        # changing module-level messages
                        self._pending_inline = (
                            lineno,
                            Comments(scoped_comments),
                            _Messages(scoped_messages),
                        )

            # if in a 'next' module level scope and the line type is a
            # newline (not a comment to allow 'next' directives to be
            # stacked) then leave the 'next' module level scope and
            # reset the module messages to before the 'next' directive
            elif self._next_scope is not None and line.type != _tokenize.NL:
                self._comments, self._messages = self._next_scope
                self._next_scope = None

            # inherit deferred inline scope on the first line after
            # the comment (e.g. an indented def on the following line)
            if (
                self._pending_inline is not None
                and lineno > self._pending_inline[0]
            ):
                _, scoped_comments, scoped_messages = self._pending_inline
                self._pending_inline = None

            # check that a scoped message has not updated this first, as
            # they take precedence over module messages
            if lineno not in self._directives:
                self._directives[lineno] = scoped_comments, scoped_messages


class Directives(dict[int, tuple[Comments, _Messages]]):
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
        scanner = _Scanner(messages)
        scanner.scan(text)
        return scanner.directives
