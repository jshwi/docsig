"""
docsig.messages
===============
"""

from __future__ import annotations

import typing as _t

#: Error code for unknown errors.
UNKNOWN = "SIG000"

#: Default template to format message strings.
TEMPLATE = "{ref}: {description} ({symbolic})"

#: Flake8 template to format message strings.
FLAKE8 = "{ref} {description} ({symbolic})"


class Message(_t.NamedTuple):
    """Represents an error message."""

    #: An error code the message can be referenced by.
    ref: str

    #: A description of the error.
    description: str

    #: A shortened description that the message can be referenced by.
    symbolic: str = ""

    #: A hint, if any, suggesting why the error may have occurred.
    hint: _t.Optional[str] = None

    @property
    def isknown(self) -> bool:
        """Whether this is a known error.

        This might exist due to a typo or an attempt to retrieve an
        error that does not exist.
        """
        return self.ref != UNKNOWN

    def fstring(self, template: str) -> str:
        """Return message values as a string.

        :param template: String to interpolate values.
        :return: Formatted string.
        """
        return template.format(
            ref=self.ref,
            description=self.description,
            symbolic=self.symbolic,
        )


class Messages(_t.List[Message]):
    """List of messages."""


class MessageMap(_t.Dict[int, Message]):
    """Messages mapped under an integer version of their codes."""

    def from_ref(self, ref: str) -> Message:
        """Get a message by its code or symbolic reference.

        :param ref: Code or symbolic reference.
        :return: Message if valid ref else an unknown message type.
        """
        for value in self.values():
            if ref in (value.ref, value.symbolic):
                return value

        return Message(UNKNOWN, ref)

    def from_codes(self, refs: list[str]) -> Messages:
        """Get the list of message types from codes or symbolic refs.

        :param refs: List of codes or symbolic references.
        :return: List of message types.
        """
        return Messages(self.from_ref(i) for i in refs)

    @property
    def all(self) -> Messages:
        """Get all messages that aren't a config error."""
        return Messages(v for k, v in self.items() if len(str(k)) > 1)


# SIGxxx: Error
E = MessageMap(
    {
        #: SIG0xx Config
        1: Message(
            "SIG001",
            "unknown module comment directive '{directive}'",
            "unknown-module-directive",
        ),
        2: Message(
            "SIG002",
            "unknown inline comment directive '{directive}'",
            "unknown-inline-directive",
        ),
        3: Message(
            "SIG003",
            "unknown module comment option for {directive} '{option}'",
            "unknown-module-directive-option",
        ),
        4: Message(
            "SIG004",
            "unknown inline comment option for {directive} '{option}'",
            "unknown-inline-directive-option",
        ),
        5: Message(
            "SIG005",
            "both mutually exclusive class options configured",
            "mutually-exclusive-options",
        ),
        #: SIG1xx Missing
        101: Message(
            "SIG101",
            "function is missing a docstring",
            "function-doc-missing",
        ),
        102: Message(
            "SIG102",
            "class is missing a docstring",
            "class-doc-missing",
        ),
        #: SIG2xx Signature
        201: Message(
            "SIG201",
            "duplicate parameters found",
            "duplicate-params-found",
        ),
        202: Message(
            "SIG202",
            "includes parameters that do not exist",
            "params-do-not-exist",
        ),
        203: Message(
            "SIG203",
            "parameters missing",
            "params-missing",
        ),
        #: SIG3xx Parameters
        301: Message(
            "SIG301",
            "description missing from parameter",
            "description-missing",
        ),
        302: Message(
            "SIG302",
            "syntax error in description",
            "syntax-error-in-description",
        ),
        303: Message(
            "SIG303",
            "parameter appears to be incorrectly documented",
            "param-incorrectly-documented",
        ),
        304: Message(
            "SIG304",
            "bad token used to close parameter declaration '{token}'",
            "bad-closing-token",
            "close a parameter declaration with ':'",
        ),
        305: Message(
            "SIG305",
            "description does not begin with a capital letter",
            "description-not-capitalized",
        ),
        #: SIG4xx Description
        401: Message(
            "SIG401",
            "param not indented correctly",
            "incorrect-indent",
        ),
        402: Message(
            "SIG402",
            "parameters out of order",
            "params-out-of-order",
        ),
        403: Message(
            "SIG403",
            "spelling error found in documented parameter",
            "spelling-error",
        ),
        404: Message(
            "SIG404",
            "documented parameter not equal to its respective argument",
            "param-not-equal-to-arg",
        ),
        #: SIG5xx Returns
        501: Message(
            "SIG501",
            "cannot determine whether a return statement should exist",
            "confirm-return-needed",
            "annotate type to indicate whether return documentation needed",
        ),
        502: Message(
            "SIG502",
            "return statement documented for None",
            "return-documented-for-none",
        ),
        503: Message(
            "SIG503",
            "return missing from docstring",
            "return-missing",
            "it is possible a syntax error could be causing this",
        ),
        504: Message(
            "SIG504",
            "return statement documented for class",
            "class-return-documented",
            "a class does not return a value during instantiation",
        ),
        505: Message(
            "SIG505",
            "return statement documented for property",
            "return-documented-for-property",
            "documentation is sufficient as a getter is the value returned",
        ),
        506: Message(
            "SIG506",
            "description missing from return",
            "return-description-missing",
        ),
        #: SIG9xx Error
        901: Message(
            "SIG901",
            "parsing python code failed",
            "invalid-syntax",
        ),
        902: Message(
            "SIG902",
            "failed to read file",
            "unicode-decode-error",
        ),
    },
)
