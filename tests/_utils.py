"""
tests._utils
============
"""
# pylint: disable=too-few-public-methods
from docsig import messages

#: Error message codes.
errors = [
    i for i in dir(messages) if not i.startswith("__") and i.startswith("E")
]


#: Hint message codes.
hints = [
    i for i in dir(messages) if not i.startswith("__") and i.startswith("H")
]


class DummyFunc:
    """Mock `docsig._function.Function` object."""

    def __init__(self) -> None:
        self.isinit = True
        self.isproperty = True
