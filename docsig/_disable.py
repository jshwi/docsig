"""
docsig._disable
===============
"""
from __future__ import annotations as _

import tokenize as _tokenize
import typing as _t
from io import StringIO as _StringIO

from ._report import ERRORS as _ERRORS


class Disabled(_t.Dict[int, _t.List[str]]):
    """Data for lines which are excluded from checks.

    :param text: Python code.
    :param disable: List of checks to disable.
    """

    def __init__(self, text: str, disable: list[str]) -> None:
        super().__init__()
        fin = _StringIO(text)
        module_is_disabled = False
        for line in _tokenize.generate_tokens(fin.readline):
            lineno = line.start[0]
            col = line.start[1]
            self[lineno] = list(disable)
            if line.type == _tokenize.COMMENT:
                if line.string[1:].strip().startswith(f"{__package__}:"):
                    string = line.string.split(":")[1].strip()

                    # module level comments
                    if col == 0:
                        if string == "disable":
                            module_is_disabled = True
                        elif string == "enable":
                            module_is_disabled = False

                    # otherwise, inline comments
                    elif string == "disable":
                        self[lineno].extend(_ERRORS)

            # keep appending disabled lines as long as this is true
            if module_is_disabled:
                self[lineno].extend(_ERRORS)

    def __setitem__(self, key: int, value: list[str]) -> None:
        if key not in self:
            super().__setitem__(key, value)
