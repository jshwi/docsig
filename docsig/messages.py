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
            if ref in (value.code, value.symbolic):
                return value

        return Message(UNKNOWN, ref)

    def from_codes(self, refs: list[str]) -> Messages:
        """Get list of message types from codes or symbolic references.

        :param refs: List of codes or symbolic references.
        :return: List of message types.
        """
        return Messages(self.from_ref(i) for i in refs)

    def all(self, category: int) -> Messages:
        """Get all messages belonging to a category.

        :param category: Index of message category.
        :return: List of all message objects belonging to category.
        """
        return Messages(
            v for k, v in self.items() if str(k).startswith(str(category))
        )


# Exxx: Error
E = MessageMap(
    {
        # E1xx: Docstring
        101: Message(
            "E101",
            "parameters out of order",
            "params-out-of-order",
        ),
        102: Message(
            "E102",
            "includes parameters that do not exist",
            "params-do-not-exist",
        ),
        103: Message(
            "E103",
            "parameters missing",
            "params-missing",
        ),
        104: Message(
            "E104",
            "return statement documented for None",
            "return-documented-for-none",
        ),
        105: Message(
            "E105",
            "return missing from docstring",
            "return-missing",
            "it is possible a syntax error could be causing this",
        ),
        106: Message(
            "E106",
            "duplicate parameters found",
            "duplicate-params-found",
        ),
        107: Message(
            "E107",
            "parameter appears to be incorrectly documented",
            "param-incorrectly-documented",
        ),
        108: Message(
            "E108",
            "return statement documented for property",
            "return-documented-for-property",
            "documentation is sufficient as a getter is the value returned",
        ),
        109: Message(
            "E109",
            "cannot determine whether a return statement should exist",
            "confirm-return-needed",
            "annotate type to indicate whether return documentation needed",
        ),
        110: Message(
            "E110",
            "documented parameter not equal to its respective argument",
            "param-not-equal-to-arg",
        ),
        111: Message(
            "E111",
            "return statement documented for class",
            "class-return-documented",
            "a class does not return a value during instantiation",
        ),
        112: Message(
            "E112",
            "spelling error found in documented parameter",
            "spelling-error",
        ),
        113: Message(
            "E113",
            "function is missing a docstring",
            "function-doc-missing",
        ),
        114: Message(
            "E114",
            "class is missing a docstring",
            "class-doc-missing",
        ),
        115: Message(
            "E115",
            "syntax error in description",
            "syntax-error-in-description",
        ),
        116: Message(
            "E116",
            "param not indented correctly",
            "incorrect-indent",
        ),
        117: Message(
            "E117",
            "description missing from parameter",
            "description-missing",
        ),
        # E2xx: Config
        201: Message(
            "E201",
            "unknown module comment directive '{directive}'",
            "unknown-module-directive",
        ),
        202: Message(
            "E202",
            "unknown inline comment directive '{directive}'",
            "unknown-inline-directive",
        ),
        203: Message(
            "E203",
            "unknown module comment option for {directive} '{option}'",
            "unknown-module-directive-option",
        ),
        204: Message(
            "E204",
            "unknown inline comment option for {directive} '{option}'",
            "unknown-inline-directive-option",
        ),
    }
)
