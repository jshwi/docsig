"""
docsig._checker
===============

Run docstring and signature checks for a single function.
"""

import contextlib as _contextlib
import typing as _t

import astroid as _ast

from ._config import Config as _Config
from ._diagnostic import Collector as _Collector
from ._diagnostic import Diagnostic as _Diagnostic
from ._diagnostic import FunctionResult as _FunctionResult
from ._module import Function as _Function
from ._stub import UNNAMED as _UNNAMED
from ._stub import VALID_DESCRIPTION as _VALID_DESCRIPTION
from ._stub import Param as _Param
from ._stub import Params as _Params
from ._stub import RetType as _RetType
from ._utils import SENTENCE_ABBREVIATIONS as _SENTENCE_ABBREVIATIONS
from ._utils import almost_equal as _almost_equal
from ._utils import sentence_tokenizer as _sentence_tokenizer
from .messages import E as _E
from .messages import Message as _Message

_MIN_MATCH = 0.8
_MAX_MATCH = 1.0
_VALID_ENDINGS = (
    "`",
    ".",
    "!",
    "?",
)


def _last_prose_char(text: str) -> tuple[str | None, bool]:
    # return the last character of non-code-block prose and whether the
    # text ends inside a code block (a line ending with ::)
    in_block = False
    last_char = None
    for line in text.strip().split("\n"):
        stripped_ln = line.strip()
        if in_block:
            if stripped_ln and line[:1] not in (" ", "\t"):
                in_block = False
            else:
                continue
        if stripped_ln.startswith(".."):
            # a directive or comment, e.g. `.. versionchanged:: 2.0`,
            # is not prose, and its indented content belongs to it
            in_block = True
            continue
        if stripped_ln.endswith("::"):
            in_block = True
        if stripped_ln:
            last_char = stripped_ln[-1]
    return last_char, in_block


class FunctionChecker:  # pylint: disable=too-few-public-methods
    """Collect docstring and signature failures for one function.

    Runs configured checks and appends Failed entries for each
    violation.

    :param func: Function under check.
    :param config: Configuration object.
    """

    def __init__(self, func: _Function, config: _Config) -> None:
        self._func = func
        self._config = config
        self._diagnostics: list[_Diagnostic] = []
        if config.target:
            self._func.messages.extend(
                i for i in _E.all if i not in config.target
            )

        self._name = self._func.name
        if (
            self._func.parent is not None
            and hasattr(self._func.parent, "name")
            and self._func.parent.name
            and not isinstance(self._func.parent, _ast.nodes.Module)
        ):
            self._name = f"{self._func.parent.name}.{self._name}"

        self._collector = _Collector(func, self._name, self._func.lineno)

    def run(self) -> _FunctionResult:
        """Run the function checks and return the result.

        :return: Function result.
        """
        if self._func.error is not None:
            self._collector.retcode.add(2)
            self._sig9xx_error()
        else:
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

                self._sig5xx_returns(self._config.check.property_returns)

        return _FunctionResult(self._name, self._func.lineno, self._collector)

    def _add(
        self,
        value: _Message,
        include_hint: bool = False,
        **kwargs: _t.Any,
    ) -> None:
        self._collector.add(value, include_hint=include_hint, **kwargs)

    @staticmethod
    def _normalize_params(from_: _Params, to: _Params) -> None:
        # inset the parameters that are missing in their corresponding
        # index so that they are included in further analysis, that way
        # there are no additional, and redundant, errors
        # this will ensure that both signature and docstring are equal,
        # with all parameters that are not documented accounted for
        for count, arg in enumerate(from_):
            try:
                is_equal = _almost_equal(
                    str(arg.name),
                    str(to[count].name),
                    _MIN_MATCH,
                    _MAX_MATCH,
                )
            except IndexError:
                is_equal = False

            # need to make one more test to determine if equal in the
            # case of very similar names, such as param1, param2 and
            # param3 for the signature, and param2, param3 for the
            # docstring, if we don't do this test, param1 is almost
            # equal to param2, and so won't be inserted, but if we can
            # determine param2 is already in signature's next index,
            # then we know that they aren't almost equal, param1 is
            # missing and does need to be inserted in the docstring
            if is_equal:
                with _contextlib.suppress(IndexError):
                    is_equal = to[count].name != from_[count + 1].name

            if not is_equal:
                to.insert(
                    count,
                    _Param(arg.kind, arg.name, _VALID_DESCRIPTION),
                )

    def _sig0xx_config(self) -> None:
        for comment in self._func.comments:
            if not comment.isvalid:
                if comment.ismodule:
                    # unknown-module-directive
                    self._add(_E[1], directive=comment.kind)
                else:
                    # unknown-inline-directive
                    self._add(_E[2], directive=comment.kind)
            elif not comment.isvalidflag:
                if comment.ismodule:
                    # unknown-module-directive-flag
                    self._add(_E[6], directive=comment.kind, flag=comment.flag)
                else:
                    # unknown-inline-directive-flag
                    self._add(_E[7], directive=comment.kind, flag=comment.flag)
            else:
                for rule in comment:
                    if not rule.isknown:
                        if comment.ismodule:
                            # unknown-module-directive-option
                            self._add(
                                _E[3],
                                directive=comment.kind,
                                option=rule.description,
                            )
                        else:
                            # unknown-inline-directive-option
                            self._add(
                                _E[4],
                                directive=comment.kind,
                                option=rule.description,
                            )

    def _sig1xx_missing(self) -> None:
        if not self._func.isinit:
            # function-doc-missing
            self._add(_E[101])
        else:
            # class-doc-missing
            self._add(_E[102])

    def _sig2xx_signature(self) -> None:
        if self._func.docstring.args.duplicated:
            # reduce each duplicate group to one representative without
            # mutating the list during iteration (which skips items)
            seen: set[str | None] = set()
            deduped: list[_Param] = []
            for arg in self._func.docstring.args:
                if arg.name not in seen:
                    seen.add(arg.name)
                    deduped.append(arg)

            list.clear(self._func.docstring.args)
            list.extend(self._func.docstring.args, deduped)

            # duplicate-params-found
            self._add(_E[201])
        # there are non-existing params in the docstring
        elif len(self._func.docstring.args) > len(self._func.signature.args):
            self._normalize_params(
                self._func.docstring.args,
                self._func.signature.args,
            )
            # params-do-not-exist
            self._add(_E[202])
        # there are more args in sig than doc, so doc params missing
        elif len(self._func.signature.args) > len(self._func.docstring.args):
            self._normalize_params(
                self._func.signature.args,
                self._func.docstring.args,
            )
            # params-missing
            self._add(_E[203])

    def _sig3xx_description(self, doc: _Param) -> None:
        # freeze result as it is a property and PyCharm complains
        # `Member 'None' of 'str | None' does not have attribute
        # 'startswith'` as property could theoretically have different
        # result from doc.description is None to
        # doc.description.startswith
        doc_description = doc.description
        if doc_description is None and doc.name is not None:
            self._add(_E[301])
        elif doc_description is not None and not doc_description.startswith(
            " ",
        ):
            # syntax-error-in-description
            self._add(_E[302])
        # if the parameter does not have a name but exists, then it must
        # be incorrectly documented
        elif doc.name == _UNNAMED:
            # param-incorrectly-documented
            self._add(_E[303])
        elif doc.closing_token != ":":
            # bad-closing-token
            self._add(_E[304], token=doc.closing_token, include_hint=True)
        if doc_description is not None and not all(
            stripped[0].isupper()
            for i in _sentence_tokenizer(doc_description)
            if (
                i
                and (stripped := i.strip())[0].isalpha()
                and stripped.lower().split()[0].rstrip(",;")
                not in _SENTENCE_ABBREVIATIONS
            )
        ):
            # description is not capitalized
            self._add(_E[305])
        # description-missing-period
        # a description that ends inside an RST code block (introduced
        # by a line ending with ::) does not need a sentence terminator
        if doc_description:
            last_char, in_block = _last_prose_char(doc_description)
            if (
                not in_block
                and last_char is not None
                and last_char not in _VALID_ENDINGS
            ):
                self._add(_E[306])

    def _sig4xx_parameters(self, doc: _Param, sig: _Param) -> None:
        # freeze result as it is a property and PyCharm complains
        # `Expected type 'str', got 'str | None' instead ' in
        # _almost_equal as property could theoretically have different
        # result from sig.name is not None and doc.name is not None
        sig_name = sig.name
        doc_name = doc.name
        if doc.indent > 0:
            # incorrect-indent
            self._add(_E[401])
        elif doc != sig:
            if (
                sig_name in self._func.docstring.args.names
                or doc_name in self._func.signature.args.names
            ) and len(self._func.docstring.args) > 1:
                # params-out-of-order
                self._add(_E[402])
            elif (
                doc_name != _UNNAMED
                and sig_name is not None
                and doc_name is not None
            ):
                if _almost_equal(sig_name, doc_name, _MIN_MATCH, _MAX_MATCH):
                    # spelling-error
                    self._add(_E[403])
                else:
                    # param-not-equal-to-arg
                    self._add(_E[404])

    def _sig5xx_returns(self, check_property_returns: bool) -> None:
        if not self._func.isinit and not (
            self._func.isproperty and not check_property_returns
        ):
            # no types, cannot know either way
            if self._func.signature.returns.type == _RetType.UNTYPED:
                # confirm-return-needed
                self._add(_E[501], include_hint=True)
            # return-type is none, so no return should be documented
            elif self._func.docstring.returns.returns:
                if self._func.signature.returns.type == _RetType.NONE:
                    # return-documented-for-none
                    self._add(_E[502])
                if self._func.docstring.returns.description_missing:
                    self._add(_E[506])
            # return-type is some, so return should be documented
            elif self._func.signature.returns.returns:
                # return-missing
                lines = str(self._func.docstring.string).splitlines()
                self._add(
                    _E[503],
                    include_hint=(
                        len(lines) > 1
                        and "return" in lines[-1]
                        and ":param" not in lines[-1]
                    ),
                )
        elif self._func.docstring.returns.returns:
            # this method is init, so no return should be documented
            if self._func.isinit:
                # class-return-documented
                self._add(_E[504], include_hint=True)
            # method is property and not set to document property
            elif self._func.isproperty and not check_property_returns:
                # return-documented-for-property
                self._add(_E[505], include_hint=True)

    def _sig9xx_error(self) -> None:
        # invalid-syntax
        if self._func.error is _ast.AstroidSyntaxError:
            self._add(_E[901])
            self._collector.retcode.add(123)
        # unicode-decode-error
        if self._func.error is UnicodeDecodeError:
            self._add(_E[902])
        # recursion-error
        if self._func.error is RecursionError:
            self._add(_E[903])
        # duplicates-found-in-mros
        if self._func.error is _ast.DuplicateBasesError:
            self._add(_E[904])
