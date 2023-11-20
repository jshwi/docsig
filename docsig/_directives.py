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

from . import messages as _messages

ERRORS = tuple(
    i for i in dir(_messages) if not i.startswith("__") and i.startswith("E1")
)


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
            self._rules.extend(ERRORS)

    @property
    def isvalid(self) -> bool:
        """Whether this directive is valid or not."""
        return self._kind in self._valid_kinds

    @property
    def rules(self) -> list[str]:
        """The rules, if any, associated with this directive."""
        return self._rules

    @property
    def ismodule(self) -> bool:
        """Whether this is a module level directive or not."""
        return self._ismodule

    @property
    def enable(self) -> bool:
        """Whether this is a enable directive or not."""
        return self._kind == self._valid_kinds[0]

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


class Directives(_t.Dict[int, _t.List[str]]):
    """Data for directives:

    Dict like object with the line number of directive as the key and
    total errors which are excluded from function checks.

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
                if directive is not None and directive.isvalid:
                    update = module_disables
                    if directive.disable:
                        update = directive.rules + module_disables
                    elif directive.enable:
                        update = [
                            i
                            for i in module_disables
                            if i not in directive.rules
                        ]

                    if directive.ismodule:
                        module_disables = update
                    else:
                        self[lineno] = update

            if lineno not in self:
                self[lineno] = list(module_disables)
