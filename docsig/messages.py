"""
docsig.messages
===============
"""

from __future__ import annotations

import typing as _t

#: Error code for unknown errors.
UNKNOWN = "E000"

#: Default template to format message strings.
TEMPLATE = "{code}: {description} ({symbolic})"


class Message(_t.NamedTuple):
    """Represents an error message."""

    #: An error code the message can be referenced by.
    ref: str

    #: Legacy error code, if any, the message can be referenced by
    code: str

    #: A description of the error.
    description: str

    #: A shortened description the message can be referenced by.
    symbolic: str = ""

    #: A hint, if any, suggesting why the error may have occurred.
    hint: _t.Optional[str] = None

    @property
    def isknown(self) -> bool:
        """Whether this is a known error.

        This might exist due to a typo or an attempt to retrieve an
        error that does not exist.
        """
        return self.code != UNKNOWN

    def fstring(self, template: str) -> str:
        """Return message values as a string.

        :param template: String to interpolate values.
        :return: Formatted string.
        """
        return template.format(
            code=self.code,
            description=self.description,
            symbolic=self.symbolic,
        )


class Messages(_t.List[Message]):
    """List of messages."""


class MessageMap(_t.Dict[int, Message]):
    """Messages mapped under an integer version of their codes.."""

    def from_ref(self, ref: str) -> Message:
        """Get a message by its code or symbolic reference.

        :param ref: Code or symbolic reference.
        :return: Message if valid ref else an unknown message type.
        """
        for value in self.values():
            if ref in (value.ref, value.code, value.symbolic):
                return value

        return Message(UNKNOWN, UNKNOWN, ref)

    def from_codes(self, refs: list[str]) -> Messages:
        """Get list of message types from codes or symbolic references.

        :param refs: List of codes or symbolic references.
        :return: List of message types.
        """
        return Messages(self.from_ref(i) for i in refs)

    @property
    def all(self) -> Messages:
        """Get all messages that aren't a config error."""
        return Messages(
            v for k, v in self.items() if str(k).startswith(str(1))
        )


# SIGxxx: Error
E = MessageMap(
    {
        #: SIG0xx Config
        201: Message(
            "SIG001",
            "E201",
            "unknown module comment directive '{directive}'",
            "unknown-module-directive",
        ),
        202: Message(
            "SIG002",
            "E202",
            "unknown inline comment directive '{directive}'",
            "unknown-inline-directive",
        ),
        203: Message(
            "SIG003",
            "E203",
            "unknown module comment option for {directive} '{option}'",
            "unknown-module-directive-option",
        ),
        204: Message(
            "SIG004",
            "E204",
            "unknown inline comment option for {directive} '{option}'",
            "unknown-inline-directive-option",
        ),
        #: SIG1xx Missing
        113: Message(
            "SIG101",
            "E113",
            "function is missing a docstring",
            "function-doc-missing",
        ),
        114: Message(
            "SIG102",
            "E114",
            "class is missing a docstring",
            "class-doc-missing",
        ),
        #: SIG2xx Signature
        106: Message(
            "SIG201",
            "E106",
            "duplicate parameters found",
            "duplicate-params-found",
        ),
        102: Message(
            "SIG202",
            "E102",
            "includes parameters that do not exist",
            "params-do-not-exist",
        ),
        103: Message(
            "SIG203",
            "E103",
            "parameters missing",
            "params-missing",
        ),
        #: SIG3xx Parameters
        117: Message(
            "SIG301",
            "E117",
            "description missing from parameter",
            "description-missing",
        ),
        115: Message(
            "SIG302",
            "E115",
            "syntax error in description",
            "syntax-error-in-description",
        ),
        107: Message(
            "SIG303",
            "E107",
            "parameter appears to be incorrectly documented",
            "param-incorrectly-documented",
        ),
        #: SIG4xx Description
        116: Message(
            "SIG401",
            "E116",
            "param not indented correctly",
            "incorrect-indent",
        ),
        101: Message(
            "SIG402",
            "E101",
            "parameters out of order",
            "params-out-of-order",
        ),
        112: Message(
            "SIG403",
            "E112",
            "spelling error found in documented parameter",
            "spelling-error",
        ),
        110: Message(
            "SIG404",
            "E110",
            "documented parameter not equal to its respective argument",
            "param-not-equal-to-arg",
        ),
        #: SIG5xx Returns
        109: Message(
            "SIG501",
            "E109",
            "cannot determine whether a return statement should exist",
            "confirm-return-needed",
            "annotate type to indicate whether return documentation needed",
        ),
        104: Message(
            "SIG502",
            "E104",
            "return statement documented for None",
            "return-documented-for-none",
        ),
        105: Message(
            "SIG503",
            "E105",
            "return missing from docstring",
            "return-missing",
            "it is possible a syntax error could be causing this",
        ),
        111: Message(
            "SIG504",
            "E111",
            "return statement documented for class",
            "class-return-documented",
            "a class does not return a value during instantiation",
        ),
        108: Message(
            "SIG505",
            "E108",
            "return statement documented for property",
            "return-documented-for-property",
            "documentation is sufficient as a getter is the value returned",
        ),
    }
)
