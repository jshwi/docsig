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

#: scope for one line: the directive comments applying to the line
#: paired with the messages they leave disabled
_Scope = tuple["Comments", _Messages]


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

    Three scopes interact while scanning:

    * module scope - column-zero directives, applying to every line
        that follows
    * 'next' scope - a module directive flagged 'next' applies until
        the following statement, then module scope is restored from a
        snapshot taken at the directive
    * inline scope - an indented directive, applying from its own line
        until the statement it annotates ends; blank lines and further
        comments in between do not end that reach, and consecutive
        directives stack rather than replacing one another

    :param messages: Initial list of messages to disable.
    """

    def __init__(self, messages: _Messages) -> None:
        self._directives = Directives()
        self._comments = Comments()
        self._messages = _Messages(messages)

        # module scope from before a 'next' directive, to restore after
        # the next statement
        self._next_scope: _Scope | None = None

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
        for token in _tokenize.generate_tokens(_StringIO(text).readline):
            # nothing can change scope on these token types
            if token.type not in (
                _tokenize.NAME,
                _tokenize.OP,
                _tokenize.DEDENT,
            ):
                self._visit(token)

    def _visit(self, token: _tokenize.TokenInfo) -> None:
        lineno, col = token.start

        # inherit the comments and messages defined in the module
        # scope; module state is only updated if the comment turns out
        # to be a module-level directive
        scope: _Scope = Comments(self._comments), _Messages(self._messages)
        if token.type == _tokenize.COMMENT:
            comment = Comment.parse(token.string, col)
            if comment is not None:
                scope = self._apply(comment, lineno, scope)

        elif self._next_scope is not None and token.type != _tokenize.NL:
            # a statement ends a 'next' directive: restore the module
            # scope from before the directive
            # the scope copied above still carries the directive, so it
            # applies to this line alone
            # comments are excluded so 'next' directives can be stacked
            self._comments, self._messages = self._next_scope
            self._next_scope = None

        # an indented directive reaches the statement it annotates
        # across any blank or comment lines between the two
        if self._pending_inline is not None:
            _, pending_comments, pending_messages = self._pending_inline
            scope = Comments(pending_comments), _Messages(pending_messages)

        # the first entry recorded for a line wins, unless an inline
        # directive already claimed the line in _apply
        self._directives.setdefault(lineno, scope)
        self._end_pending_inline(lineno, token.type)

    def _apply(self, comment: Comment, lineno: int, scope: _Scope) -> _Scope:
        if not comment.ismodule and self._pending_inline is not None:
            # stack onto an indented directive that is still waiting
            # for its statement, so neither directive is lost, the way
            # module directives already accumulate
            _, pending_comments, pending_messages = self._pending_inline
            scope = Comments(pending_comments), _Messages(pending_messages)

        comments, messages = scope
        comments.append(comment)
        if comment.disable:
            messages.extend(comment)

        elif comment.enable:
            messages = _Messages(i for i in self._messages if i not in comment)

        if comment.isnext and self._next_scope is None:
            # save module scope from before the directive so it can be
            # restored after the next statement
            # stacked 'next' directives keep the first snapshot
            self._next_scope = (
                Comments(self._comments),
                _Messages(self._messages),
            )

        if comment.ismodule:
            self._comments = comments
            self._messages = messages
        else:
            # keep disable on this line even if an earlier token
            # already recorded an empty entry (e.g. a string arg before
            # an inline comment)
            self._directives[lineno] = Comments(comments), _Messages(messages)

            # defer this scope to the following line without changing
            # module scope
            self._pending_inline = (
                lineno,
                Comments(comments),
                _Messages(messages),
            )

        return comments, messages

    def _end_pending_inline(self, lineno: int, kind: int) -> None:
        # the end of a statement on a line after the directive ends its
        # reach; a directive written on the code line itself ends at
        # the following statement instead, so its own line is excluded
        if (
            self._pending_inline is not None
            and kind == _tokenize.NEWLINE
            and lineno > self._pending_inline[0]
        ):
            self._pending_inline = None


class Directives(dict[int, _Scope]):
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
