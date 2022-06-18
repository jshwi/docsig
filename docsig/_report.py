"""
docsig._report
==============
"""
import typing as _t
from collections import Counter as _Counter

from ._objects import MutableSet as _MutableSet
from .messages import E101, E102, E103, E104, E105, E106, E107


class Report(_MutableSet):
    """Compile and produce report."""

    def order(
        self,
        arg: _t.Optional[str],
        doc: _t.Optional[str],
        params: _t.Tuple[str, ...],
        docstring: _t.Tuple[_t.Optional[str], ...],
    ) -> None:
        """Test for documented parameters and their order.

        :param arg: Signature argument.
        :param doc: Docstring argument.
        :param params: All Signature arguments.
        :param docstring: All docstring arguments.
        """
        if arg in docstring or doc in params:
            self.add(E101)

    def exists(
        self,
        params: _t.Tuple[str, ...],
        docstring: _t.Tuple[_t.Optional[str], ...],
    ) -> None:
        """Test that non-existing parameter is not documented.

        :param params: All Signature arguments.
        :param docstring: All docstring arguments.
        """
        if len(docstring) > len(params):
            self.add(E102)

    def missing(
        self,
        params: _t.Tuple[str, ...],
        docstring: _t.Tuple[_t.Optional[str], ...],
    ) -> None:
        """Test that parameter is not missing from documentation.

        :param params: All Signature arguments.
        :param docstring: All docstring arguments.
        """
        if len(params) > len(docstring):
            self.add(E103)

    def duplicates(self, docstring: _t.Tuple[_t.Optional[str], ...]) -> None:
        """Test that there are no duplicate parameters in docstring.

        :param docstring: All docstring arguments.
        """
        if any(k for k, v in _Counter(docstring).items() if v > 1):
            self.add(E106)

    def extra_return(
        self, returns: bool, arg_returns: _t.Optional[str]
    ) -> None:
        """Check that return is not documented when there is none.

        :param returns: Boolean check that function return is not None.
        :param arg_returns: Value of documented return.
        """
        if returns and not arg_returns:
            self.add(E104)

    def missing_return(
        self, returns: bool, arg_returns: _t.Optional[str]
    ) -> None:
        """Check that return is documented when function returns value.

        :param returns: Boolean check that function return is not None.
        :param arg_returns: Value of documented return.
        """
        if arg_returns and not returns:
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
