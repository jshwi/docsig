"""
tests
=====

Test package for ``docsig``.
"""
import typing as t
from pathlib import Path

from templatest import BaseTemplate as _BaseTemplate
from templatest import templates as _templates

from docsig import messages

MockMainType = t.Callable[..., int]
InitFileFixtureType = t.Callable[[str], Path]

CHECK = "\u2713"
CROSS = "\u2716"

MULTI = "multi"


@_templates.register
class _PassParam(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    :param param1: Passes.
    :param param2: Passes.
    :param param3: Passes.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FailParamDocs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2) -> None:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"
"""


@_templates.register
class _FailParamSig(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Not proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _PassNoDocstring(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    pass
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassNoParams(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function() -> None:
    \"\"\"No params.\"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassUnderscoreParam(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, _) -> None:
    \"\"\"Proper docstring.

    :param param1: Passes.
    :param param2: Passes.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FailOutOfOrder(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3):
    \"\"\"Proper docstring.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CROSS}param1, {CROSS}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"...

    :param param2: {CROSS}
    :param param3: {CROSS}
    :param param1: {CROSS}
    \"\"\"
"""


@_templates.register
class _PassRetType(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> int:
    \"\"\"Proper docstring.

    :param param1: Passes.
    :param param2: Passes.
    :param param3: Passes.
    :return: Passes.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FailRetTypeDocs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :return: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CHECK}param3) -> {CROSS}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CHECK}
    :return: {CROSS}
    \"\"\"
"""


@_templates.register
class _FailRetTypeSig(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> int:
    \"\"\"Proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CHECK}param3) -> {CROSS}int:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CHECK}
    :return: {CROSS}
    \"\"\"
"""


@_templates.register
class _PassNoRetNoType(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3):
    \"\"\"Proper docstring.

    :param param1: Passes.
    :param param2: Passes.
    :param param3: Passes.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FailNoRetDocsNoType(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3):
    \"\"\"Proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :return: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CHECK}param3) -> {CROSS}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CHECK}
    :return: {CROSS}
    \"\"\"
"""


@_templates.register
class _FailRetDocsAttrType(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
import typing as t

def function(param1) -> t.Optional[str]:
    \"\"\"Proper docstring.

    :param param1: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1) -> {CROSS}Optional[str]:
    \"\"\"...

    :param param1: {CHECK}
    :return: {CROSS}
    \"\"\"
"""


@_templates.register
class _FailRetDocsNameType(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
from typing import Optional

def function(param1) -> Optional[str]:
    \"\"\"Proper docstring.

    :param param1: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1) -> {CROSS}Optional[str]:
    \"\"\"...

    :param param1: {CHECK}
    :return: {CROSS}
    \"\"\"
"""


@_templates.register
class _FailOutOfOrder1Sum(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3):
    \"\"\"Proper docstring.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return messages.E101


@_templates.register
class _FailIncorrectDoc(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1) -> None:
    \"\"\"Proper docstring.

    :param param1: Fails.
    :param: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CROSS}None) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _FailParamDocs1Sum(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2) -> None:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E102


@_templates.register
class _FailParamSig1Sum(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Not proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E103


@_templates.register
class _FailRetTypeDocs1Sum(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :return: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E104


@_templates.register
class _FailRetTypeSig1Sum(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> int:
    \"\"\"Proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return messages.E105


@_templates.register
class _FailDupesSum(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    :param param1: Fails.
    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E106


@_templates.register
class _FailIncorrectDocSum(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    :param param1: Fails.
    :param param1: Fails.
    :param param2: Fails.
    :param: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E107


@_templates.register
class _PassWithArgs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, *args) -> None:
    \"\"\"Proper docstring.

    :param param1: Pass.
    :param param2: Pass.
    :param args: Pass
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FailWithArgs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, *args) -> None:
    \"\"\"Proper docstring.

    :param param1: Pass.
    :param param2: Pass.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CROSS}*args) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _PassWithKwargs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, **kwargs) -> None:
    \"\"\"Proper docstring.

    :param param1: Pass.
    :param param2: Pass.
    :param kwargs: Pass
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FailWithKwargs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, **kwargs) -> None:
    \"\"\"Proper docstring.

    :param param1: Pass.
    :param param2: Pass.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CROSS}**kwargs) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _MultiFail(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function_1(param1, param2, param3):
    \"\"\"Proper docstring.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    \"\"\"
    return 0
    
def function_2(param1, param2) -> None:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
    
def function_3(param1, param2, param3) -> None:
    \"\"\"Not proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function_1({CROSS}param1, {CROSS}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"...

    :param param2: {CROSS}
    :param param3: {CROSS}
    :param param1: {CROSS}
    \"\"\"

{messages.E101}


def function_2({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"

{messages.E102}


def function_3({CHECK}param1, {CHECK}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"

{messages.E103}
"""


@_templates.register
class _FailClass(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class Klass:
    def method(param1, param2, **kwargs) -> None:
        \"\"\"Proper docstring.

        :param param1: Pass.
        :param param2: Pass.
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def method({CHECK}param1, {CHECK}param2, {CROSS}**kwargs) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _PassClassSelf(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class Klass:
    def method(self, param1) -> None:
        \"\"\"Proper docstring.

        :param param1: Pass.
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassClassProperty(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class Klass:
    @property
    def method(self) -> int:
        \"\"\"Proper docstring.\"\"\"
        return self._method
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassWithKwargsKey(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, **kwargs) -> None:
    \"\"\"Proper docstring.

    :param param1: Passes
    :key kwarg1: Pass
    :keyword kwarg2: Pass
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FailWithKwargsOutOfOrder(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, **kwargs) -> None:
    \"\"\"Proper docstring.

    :keyword kwarg1: Fail
    :keyword kwarg3: Fail
    :param param1: Fail
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassDualColon(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(attachments, sync, **kwargs) -> None:
    \"\"\"Proper docstring.

    Note: Keyword args (dict) to pass to ``attachments``:

        See ``flask_mail.Message.attach``.

        * filename:     filename of attachment
        * content_type: file mimetype
        * data:         the raw file data

    :param attachments: Iterable of kwargs to construct attachment.
    :param sync: Don't thread if True: Defaults to False.
    :param kwargs: Keyword args to pass to ``Message``:
        See ``flask_mail.Message``.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassOnlyParams(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(reduce: bool = False) -> _t.Tuple[str, ...]:
    \"\"\"Proper docstring.

    :param reduce: :func:`~lsfiles.utils._Tree.reduce`
    :return: Tuple of `Path` objects or str repr.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassReturnAny(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(*args: _t.Any, **kwargs: bool) -> _t.Any:
    \"\"\"Proper docstring.

    :param args: Manipulate string(s).
    :key format: Return a string instead of a tuple if strings are
        passed as tuple.
    :return: Colored string or None.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassPoorIndent(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def get_post(
        id: int, version: t.Optional[int] = None, checkauthor: bool = True
) -> Post:
    \"\"\"Get post by post's ID or abort with ``404: Not Found.``

    Standard behaviour would be to return None, so do not bypass
     silently.

     :param id: The post's ID.
     :param version: If provided populate session object with
        version.
     :param checkauthor: Rule whether to check for author ID.
     :return: Post's connection object.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FailNoSpace(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1) -> None:
    \"\"\"Proper docstring.

    :param param1:Passes.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E103


@_templates.register
class _PassBinOp(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def get_index(index: int, seq: _t.Sequence[_T]) -> _T | None:
    \"\"\"Fet index without throwing an error if index does not exist.

    :param index: Index to get.
    :param seq: Sequence object that can be indexed.
    :return: Item from index else None.
    \"\"\"
    try:
        return seq[index]
    except IndexError:
        return None
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FailBinOpRepr(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def get_index(index: int) -> _T | None:
    \"\"\"Get index without throwing an error if index does not exist.

    :return: Item from index else None.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""
def get_index({CROSS}index) -> {CHECK}_T | None:
    \"\"\"...

    :param None: {CROSS}
    :return: {CHECK}
    \"\"\"
"""
