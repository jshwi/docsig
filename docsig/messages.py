"""
docsig.messages
===============

Error message definitions (Message, MessageMap, E) and format templates
for docstring-check output.
"""

from __future__ import annotations as _

import typing as _t

#: Error code for unknown errors.
UNKNOWN = "SIG000"

#: Default template to format message strings.
TEMPLATE = "{ref}: {description} ({symbolic})"

#: Flake8 template to format message strings.
FLAKE8 = "{ref} {description} ({symbolic})"

NEW = """\
{ref} is a new violation and will error in a future version\
"""


class Message(_t.NamedTuple):
    """One docstring-check error (ref, description, symbolic, hint)."""

    #: An error code the message can be referenced by.
    ref: str

    #: A description of the error.
    description: str

    #: A shortened description that the message can be referenced by.
    symbolic: str = ""

    #: A hint, if any, suggesting why the error may have occurred.
    hint: _t.Optional[str] = None

    #: Whether this message is a new addition.
    new: bool = False

    @property
    def isknown(self) -> bool:
        """True if ref is a known code, else False (typo or missing)."""
        return self.ref != UNKNOWN

    def fstring(self, template: str) -> str:
        """Format this message with the given template.

        Placeholders: ref, description, symbolic.

        :param template: Format string with ref, description, symbolic.
        :return: Formatted string.
        """
        template = f"W {template}" if self.new else template
        return template.format(
            ref=self.ref,
            description=self.description,
            symbolic=self.symbolic,
        )


class Messages(_t.List[Message]):
    """Sequence of Message instances, typically for one failure."""


class MessageMap(_t.Dict[int, Message]):
    """Mapping from integer key to Message (used for the E registry)."""

    def from_ref(self, ref: str) -> Message:
        """Return Message for the given code or symbolic ref.

        :param ref: Code (e.g. SIG101) or symbolic name.
        :return: Matching Message, or unknown if not found.
        """
        for value in self.values():
            if ref in (value.ref, value.symbolic):
                return value

        return Message(UNKNOWN, ref)

    def from_codes(self, refs: list[str]) -> Messages:
        """Return Messages for the given codes or symbolic refs.

        :param refs: Codes or symbolic names.
        :return: One Message per ref (unknown if not found).
        """
        return Messages(self.from_ref(i) for i in refs)

    @property
    def all(self) -> Messages:
        """All Messages except single-digit config errors (SIG0xx)."""
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
        6: Message(
            "SIG006",
            "unknown module comment flag for {directive} '{flag}'",
            "unknown-module-directive-flag",
        ),
        7: Message(
            "SIG007",
            "unknown inline comment flag for {directive} '{flag}'",
            "unknown-inline-directive-flag",
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
        #: SIG3xx Description
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
        306: Message(
            "SIG306",
            "description does not end in a period",
            "description-missing-period",
        ),
        #: SIG4xx Parameters
        401: Message(
            "SIG401",
            "parameter not indented correctly",
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
