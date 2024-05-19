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
from .messages import TEMPLATE as _TEMPLATE
from .messages import E as _E
from .messages import Message as _Message
from .messages import Messages as _Messages

_MIN_MATCH = 0.8
_MAX_MATCH = 1.0


class Failure(_t.List[str]):
    """Compile and produce report.

    :param func: Function object.
    :param targets: List of errors to target.
    :param disable: List of errors to disable.
    :param check_property_returns: Run return checks on properties.
    :param ignore_typechecker: Ignore checking return values.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        func: _Function,
        targets: _Messages,
        disable: _Messages,
        check_property_returns: bool,
        ignore_typechecker: bool,
    ) -> None:
        super().__init__()
        self._disable = list(disable)
        if targets:
            errors = list(_E.all(1))
            for target in targets:
                errors.remove(target)

            self._disable.extend(errors)

        self._errors = _Messages()
        self._func = func
        self._no_prop_return = (
            func.isproperty
            and not check_property_returns
            and not ignore_typechecker
        )
        self._no_returns = (
            func.isinit or self._no_prop_return or ignore_typechecker
        )
        self._invalid_directive()
        self._invalid_directive_options()
        self._missing_class_docstring()
        self._missing_func_docstring()
        if func.docstring.string is not None:
            # make sure these come first as they alter the function
            # docstring object before it is analysed further
            self._duplicates()
            self._exists()

            # all further analysis below
            self._return_not_typed()
            self._missing()
            self._extra_return()
            self._missing_return()
            self._property_return()
            self._class_return()
            for index in range(len(func)):
                arg = func.signature.args.get(index)
                doc = func.docstring.args.get(index)
                self._no_description(doc)
                self._description_syntax(doc)
                self._indent_syntax(doc)

                if doc.name == _UNNAMED:
                    # if the parameter does not have a name, but exists,
                    # then it must be incorrectly documented
                    # prior implementation relied on the docstring
                    # parameter equalling the signature parameter
                    self._add(_E[107])

                elif arg != doc:
                    if any(
                        arg.name == i.name for i in self._func.docstring.args
                    ) or any(
                        doc.name == i.name for i in self._func.signature.args
                    ):
                        # parameters out of order
                        self._add(_E[101])

                    elif (
                        arg.name is not None
                        and doc.name is not None
                        and not self._errors
                        and _almost_equal(
                            arg.name, doc.name, _MIN_MATCH, _MAX_MATCH
                        )
                    ):
                        # spelling error found in documented parameter
                        self._add(_E[112])

                    elif arg.name is not None and doc.name is not None:
                        # documented parameter not equal to its
                        # respective argument
                        self._add(_E[110])

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

    def _exists(self) -> None:
        # pop the parameters that do not exist so that they are excluded
        # from further analysis, that way there are no additional, and
        # redundant, errors
        # this will ensure that both signature and docstring are equal
        # in length, with all parameters that do not exist accounted for
        if len(self._func.docstring.args) > len(self._func.signature.args):
            for count, __ in enumerate(self._func.docstring.args, 1):
                if count > len(self._func.signature.args):
                    self._func.docstring.args.pop(count - 1)

            self._add(_E[102])

    def _missing_func_docstring(self) -> None:
        if not self._func.isinit and self._func.docstring.string is None:
            self._add(_E[113])

    def _missing_class_docstring(self) -> None:
        if self._func.isinit and self._func.docstring.string is None:
            self._add(_E[114])

    def _missing(self) -> None:
        if len(self._func.signature.args) > len(self._func.docstring.args):
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

    def _duplicates(self) -> None:
        # pop the duplicates so that they are considered a single
        # parameter, that way there are no assumptions that the
        # parameters must be out of order
        if self._func.docstring.args.duplicated:
            for count, arg in enumerate(self._func.docstring.args):
                if arg in self._func.docstring.args.duplicates:
                    self._func.docstring.args.pop(count)

            self._add(_E[106])

    def _extra_return(self) -> None:
        if (
            self._func.docstring.returns
            and self._func.signature.rettype == _RetType.NONE
            and not self._no_returns
        ):
            self._add(_E[104])

    def _property_return(self) -> None:
        if self._func.docstring.returns and self._no_prop_return:
            self._add(_E[108], hint=True)

    def _return_not_typed(self) -> None:
        if (
            self._func.signature.rettype == _RetType.UNTYPED
            and not self._no_returns
        ):
            self._add(_E[109], hint=True)

    def _missing_return(self) -> None:
        hint = False
        if (
            self._func.signature.returns
            and not self._func.docstring.returns
            and not self._no_returns
        ):
            docstring = self._func.docstring.string
            # do more than just search the docstring for the word return
            # as return statements come last, so only search the last
            # line
            # params can also come last, so make sure it is not a param
            # declaration
            if docstring is not None:
                lines = docstring.splitlines()
                if len(lines) > 1:
                    if "return" in lines[-1] and ":param" not in lines[-1]:
                        hint = True

            self._add(_E[105], hint=hint)

    def _class_return(self) -> None:
        if self._func.docstring.returns and self._func.isinit:
            self._add(_E[111], hint=True)

    def _description_syntax(self, doc: _Param) -> None:
        if doc.description is not None and not doc.description.startswith(" "):
            self._add(_E[115])

    def _indent_syntax(self, doc: _Param) -> None:
        if doc.indent > 0:
            self._add(_E[116])

    def _no_description(self, doc: _Param) -> None:
        if doc.description is None:
            self._add(_E[117])

    def _invalid_directive(self) -> None:
        for comment in self._func.comments:
            if not comment.isvalid:
                err = _E[int(f"20{1 if comment.ismodule else 2}")]
                self._add(err, directive=comment.kind)

    def _invalid_directive_options(self) -> None:
        for comment in self._func.comments:
            for rule in comment:
                if not rule.isknown:
                    self._add(
                        _E[int(f"20{3 if comment.ismodule else 4}")],
                        directive=comment.kind,
                        option=rule.description,
                    )

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
