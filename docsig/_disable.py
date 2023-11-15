"""
docsig._disable
===============
"""
from __future__ import annotations as _

import re as _re
import tokenize as _tokenize
import typing as _t
from io import StringIO as _StringIO

from typing_extensions import Self as _Self

from ._report import ERRORS as _ERRORS


class _Directive:
    _valid_kinds = "enable", "disable"

    def __init__(self, kind: str, col: int) -> None:
        self._ismodule = col == 0
        self._rules = []
        self._kind = kind
        delimiter = _re.search(r"\W+", kind)
        if delimiter and delimiter[0] == "=":
            self._kind, value = kind.split("=")
            self._rules.extend(
                [value] if "," not in value else value.split(",")
            )
        else:
            self._rules.extend(_ERRORS)

    @property
    def rules(self) -> list[str]:
        """The rules, if any, associated with this directive."""
        return self._rules

    @property
    def ismodule(self) -> bool:
        """Whether this is a module level directive or not."""
        return self._ismodule

    @property
    def disable(self) -> bool:
        """Whether this is a disable directive or not."""
        return self._kind == self._valid_kinds[1]

    @classmethod
    def parse(cls, comment: str, col: int) -> _Self | None:
        """Parse string into directive object if possible.

        :param comment: Comment to parse.
        :param col: Column of comment to instantiate directive.
        :return: Instantiated directive object if valid directive or
            None if not a valid directive.
        """
        if comment[1:].strip().startswith(f"{__package__}:"):
            return cls(comment.split(":")[1].strip(), col)

        return None


class Disabled(_t.Dict[int, _t.List[str]]):
    """Data for lines which are excluded from checks.

    :param text: Python code.
    :param disable: List of checks to disable.
    """

    def __init__(self, text: str, disable: list[str]) -> None:
        super().__init__()
        fin = _StringIO(text)
        module_disables = list(disable)
        for line in _tokenize.generate_tokens(fin.readline):
            if line.type in (_tokenize.NAME, _tokenize.OP, _tokenize.DEDENT):
                continue

            lineno, col = line.start
            if line.type == _tokenize.COMMENT:
                directive = _Directive.parse(line.string, col)
                if directive is not None:
                    if directive.ismodule:
                        if directive.disable:
                            module_disables.extend(directive.rules)
                        else:
                            module_disables = [
                                i
                                for i in module_disables
                                if i not in directive.rules
                            ]
                    else:
                        if directive.disable:
                            self[lineno] = [*directive.rules, *module_disables]

            self[lineno] = list(module_disables)

    def __setitem__(self, key, value) -> None:
        if key not in self:
            super().__setitem__(key, value)
