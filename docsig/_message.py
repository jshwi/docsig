"""
docsig._message
===============
"""
from __future__ import annotations as _

import typing as _t


class Message(_t.NamedTuple):
    """Message type for errors."""

    code: str
    description: str
    symbolic: str = ""
    hint: _t.Optional[str] = None

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

    def all(self, category: int) -> tuple[Message, ...]:
        """Get all messages belonging to a category.

        :param category: Index of message category.
        :return: Tuple of all message objects belonging to category.
        """
        return tuple(
            v for k, v in self.items() if str(k).startswith(str(category))
        )
