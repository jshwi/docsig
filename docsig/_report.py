"""
docsig._report
==============
"""

from __future__ import annotations as _

import typing as _t

from ._message import Message as _Message
from ._module import Function as _Function
from ._stub import RETURN as _RETURN
from ._stub import Param as _Param
from ._utils import almost_equal as _almost_equal
from .messages import TEMPLATE as _TEMPLATE
from .messages import E as _E

_MIN_MATCH = 0.8
_MAX_MATCH = 1.0


class Report(_t.List[str]):
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
        super().__init__()
        self._disable = list(disable)
        if targets:
            errors = list(_E.all(1))
            for target in targets:
                errors.remove(target)

            self._disable.extend(errors)

        self._errors: list[_Message] = []
        self._func = func
        self._no_prop_return = func.isproperty and not check_property_returns
        self._no_returns = func.isinit or self._no_prop_return
        self._invalid_directive()
        self._invalid_directive_options()
        self._missing_class_docstring()
        self._missing_func_docstring()
        if func.docstring.string is not None:
            self._return_not_typed()
            self._exists()
            self._missing()
            self._duplicates()
            self._extra_return()
            self._missing_return()
            self._property_return()
            self._class_return()
            for index in range(len(func)):
                arg = func.signature.args.get(index)
                doc = func.docstring.args.get(index)
                self._description_syntax(doc)
                self._indent_syntax(doc)
                if arg != doc:
                    self._order(arg, doc)
                    self._incorrect(arg, doc)
                    self._misspelled(arg, doc)
                    self._not_equal(arg, doc)

        self.sort()

    def _add(self, value: _Message, hint: bool = False, **kwargs) -> None:
        self._errors.append(value)
        message = value.fstring(_TEMPLATE)
        if kwargs:
            message = message.format(**kwargs)

        if hint:
            message += f"\n    hint: {value.hint}"

        if value not in self._disable and message not in self:
            super().append(message)

    def _order(self, sig: _Param, doc: _Param) -> None:
        if any(sig.name == i.name for i in self._func.docstring.args) or any(
            doc.name == i.name for i in self._func.signature.args
        ):
            self._add(_E[101])

    def _exists(self) -> None:
        if len(self._func.docstring.args) > len(self._func.signature.args):
            self._add(_E[102])

    def _missing_func_docstring(self) -> None:
        if not self._func.isinit and self._func.docstring.string is None:
            self._add(_E[113])

    def _missing_class_docstring(self) -> None:
        if self._func.isinit and self._func.docstring.string is None:
            self._add(_E[114])

    def _missing(self) -> None:
        if len(self._func.signature.args) > len(self._func.docstring.args):
            self._add(_E[103])

    def _duplicates(self) -> None:
        if self._func.docstring.args.duplicated:
            self._add(_E[106])

    def _extra_return(self) -> None:
        if (
            self._func.docstring.returns
            and self._func.signature.rettype == "None"
            and not self._no_returns
        ):
            self._add(_E[104])

    def _property_return(self) -> None:
        if self._func.docstring.returns and self._no_prop_return:
            self._add(_E[108], hint=True)

    def _return_not_typed(self) -> None:
        if self._func.signature.rettype is None and not self._no_returns:
            self._add(_E[109])

    def _missing_return(self) -> None:
        hint = False
        if (
            self._func.signature.returns
            and not self._func.docstring.returns
            and not self._no_returns
        ):
            docstring = self._func.docstring.string
            if docstring is not None and _RETURN in docstring:
                hint = True

            self._add(_E[105], hint=hint)

    def _incorrect(self, sig: _Param, doc: _Param) -> None:
        if sig.name is None and doc.name is None:
            self._add(_E[107])

    # final catch-all
    def _not_equal(self, sig: _Param, doc: _Param) -> None:
        if sig.name is not None and doc.name is not None and not self._errors:
            self._add(_E[110])

    def _class_return(self) -> None:
        if self._func.docstring.returns and self._func.isinit:
            self._add(_E[111], hint=True)

    def _misspelled(self, sig: _Param, doc: _Param) -> None:
        if (
            sig.name is not None
            and doc.name is not None
            and not self._errors
            and _almost_equal(sig.name, doc.name, _MIN_MATCH, _MAX_MATCH)
        ):
            self._add(_E[112])

    def _description_syntax(self, doc: _Param) -> None:
        if doc.description is not None and not doc.description.startswith(" "):
            self._add(_E[115])

    def _indent_syntax(self, doc: _Param) -> None:
        if doc.indent > 0:
            self._add(_E[116])

    def _invalid_directive(self) -> None:
        for comment in self._func.comments:
            if not comment.isvalid:
                err = _E[int(f"20{1 if comment.ismodule else 2}")]
                self._add(err, directive=comment.kind)

    def _invalid_directive_options(self) -> None:
        for comment in self._func.comments:
            if comment.rules.unknown:
                err = _E[int(f"20{3 if comment.ismodule else 4}")]
                for rule in comment.rules.unknown:
                    self._add(
                        err, directive=comment.kind, option=rule.description
                    )

    def get_report(self, prefix: str = "") -> str:
        """Get report compiled as a string.

        :param prefix: Prefix report.
        :return: Current report.
        """
        report = f"\n{prefix}".join(self)
        return f"{report}\n"
