"""
docsig._report
==============
"""
from __future__ import annotations

from collections import Counter as _Counter

from . import messages as _messages
from ._function import Function as _Function
from ._objects import MutableSequence as _MutableSequence


class Report(_MutableSequence):
    """Compile and produce report.

    :param func: Function object.
    """

    def __init__(self, func: _Function) -> None:
        super().__init__()
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
            self.append(_messages.E101)

    def exists(self) -> None:
        """Test that non-existing parameter is not documented."""
        if len(self._func.docstring.args) > len(self._func.signature.args):
            self.append(_messages.E102)

    def missing(self) -> None:
        """Test that parameter is not missing from documentation."""
        if len(self._func.signature.args) > len(self._func.docstring.args):
            message = _messages.E103
            docstring = self._func.docstring.docstring
            if not self._func.docstring.is_doc:
                message += f"\n{_messages.H104}"

            elif docstring is not None and all(
                f"param {i}" in docstring for i in self._func.signature.args
            ):
                message += f"\n{_messages.H101}"

            self.append(message)

    def duplicates(self) -> None:
        """Test that there are no duplicate parameters in docstring."""
        if any(
            k for k, v in _Counter(self._func.docstring.args).items() if v > 1
        ):
            self.append(_messages.E106)

    def extra_return(self) -> None:
        """Check that return is not documented when there is none."""
        if (
            self._func.docstring.returns
            and self._func.signature.return_value == "None"
            and not self._func.isproperty
        ):
            self.append(_messages.E104)

    def property_return(self) -> None:
        """Check that return is not documented for property."""
        if self._func.docstring.returns and self._func.isproperty:
            self.append(f"{_messages.E108}\n{_messages.H102}")

    def return_not_typed(self) -> None:
        """Check that return is not documented when no type provided."""
        if (
            self._func.signature.return_value is None
            and not self._func.isproperty
        ):
            self.append(_messages.E109)

    def missing_return(self) -> None:
        """Check that return is documented when func returns value."""
        if self._func.signature.returns and not self._func.docstring.returns:
            message = _messages.E105
            docstring = self._func.docstring.docstring
            if not self._func.docstring.is_doc:
                message += f"\n{_messages.H104}"

            elif docstring is not None and "return" in docstring:
                message += f"\n{_messages.H103}"

            self.append(message)

    def incorrect(self, arg: str | None, doc: str | None) -> None:
        """Test that proper syntax is used when documenting parameters.

        :param arg: Signature argument.
        :param doc: Docstring argument.
        """
        if arg is None and doc is None:
            self.append(_messages.E107)

    def get_report(self) -> str:
        """Get report compiled as a string.

        :return: Current report.
        """
        return "\n".join(self) + "\n"
