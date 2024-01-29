"""
docsig._message
===============
"""

from __future__ import annotations as _

import typing as _t

UNKNOWN = "E000"


class Message(_t.NamedTuple):
    """Message type for errors."""

    code: str
    description: str
    symbolic: str = ""
    hint: _t.Optional[str] = None

    @property
    def isknown(self) -> bool:
        """Whether this is a known error."""
        return self.code != UNKNOWN

    def fstring(self, template: str) -> str:
        """Return values as a format string.

        :param template: String to interpolate values.
        :return: Formatted string.
        """
        return template.format(
            code=self.code,
            description=self.description,
            symbolic=self.symbolic,
        )


class Messages(_t.Dict[int, Message]):
    """Object for storing and retrieving message objects."""

    def fromref(self, ref: str) -> Message:
        """Get a message by its code or symbolic reference.

        :param ref: Code or symbolic reference.
        :return: Message if valid ref else an unknown message type.
        """
        for value in self.values():
            if ref in (value.code, value.symbolic):
                return value

        return Message(UNKNOWN, ref)

    def fromcodes(self, refs: list[str]) -> tuple[Message, ...]:
        """Get tuple of message types from codes or symbolic references.

        :param refs: Tuple of codes or symbolic references.
        :return: Tuple of message types.
        """
        return tuple(self.fromref(i) for i in refs)

    def all(self, category: int) -> tuple[Message, ...]:
        """Get all messages belonging to a category.

        :param category: Index of message category.
        :return: Tuple of all message objects belonging to category.
        """
        return tuple(
            v for k, v in self.items() if str(k).startswith(str(category))
        )
