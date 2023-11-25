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
