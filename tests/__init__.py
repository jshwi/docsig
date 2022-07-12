"""
tests
=====

Test package for ``docsig``.
"""
# pylint: disable=too-many-lines
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
NAME = "name"
TEMPLATE = "template"
ERR_GROUP = "fail-e-1-0"
FUNC = "func"
E10 = "e-1-0"


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
class _FailNoDocNoRet(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    pass
"""

    @property
    def expected(self) -> str:
        return messages.H104


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
def function({CROSS}param1, {CROSS}param2, {CROSS}param3)?:
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
class _FailE109NoRetNoType(_BaseTemplate):
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
        return messages.E109


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
def function({CHECK}param1, {CHECK}param2, {CHECK}param3)?:
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
class _FailE101OutOfOrder1Sum(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
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
class _FailE102ParamDocs1Sum(_BaseTemplate):
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
class _FailE103ParamSig1Sum(_BaseTemplate):
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
class _FailE104RetTypeDocs1Sum(_BaseTemplate):
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
class _FailE105RetTypeSig1Sum(_BaseTemplate):
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
def function_1(param1, param2, param3) -> None:
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
class _FailMsgPoorIndent(_BaseTemplate):
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
        return messages.H101


@_templates.register
class _FailE103NoSpace(_BaseTemplate):
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


@_templates.register
class _PassDoubleUnderscoreParam(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, __) -> None:
    \"\"\"Proper docstring.

    :param param1: Passes.
    :param param2: Passes.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassUnderscoreArgsKwargs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(*_, **__) -> None:
    \"\"\"Proper docstring.\"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassPropertyNoReturn(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    @property
    def function(*_, **__) -> int:
        \"\"\"Proper docstring.\"\"\"
        return 0
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FailPropertyReturn(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    @property
    def function(*_, **__) -> int:
        \"\"\"Proper docstring.
        
        :return: Returncode.
        \"\"\"
        return 0
"""

    @property
    def expected(self) -> str:
        return messages.E108


@_templates.register
class _FailHintMissingReturn(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def get_post() -> Post:
    \"\"\"Proper docstring.

     return: Post's connection object.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.H103


@_templates.register
class _PassSkipOverridden(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
import typing as _t

T = _t.TypeVar("T")


class MutableSet(_t.MutableSet[T]):
    \"\"\"Set objet to inherit from.\"\"\"

    def __init__(self) -> None:
        self._set: _t.Set[T] = set()

    def add(self, value: T) -> None:
        self._set.add(value)

    def discard(self, value: T) -> None:
        self._set.discard(value)

    def __contains__(self, x: object) -> bool:
        return self._set.__contains__(x)

    def __len__(self) -> int:
        return self._set.__len__()

    def __iter__(self) -> _t.Iterator[T]:
        return self._set.__iter__()
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FailNoDocRet(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function() -> int:
    pass
"""

    @property
    def expected(self) -> str:
        return messages.H104


@_templates.register
class _PassInconsistentSpace(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
@pytest.fixture(name="main")
def fixture_main(monkeypatch) -> t.Callable[..., None]:
    \"\"\"Function for passing mock ``main`` commandline arguments
    to package's main function.

    :param monkeypatch: ``pytest`` fixture for mocking attributes.
    :return:            Function for using this fixture.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FailE109WRetQuestion(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function():
    \"\"\"Docstring.
    
    :return: Does it?
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E109


@_templates.register
class _FailE109WORetQuestion(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function():
    \"\"\"Docstring.\"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E109


@_templates.register
class _FailE110NE(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(arg, param2) -> None:
    \"\"\"Docstring.
    
    :param param1: not equal.
    :param para2: not equal.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E110


@_templates.register
class _FailClassHeader(_BaseTemplate):
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
        return "module/file.py::Klass::4"


@_templates.register
class _PassKWOnlyArgs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def docsig(
    *path: _Path,
    targets: _t.List[str] | None = None,
    disable: _t.List[str] | None = None,
) -> bool:
    \"\"\"...

    :param path: Path(s) to check.
    :param targets: List of errors to target.
    :param disable: List of errors to disable.
    :return: Boolean value for whether there were any failures or not.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return """"""
