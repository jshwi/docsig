"""
docsig._report
==============
"""
import typing as _t
import warnings as _warnings
from collections import Counter as _Counter

from ._function import Function as _Function
from ._objects import MutableSet as _MutableSet
from .messages import E101, E102, E103, E104, E105, E106, E107, W101


class Report(_MutableSet):
    """Compile and produce report.

    :param func: Function object.
    """

    def __init__(self, func: _Function) -> None:
        super().__init__()
        self._func = func

    def order(self, arg: _t.Optional[str], doc: _t.Optional[str]) -> None:
        """Test for documented parameters and their order.

        :param arg: Signature argument.
        :param doc: Docstring argument.
        """
        if (
            arg in self._func.docstring.args
            or doc in self._func.signature.args
        ):
            self.add(E101)

    def exists(self) -> None:
        """Test that non-existing parameter is not documented."""
        if len(self._func.docstring.args) > len(self._func.signature.args):
            self.add(E102)

    def missing(self) -> None:
        """Test that parameter is not missing from documentation."""
        if len(self._func.signature.args) > len(self._func.docstring.args):
            self.add(E103)

    def duplicates(self) -> None:
        """Test that there are no duplicate parameters in docstring."""
        if any(
            k for k, v in _Counter(self._func.docstring.args).items() if v > 1
        ):
            self.add(E106)

    def extra_return(self) -> None:
        """Check that return is not documented when there is none."""
        if self._func.docstring.returns and not self._func.signature.returns:
            self.add(E104)

    def missing_return(self) -> None:
        """Check that return is documented when function returns
        value."""
        if self._func.signature.returns and not self._func.docstring.returns:
            self.add(E105)

    def incorrect(self, arg: _t.Optional[str], doc: _t.Optional[str]) -> None:
        """Test that proper syntax is used when documenting parameters.

        :param arg: Signature argument.
        :param doc: Docstring argument.
        """
        if arg is None and doc is None:
            self.add(E107)

    def get_report(self) -> str:
        """Get report compiled as a string.

        :return: Current report.
        """
        return "\n".join(self) + "\n"


def warn(missing: _t.List[_t.Tuple[str, _Function]]) -> None:
    """Warn if function does not contain a docstring.

    :param missing: Tuple of module names containing a list of function
        to warn for.
    """
    for module, func in missing:
        _warnings.warn(W101.format(module=module, func=func.name))
