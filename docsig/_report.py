"""
docsig._report
==============
"""
from __future__ import annotations

import typing as _t
from collections import Counter as _Counter

from . import messages as _messages
from ._function import Function as _Function
from ._objects import MutableSequence as _MutableSequence
from ._utils import almost_equal as _almost_equal

_MIN_MATCH = 0.8
_MAX_MATCH = 1.0


class _MessageSequence(_MutableSequence[str]):
    def __init__(
        self,
        targets: _t.List[str] | None = None,
        disable: _t.List[str] | None = None,
    ) -> None:
        super().__init__()
        self._disable = disable or []
        self._disabled = False
        self._resolve_targeted(targets or [])
        self._errors: _t.List[str] = []

    def _resolve_targeted(self, targets: _t.List[str]) -> None:
        errors = [
            i
            for i in dir(_messages)
            if not i.startswith("__") and i.startswith("E")
        ]
        if targets:
            for target in targets:
                errors.remove(target)

            self._disable.extend(errors)

    def _lock(self, value: str) -> None:
        # if the last code to be disabled was an error then all
        # following hints are disabled until a new error is evaluated
        if value.startswith("E"):
            self._disabled = False

        if value in self._disable:
            self._disabled = True

    def insert(self, index: int, value: str) -> None:
        self._lock(value)
        if value.startswith("E"):
            self._errors.append(value)

        message = getattr(_messages, value)
        if not self._disabled and not (
            value.startswith("E") and message in self
        ):
            super().insert(index, message)


class Report(_MessageSequence):
    """Compile and produce report.

    :param func: Function object.
    :param targets: List of errors to target.
    :param disable: List of errors to disable.
    """

    def __init__(
        self,
        func: _Function,
        targets: _t.List[str] | None = None,
        disable: _t.List[str] | None = None,
    ) -> None:
        super().__init__(targets, disable)
        self._func = func

    def order(self, arg: str | None, doc: str | None) -> None:
        """Test for documented parameters and their order.

        :param arg: Signature argument.
        :param doc: Docstring argument.
        """
        if (
            arg in self._func.docstring.args
            or doc in self._func.signature.args
        ):
            self.append("E101")

    def exists(self) -> None:
        """Test that non-existing parameter is not documented."""
        if len(self._func.docstring.args) > len(self._func.signature.args):
            self.append("E102")

    def missing(self) -> None:
        """Test that parameter is not missing from documentation."""
        if len(self._func.signature.args) > len(self._func.docstring.args):
            self.append("E103")
            docstring = self._func.docstring.docstring
            if docstring is None:
                self.append("H104")

            elif docstring is not None and all(
                f"param {i}" in docstring for i in self._func.signature.args
            ):
                self.append("H101")

    def duplicates(self) -> None:
        """Test that there are no duplicate parameters in docstring."""
        if any(
            k for k, v in _Counter(self._func.docstring.args).items() if v > 1
        ):
            self.append("E106")

    def extra_return(self) -> None:
        """Check that return is not documented when there is none."""
        if (
            self._func.docstring.returns
            and self._func.signature.return_value == "None"
            and not self._func.kind.isproperty
            and not self._func.kind.isinit
        ):
            self.append("E104")

    def property_return(self) -> None:
        """Check that return is not documented for property."""
        if self._func.docstring.returns and self._func.kind.isproperty:
            self.append("E108")
            self.append("H102")

    def return_not_typed(self) -> None:
        """Check that return is not documented when no type provided."""
        if (
            self._func.signature.return_value is None
            and not self._func.kind.isproperty
            and not self._func.kind.isinit
        ):
            self.append("E109")

    def missing_return(self) -> None:
        """Check that return is documented when func returns value."""
        if (
            self._func.signature.returns
            and not self._func.docstring.returns
            and not self._func.kind.isproperty
            and not self._func.kind.isinit
        ):
            self.append("E105")
            docstring = self._func.docstring.docstring
            if docstring is None:
                self.append("H104")

            elif docstring is not None and "return" in docstring:
                self.append("H103")

    def incorrect(self, arg: str | None, doc: str | None) -> None:
        """Test that proper syntax is used when documenting parameters.

        :param arg: Signature argument.
        :param doc: Docstring argument.
        """
        if arg is None and doc is None:
            self.append("E107")

    def not_equal(self, arg: str | None, doc: str | None) -> None:
        """Final catch-all.

        Only applies if no other errors, including disabled, have been
        triggered

        :param arg: Signature argument.
        :param doc: Docstring argument.
        """
        if arg is not None and doc is not None and not self._errors:
            self.append("E110")

    def class_return(self) -> None:
        """Check that return is not documented for __init__."""
        if self._func.docstring.returns and self._func.kind.isinit:
            self.append("E111")
            self.append("H105")

    def misspelled(self, arg: str | None, doc: str | None) -> None:
        """Test whether there is a spelling error in documentation.

        To avoid false positives also check whether doc param is almost
        equal amongst its sibling params. If params are too similarly
        named then this error won't be raised.

        :param arg: Signature argument.
        :param doc: Docstring argument.
        """
        if (
            arg is not None
            and doc is not None
            and not self._errors
            and _almost_equal(arg, doc, _MIN_MATCH, _MAX_MATCH)
        ):
            self.append("E112")

    def get_report(self, prefix: str = "") -> str:
        """Get report compiled as a string.

        :param prefix: Prefix report.
        :return: Current report.
        """
        return f"\n{prefix}".join(self) + "\n"
