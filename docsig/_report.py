"""
docsig._report
==============
"""

from __future__ import annotations as _

import sys as _sys
import typing as _t

import click as _click

from ._module import Function as _Function
from ._stub import UNNAMED as _UNNAMED
from ._stub import VALID_DESCRIPTION as _VALID_DESCRIPTION
from ._stub import Param as _Param
from ._stub import RetType as _RetType
from ._utils import almost_equal as _almost_equal
from ._utils import has_bad_return as _has_bad_return
from .messages import TEMPLATE as _TEMPLATE
from .messages import E as _E
from .messages import Message as _Message
from .messages import Messages as _Messages

_MIN_MATCH = 0.8
_MAX_MATCH = 1.0


class Failure(_t.List[str]):
    """Compile and produce report.

    :param func: Function object.
    :param target: List of errors to target.
    :param check_property_returns: Run return checks on properties.
    :param ignore_typechecker: Ignore checking return values.
    """

    def __init__(
        self,
        func: _Function,
        target: _Messages,
        check_property_returns: bool,
        ignore_typechecker: bool,
    ) -> None:
        super().__init__()
        self._func = func
        if target:
            self._func.messages.extend(i for i in _E.all if i not in target)

        self._func = func
        self._check_property_returns = check_property_returns
        self._sig0xx_config()
        if self._func.docstring.string is None:
            self._sig1xx_missing()
        else:
            self._sig2xx_signature()
            for index in range(len(self._func)):
                doc = self._func.docstring.args.get(index)
                self._sig3xx_description(doc)
                sig = self._func.signature.args.get(index)
                self._sig4xx_parameters(doc, sig)
            if not ignore_typechecker:
                self._sig5xx_returns()

        self.sort()

    def _add(self, value: _Message, hint: bool = False, **kwargs) -> None:
        message = value.fstring(_TEMPLATE)
        if kwargs:
            message = message.format(**kwargs)

        if hint:
            message += f"\n    hint: {value.hint}"

        if value not in self._func.messages and message not in self:
            super().append(message)

    def _sig0xx_config(self) -> None:
        for comment in self._func.comments:
            if not comment.isvalid:
                if comment.ismodule:
                    # unknown-module-directive
                    self._add(_E[201], directive=comment.kind)
                else:
                    # unknown-inline-directive
                    self._add(_E[202], directive=comment.kind)
            else:
                for rule in comment:
                    if not rule.isknown:
                        if comment.ismodule:
                            # unknown-module-directive-option
                            self._add(
                                _E[203],
                                directive=comment.kind,
                                option=rule.description,
                            )
                        else:
                            # unknown-inline-directive-option
                            self._add(
                                _E[204],
                                directive=comment.kind,
                                option=rule.description,
                            )

    def _sig1xx_missing(self) -> None:
        if not self._func.isinit:
            # function-doc-missing
            self._add(_E[113])
        else:
            # class-doc-missing
            self._add(_E[114])

    def _sig2xx_signature(self) -> None:
        if self._func.docstring.args.duplicated:
            # pop the duplicates so that they are considered a single
            # parameter, that way there are no assumptions that the
            # parameters must be out of order
            for count, arg in enumerate(self._func.docstring.args):
                if arg in self._func.docstring.args.duplicates:
                    self._func.docstring.args.pop(count)

            # duplicate-params-found
            self._add(_E[106])
        # there are non-existing params in the docstring
        elif len(self._func.docstring.args) > len(self._func.signature.args):
            # pop the parameters that do not exist so that they are
            # excluded from further analysis, that way there are no
            # additional, and redundant, errors
            # this will ensure that both signature and docstring are
            # equal in length, with all parameters that do not exist
            # accounted for
            for count, __ in enumerate(self._func.docstring.args, 1):
                if count > len(self._func.signature.args):
                    self._func.docstring.args.pop(count - 1)
            # params-do-not-exist
            self._add(_E[102])
        # there are more args in sig than doc, so doc params missing
        elif len(self._func.signature.args) > len(self._func.docstring.args):
            # append the parameters that are missing so that they are
            # included in further analysis, that way there are no
            # additional, and redundant, errors
            # this will ensure that both signature and docstring are
            # equal in length, with all parameters that are not
            # documented accounted for
            for count, arg in enumerate(self._func.signature.args, 1):
                if count > len(self._func.docstring.args):
                    self._func.docstring.args.append(
                        _Param(arg.kind, arg.name, _VALID_DESCRIPTION, 0)
                    )
            # params-missing
            self._add(_E[103])

    def _sig3xx_description(self, doc: _Param) -> None:
        if doc.description is None:
            self._add(_E[117])
        elif doc.description is not None and not doc.description.startswith(
            " "
        ):
            # syntax-error-in-description
            self._add(_E[115])
        # if the parameter does not have a name, but exists, then it
        # must be incorrectly documented
        elif doc.name == _UNNAMED:
            # param-incorrectly-documented
            self._add(_E[107])

    def _sig4xx_parameters(self, doc: _Param, sig: _Param) -> None:
        if doc.indent > 0:
            # incorrect-indent
            self._add(_E[116])
        elif doc != sig:
            if (
                sig.name in self._func.docstring.args.names
                or doc.name in self.func.signature.args.names
            ):
                # params-out-of-order
                self._add(_E[101])
            elif (
                doc.name != _UNNAMED
                and sig.name is not None
                and doc.name is not None
            ):
                if _almost_equal(sig.name, doc.name, _MIN_MATCH, _MAX_MATCH):
                    # spelling-error
                    self._add(_E[112])
                else:
                    # param-not-equal-to-arg
                    self._add(_E[110])

    def _sig5xx_returns(self) -> None:
        if not self._func.isinit and not (
            self._func.isproperty and not self._check_property_returns
        ):
            # no types, cannot know either way
            if self._func.signature.rettype == _RetType.UNTYPED:
                # confirm-return-needed
                self._add(_E[109], hint=True)
            # return type is none, so no return should be documented
            elif self._func.docstring.returns:
                if self._func.signature.rettype == _RetType.NONE:
                    # return-documented-for-none
                    self._add(_E[104])
            # return type is some, so return should be documented
            elif self._func.signature.returns:
                # return-missing
                self._add(
                    _E[105],
                    hint=_has_bad_return(str(self._func.docstring.string)),
                )
        elif self._func.docstring.returns:
            # method is init, so no return should be documented
            if self._func.isinit:
                # class-return-documented
                self._add(_E[111], hint=True)
            # method is property and not set to document property
            elif self._func.isproperty and not self._check_property_returns:
                # return-documented-for-property
                self._add(_E[108], hint=True)

    @property
    def func(self) -> _Function:
        """Function this failure belongs to."""
        return self._func


class Failures(_t.List[Failure]):
    """Sequence of failed functions."""


class Report(_t.Dict[str, _t.List[Failures]]):
    """Collect and display report."""

    def __getitem__(self, key: str) -> list[Failures]:
        if key not in super().__iter__():
            super().__setitem__(key, [])

        return super().__getitem__(key)

    def print(self, no_ansi: bool) -> None:
        """Display report summary if any checks have failed.

        :param no_ansi: Disable ANSI output.
        """
        for key, value in self.items():
            for failures in value:
                for failure in failures:
                    header = f"{key}{failure.func.lineno}"
                    function = failure.func.name
                    if failure.func.parent.name:
                        function = f"{failure.func.parent.name}.{function}"

                    header += f" in {function}"
                    _click.echo(
                        "{}\n    {}".format(
                            _click.style(header, fg="magenta"),
                            "\n    ".join(failure),
                        ),
                        color=not no_ansi and _sys.stdout.isatty(),
                    )
