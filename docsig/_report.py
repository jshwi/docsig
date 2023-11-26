"""
docsig._report
==============
"""
from __future__ import annotations as _

import typing as _t

from ._function import RETURN as _RETURN
from ._function import Function as _Function
from ._function import Param as _Param
from ._message import Message as _Message
from ._utils import almost_equal as _almost_equal
from .messages import TEMPLATE as _TEMPLATE
from .messages import E as _E

_MIN_MATCH = 0.8
_MAX_MATCH = 1.0


class _MessageSequence(_t.List[str]):
    def __init__(
        self,
        targets: list[_Message],
        disable: list[_Message],
    ) -> None:
        super().__init__()
        self._disable = list(disable)
        if targets:
            errors = list(_E.all(1))
            for target in targets:
                errors.remove(target)

            self._disable.extend(errors)

        self._errors: list[_Message] = []

    def add(self, value: _Message, hint: bool = False, **kwargs) -> None:
        """Add an error to the container.

        :param value: Value to add.
        :param hint: Whether to print a hint or not.
        :param kwargs: Variable(s) if format string.
        """
        self._errors.append(value)
        message = value.fstring(_TEMPLATE)
        if kwargs:
            message = message.format(**kwargs)

        if hint:
            message += f"\nhint: {value.hint}"

        if value not in self._disable and message not in self:
            super().append(message)


class Report(_MessageSequence):
    """Compile and produce report.

    :param func: Function object.
    :param targets: List of errors to target.
    :param disable: List of errors to disable.
    :param check_property_returns: Run return checks on properties.
    """

    def __init__(
        self,
        func: _Function,
        targets: list[_Message],
        disable: list[_Message],
        check_property_returns: bool,
    ) -> None:
        super().__init__(targets, disable)
        self._func = func
        self._no_prop_return = func.isproperty and not check_property_returns
        self._no_returns = func.isinit or self._no_prop_return

    def order(self, sig: _Param, doc: _Param) -> None:
        """Test for documented parameters and their order.

        :param sig: Signature argument.
        :param doc: Docstring argument.
        """
        if any(sig.name == i.name for i in self._func.docstring.args) or any(
            doc.name == i.name for i in self._func.signature.args
        ):
            self.add(_E[101])

    def exists(self) -> None:
        """Test that non-existing parameter is not documented."""
        if len(self._func.docstring.args) > len(self._func.signature.args):
            self.add(_E[102])

    def missing_func_docstring(self) -> None:
        """Test that docstring is not missing from func."""
        if not self._func.isinit and self._func.docstring.string is None:
            self.add(_E[113])

    def missing_class_docstring(self) -> None:
        """Test that docstring is not missing from class."""
        if self._func.isinit and self._func.docstring.string is None:
            self.add(_E[114])

    def missing(self) -> None:
        """Test that parameter is not missing from documentation."""
        if len(self._func.signature.args) > len(self._func.docstring.args):
            self.add(_E[103])

    def duplicates(self) -> None:
        """Test that there are no duplicate parameters in docstring."""
        if self._func.docstring.args.duplicated:
            self.add(_E[106])

    def extra_return(self) -> None:
        """Check that return is not documented when there is none."""
        if (
            self._func.docstring.returns
            and self._func.signature.rettype == "None"
            and not self._no_returns
        ):
            self.add(_E[104])

    def property_return(self) -> None:
        """Check that return is not documented for property."""
        if self._func.docstring.returns and self._no_prop_return:
            self.add(_E[108], hint=True)

    def return_not_typed(self) -> None:
        """Check that return is not documented when no type provided."""
        if self._func.signature.rettype is None and not self._no_returns:
            self.add(_E[109])

    def missing_return(self) -> None:
        """Check that return is documented when func returns value."""
        hint = False
        if (
            self._func.signature.returns
            and not self._func.docstring.returns
            and not self._no_returns
        ):
            docstring = self._func.docstring.string
            if docstring is not None and _RETURN in docstring:
                hint = True

            self.add(_E[105], hint=hint)

    def incorrect(self, sig: _Param, doc: _Param) -> None:
        """Test that proper syntax is used when documenting parameters.

        :param sig: Signature argument.
        :param doc: Docstring argument.
        """
        if sig.name is None and doc.name is None:
            self.add(_E[107])

    def not_equal(self, sig: _Param, doc: _Param) -> None:
        """Final catch-all.

        Only applies if no other errors, including disabled, have been
        triggered

        :param sig: Signature argument.
        :param doc: Docstring argument.
        """
        if sig.name is not None and doc.name is not None and not self._errors:
            self.add(_E[110])

    def class_return(self) -> None:
        """Check that return is not documented for __init__."""
        if self._func.docstring.returns and self._func.isinit:
            self.add(_E[111], hint=True)

    def misspelled(self, sig: _Param, doc: _Param) -> None:
        """Test whether there is a spelling error in documentation.

        To avoid false positives also check whether doc param is almost
        equal amongst its sibling params. If params are too similarly
        named then this error won't be raised.

        :param sig: Signature argument.
        :param doc: Docstring argument.
        """
        if (
            sig.name is not None
            and doc.name is not None
            and not self._errors
            and _almost_equal(sig.name, doc.name, _MIN_MATCH, _MAX_MATCH)
        ):
            self.add(_E[112])

    def description_syntax(self, doc: _Param) -> None:
        """Test whether docstring description has correct spacing.

        :param doc: Docstring argument.
        """
        if doc.description is not None and not doc.description.startswith(" "):
            self.add(_E[115])

    def indent_syntax(self, doc: _Param) -> None:
        """Test whether docstring description is indented correctly.

        :param doc: Docstring argument.
        """
        if doc.indent > 0:
            self.add(_E[116])

    def invalid_directive(self) -> None:
        """Report on any invalid directives belonging to this func."""
        for directive in self._func.directives:
            if not directive.isvalid:
                err = _E[int(f"20{1 if directive.ismodule else 2}")]
                self.add(err, directive=directive.kind)

    def invalid_directive_options(self) -> None:
        """Report on any invalid directive options belonging to this."""
        for directive in self._func.directives:
            if directive.rules.unknown:
                err = _E[int(f"20{3 if directive.ismodule else 4}")]
                for rule in directive.rules.unknown:
                    self.add(
                        err, directive=directive.kind, option=rule.description
                    )

    def get_report(self, prefix: str = "") -> str:
        """Get report compiled as a string.

        :param prefix: Prefix report.
        :return: Current report.
        """
        report = f"\n{prefix}".join(self)
        return f"{report}\n"


def generate_report(
    func: _Function,
    targets: list[_Message],
    disable: list[_Message],
    check_property_returns: bool,
) -> Report:
    """Generate report if function or method has failed.

    :param func: Function object.
    :param targets: List of errors to target.
    :param disable: List of errors to disable.
    :param check_property_returns: Run return checks on properties.
    :return: Compiled report.
    """
    report = Report(func, targets, disable, check_property_returns)
    report.invalid_directive()
    report.invalid_directive_options()
    report.missing_class_docstring()
    report.missing_func_docstring()
    if func.docstring.string is not None:
        report.return_not_typed()
        report.exists()
        report.missing()
        report.duplicates()
        report.extra_return()
        report.missing_return()
        report.property_return()
        report.class_return()
        for index in range(len(func)):
            arg = func.signature.args.get(index)
            doc = func.docstring.args.get(index)
            report.description_syntax(doc)
            report.indent_syntax(doc)
            if arg != doc:
                report.order(arg, doc)
                report.incorrect(arg, doc)
                report.misspelled(arg, doc)
                report.not_equal(arg, doc)

    report.sort()
    return report
