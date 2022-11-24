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
ERR_GROUP = "f-e-1-0"
FUNC = "func"
E10 = "e-1-0"
CHECK_CLASS = "--check-class"
CHECK_PROTECTED = "--check-protected"
FAIL_PROTECT = "f-protect"
CHECK_OVERRIDDEN = "--check-overridden"
FAIL_OVERRIDE = "f-override"
CHECK_DUNDERS = "--check-dunders"
FAIL = "f"


@_templates.register
class _PassParamS(_BaseTemplate):
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
class _FParamDocsS(_BaseTemplate):
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
class _FParamSigS(_BaseTemplate):
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
class _FNoDocNoRetS(_BaseTemplate):
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
class _PassNoParamsS(_BaseTemplate):
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
class _PassUnderscoreParamS(_BaseTemplate):
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
class _FOutOfOrderS(_BaseTemplate):
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
class _PassRetTypeS(_BaseTemplate):
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
class _FRetTypeDocsS(_BaseTemplate):
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
class _FRetTypeSigS(_BaseTemplate):
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
class _FE109NoRetNoTypeS(_BaseTemplate):
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
class _FNoRetDocsNoTypeS(_BaseTemplate):
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
class _FRetDocsAttrTypeS(_BaseTemplate):
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
class _FRetDocsNameTypeS(_BaseTemplate):
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
class _FE101OutOfOrder1SumS(_BaseTemplate):
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
class _FIncorrectDocS(_BaseTemplate):
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
class _FE102ParamDocs1SumS(_BaseTemplate):
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
class _FE103ParamSig1SumS(_BaseTemplate):
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
class _FE104RetTypeDocs1SumS(_BaseTemplate):
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
class _FE105RetTypeSig1SumS(_BaseTemplate):
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
class _FDupesSumS(_BaseTemplate):
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
class _FIncorrectDocSumS(_BaseTemplate):
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
class _PassWithArgsS(_BaseTemplate):
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
class _FWithArgsS(_BaseTemplate):
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
class _PassWithKwargsS(_BaseTemplate):
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
class _FWithKwargsS(_BaseTemplate):
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
class _MultiFailS(_BaseTemplate):
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
class _FClassS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class Klass:
    def method(self, param1, param2, **kwargs) -> None:
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
class _PassClassSelfS(_BaseTemplate):
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
class _PassClassPropertyS(_BaseTemplate):
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
class _PassWithKwargsKeyS(_BaseTemplate):
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
class _FWithKwargsOutOfOrderS(_BaseTemplate):
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
class _PassDualColonS(_BaseTemplate):
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
class _PassOnlyParamsS(_BaseTemplate):
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
class _PassReturnAnyS(_BaseTemplate):
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
class _FMsgPoorIndentS(_BaseTemplate):
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
class _FE103NoSpaceS(_BaseTemplate):
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
class _PassBinOpS(_BaseTemplate):
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
class _FBinOpReprS(_BaseTemplate):
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
class _PassDoubleUnderscoreParamS(_BaseTemplate):
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
class _PassUnderscoreArgsKwargsS(_BaseTemplate):
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
class _PassPropertyNoReturnS(_BaseTemplate):
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
class _FPropertyReturnS(_BaseTemplate):
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
class _FHintMissingReturnS(_BaseTemplate):
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
class _FOverrideS(_BaseTemplate):
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
        return messages.E103


@_templates.register
class _FNoDocRetS(_BaseTemplate):
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
class _PassInconsistentSpaceS(_BaseTemplate):
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
class _FE109WRetQuestionS(_BaseTemplate):
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
class _FE109WORetQuestionS(_BaseTemplate):
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
class _FE110NES(_BaseTemplate):
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
class _FClassHeaderS(_BaseTemplate):
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
class _PassKWOnlyArgsS(_BaseTemplate):
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


@_templates.register
class _FInitS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
    
    def __init__(self, param1, param2) -> None:
        pass
"""

    @property
    def expected(self) -> str:
        return f"""\
class Klass:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"

    def __init__({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
"""


@_templates.register
class _PassPropNoRetTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class Klass:
    @property
    def method(self):
        \"\"\"Proper docstring.\"\"\"
        return self._method
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassInitNoRetS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    \"\"\"

    def __init__(self, param1, param2):
        pass
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassInitBadRetS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    \"\"\"

    # bad typing, but leave that up to mypy
    def __init__(self, param1, param2) -> int:
        pass
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FInitRetNoneS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :return: Fails
    \"\"\"

    def __init__(self, param1, param2) -> None:
        pass
"""

    @property
    def expected(self) -> str:
        return f"""
class Klass:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :return: {CROSS}
    \"\"\"

    def __init__({CHECK}param1, {CHECK}param2) -> {CROSS}None:
"""


@_templates.register
class _FE111S(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :return: Fails
    \"\"\"

    def __init__(param1, param2) -> None:
        pass
"""

    @property
    def expected(self) -> str:
        return messages.E111


@_templates.register
class _FProtectFuncS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def _function(param1, param2) -> None:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def _function({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"
"""


@_templates.register
class _FFuncPropS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
@property
def function(self) -> int:
    \"\"\"Docstring.
    
    :param self: Fails.
    \"\"\"
    return self._method
"""

    @property
    def expected(self) -> str:
        return messages.E105


@_templates.register
class _PassFuncPropReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
@property
def function(*_, **__) -> int:
    \"\"\"Docstring.

    :return: Returncode.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FFuncPropNoRetTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
@property
def method(self):
    \"\"\"Docstring.
    
    :param self: Fails.
    \"\"\"
    return self._method
"""

    @property
    def expected(self) -> str:
        return messages.E109


@_templates.register
class _FProtectNInitS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def __init__(param1, param2) -> None:
    pass
"""

    @property
    def expected(self) -> str:
        return messages.E103


@_templates.register
class _PassStaticSelfS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
    class Klass:
        @staticmethod
        def method(self, param1) -> None:
            \"\"\"Proper docstring.

            :param self: Pass.
            :param param1: Pass.
            \"\"\"
    """

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassClassNoSelfS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class Klass:

    # against convention but not up to this package to decide
    def method(no_self) -> None:
        \"\"\"Docstring.\"\"\"
        return None
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FProtectClsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class _Klass:
    def method(self, param1, param2, **kwargs) -> None:
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
class _FDunderS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class MutableSet:
    \"\"\"Set objet to inherit from.\"\"\"

    def __init__(self) -> None:
        self._set: _t.Set[T] = set()

    def __contains__(self, x: object) -> bool:
        return self._set.__contains__(x)

    def __len__(self) -> int:
        return self._set.__len__()

    def __iter__(self) -> _t.Iterator[T]:
        return self._set.__iter__()
"""

    @property
    def expected(self) -> str:
        return messages.E103


@_templates.register
class _FDunderParamS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    def __dunder__(self, param1, param2) -> None:
        \"\"\"...

        :param param1: Fails.
        :param param2: Fails.
        :param param3: Fails.
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def __dunder__({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"
"""


@_templates.register
class _FE112S(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param) -> None:
    \"\"\"Docstring.

    :param pram: Misspelled.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E112


@_templates.register
class _PassParamN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
        param1 : int
            Passes.
        param2 : int
            Passes.
        param3 : int
            Passes.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FParamDocsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2) -> None:
    \"\"\"...

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
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
class _FParamSigN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Not proper docstring.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
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
class _FNoDocNoRetN(_BaseTemplate):
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
class _PassNoParamsN(_BaseTemplate):
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
class _PassUnderscoreParamN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, _) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
        param1 : int
            Passes.
        param2 : int
            Passes.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FOutOfOrderN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3):
    \"\"\"Proper docstring.

    Parameters
    ----------
        param2 : int
            Fails.
        param3 : int
            Fails.
        param1 : int
            Fails.
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
class _PassRetTypeN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> int:
    \"\"\"Proper docstring.

    Parameters
    ----------
        param1 : int
            Passes.
        param2 : int
            Passes.
        param3 : int
            Passes.
    
    Returns
    -------
        int
            Passes.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FRetTypeDocsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.

    Returns
    -------
        int
            Fails.
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
class _FRetTypeSigN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> int:
    \"\"\"Proper docstring.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
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
class _FE109NoRetNoTypeN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3):
    \"\"\"Proper docstring.

    Parameters
    ----------
        param1 : int
            Passes.
        param2 : int
            Passes.
        param3 : int
            Passes.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E109


@_templates.register
class _FNoRetDocsNoTypeN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3):
    \"\"\"Proper docstring.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.

    Returns
    -------
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
class _FRetDocsAttrTypeN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
import typing as t

def function(param1) -> t.Optional[str]:
    \"\"\"Proper docstring.

    Parameters
    ----------
        param1 : int
            Fails.
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
class _FRetDocsNameTypeN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
from typing import Optional

def function(param1) -> Optional[str]:
    \"\"\"Proper docstring.

    Parameters
    ----------
        param1 : int
            Fails.
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
class _FE101OutOfOrder1SumN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
        param2 : int
            Fails.
        param3 : int
            Fails.
        param1 : int
            Fails.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return messages.E101


@_templates.register
class _FE102ParamDocs1SumN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2) -> None:
    \"\"\"...

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E102


@_templates.register
class _FE103ParamSig1SumN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Not proper docstring.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E103


@_templates.register
class _FE104RetTypeDocs1SumN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.

    Returns
    -------
    :return: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E104


@_templates.register
class _FE105RetTypeSig1SumN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> int:
    \"\"\"Proper docstring.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return messages.E105


@_templates.register
class _FDupesSumN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
        param1 : int
            Fails.
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E106


@_templates.register
class _PassWithArgsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, *args) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
        param1 : int
            Pass.
        param2 : int
            Pass.
        args : int
            Pass
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWithArgsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, *args) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
        param1 : int
            Pass.
        param2 : int
            Pass.
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
class _PassWithKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, **kwargs) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
        param1 : int
            Pass.
        param2 : int
            Pass.
        kwargs : int
            Pass
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWithKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, **kwargs) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
        param1 : int
            Pass.
        param2 : int
            Pass.
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
class _MultiFailN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function_1(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
        param2 : int
            Fails.
        param3 : int
            Fails.
        param1 : int
            Fails.
    \"\"\"
    return 0
    
def function_2(param1, param2) -> None:
    \"\"\"...

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
    \"\"\"
    
def function_3(param1, param2, param3) -> None:
    \"\"\"Not proper docstring.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
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
class _FClassN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class Klass:
    def method(self, param1, param2, **kwargs) -> None:
        \"\"\"Proper docstring.

        Parameters
        ----------
            param1 : int
                Pass.
            param2 : int
                Pass.
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
class _PassClassSelfN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class Klass:
    def method(self, param1) -> None:
        \"\"\"Proper docstring.

        Parameters
        ----------
            param1 : int
                Pass.
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassClassPropertyN(_BaseTemplate):
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
class _PassWithKwargsKeyN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, **kwargs) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
        param1 : int
            Passes

    **kwargs
        Passes
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWithKwargsOutOfOrderN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, **kwargs) -> None:
    \"\"\"Proper docstring.

    **kwargs
        Passes

    Parameters
    ----------
        param1 : int Fail
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassDualColonN(_BaseTemplate):
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

    Parameters
    ----------
        attachments : int
            Iterable of kwargs to construct attachment.
        sync : int
            Don't thread if True: Defaults to False.
        kwargs : int
            Keyword args to pass to ``Message``:
            See ``flask_mail.Message``.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassOnlyParamsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(reduce: bool = False) -> _t.Tuple[str, ...]:
    \"\"\"Proper docstring.

    Parameters
    ----------
        reduce : int
            :func:`~lsfiles.utils._Tree.reduce`

    Returns
    -------
        int
            Tuple of `Path` objects or str repr.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassReturnAnyN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(*args: _t.Any, **kwargs: bool) -> _t.Any:
    \"\"\"Proper docstring.

    Parameters
    ----------
        args : int
            Manipulate string(s).

    **kwargs
        Return a string instead of a tuple if strings are passed as tuple.

    Returns
    -------
        int
            Colored string or None.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassBinOpN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def get_index(index: int, seq: _t.Sequence[_T]) -> _T | None:
    \"\"\"Fet index without throwing an error if index does not exist.

    Parameters
    ----------
        index : int
            Index to get.
        seq : int
            Sequence object that can be indexed.

    Returns
    -------
        int
            Item from index else None.
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
class _FBinOpReprN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def get_index(index: int) -> _T | None:
    \"\"\"Get index without throwing an error if index does not exist.


    Returns
    -------
        int
            Item from index else None.
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
class _PassDoubleUnderscoreParamN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, __) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
        param1 : int
            Passes.
        param2 : int
            Passes.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassUnderscoreArgsKwargsN(_BaseTemplate):
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
class _PassPropertyNoReturnN(_BaseTemplate):
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
class _FPropertyReturnN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    @property
    def function(*_, **__) -> int:
        \"\"\"Proper docstring.
        

        Returns
        -------
            int
                Returncode.
        \"\"\"
        return 0
"""

    @property
    def expected(self) -> str:
        return messages.E108


@_templates.register
class _FOverrideN(_BaseTemplate):
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
        return messages.E103


@_templates.register
class _FNoDocRetN(_BaseTemplate):
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
class _FE109WRetQuestionN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function():
    \"\"\"Docstring.

    Returns
    -------
        int
            Does it?
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E109


@_templates.register
class _FE109WORetQuestionN(_BaseTemplate):
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
class _FE110NEN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(arg, param2) -> None:
    \"\"\"Docstring.
    
    Parameters
    ----------
        param1 : int
            not equal.
        para2 : int
            not equal.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E110


@_templates.register
class _FClassHeaderN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class Klass:
    def method(param1, param2, **kwargs) -> None:
        \"\"\"Proper docstring.

        Parameters
        ----------
            param1 : int
                Pass.
            param2 : int
                Pass.
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return "module/file.py::Klass::4"


@_templates.register
class _PassKWOnlyArgsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def docsig(
    *path: _Path,
    targets: _t.List[str] | None = None,
    disable: _t.List[str] | None = None,
) -> bool:
    \"\"\"...

    Parameters
    ----------
        path : int
            Path(s) to check.
        targets : int
            List of errors to target.
        disable : int
            List of errors to disable.

    Returns
    -------
        int
            Boolean value for whether there were any failures or not.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return """"""


@_templates.register
class _FInitN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
    \"\"\"
    
    def __init__(self, param1, param2) -> None:
        pass
"""

    @property
    def expected(self) -> str:
        return f"""\
class Klass:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"

    def __init__({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
"""


@_templates.register
class _PassPropNoRetTypeN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class Klass:
    @property
    def method(self):
        \"\"\"Proper docstring.\"\"\"
        return self._method
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassInitNoRetN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
    \"\"\"

    def __init__(self, param1, param2):
        pass
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassInitBadRetN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    Parameters
    ----------
    param1 : int
        Fails.
    param2 : int
        Fails.
    \"\"\"

    # bad typing, but leave that up to mypy
    def __init__(self, param1, param2) -> int:
        pass
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FInitRetNoneN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.

    Returns
    -------
        int
            Fails
    \"\"\"

    def __init__(self, param1, param2) -> None:
        pass
"""

    @property
    def expected(self) -> str:
        return f"""
class Klass:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :return: {CROSS}
    \"\"\"

    def __init__({CHECK}param1, {CHECK}param2) -> {CROSS}None:
"""


@_templates.register
class _FE111N(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.

    Returns
    -------
        int
            Fails
    \"\"\"

    def __init__(param1, param2) -> None:
        pass
"""

    @property
    def expected(self) -> str:
        return messages.E111


@_templates.register
class _FProtectFuncN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def _function(param1, param2) -> None:
    \"\"\"...

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def _function({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"
"""


@_templates.register
class _FFuncPropN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
@property
def function(self) -> int:
    \"\"\"Docstring.
    
    Parameters
    ----------
        self : Klass
            Fails.
    \"\"\"
    return self._method
"""

    @property
    def expected(self) -> str:
        return messages.E105


@_templates.register
class _PassFuncPropReturnN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
@property
def function(*_, **__) -> int:
    \"\"\"Docstring.

    Returns
    -------
        int
            Returncode.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FFuncPropNoRetTypeN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
@property
def method(self):
    \"\"\"Docstring.
    
    Parameters
    ----------
        self : Klass
            Fails.
    \"\"\"
    return self._method
"""

    @property
    def expected(self) -> str:
        return messages.E109


@_templates.register
class _FProtectNInitN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def __init__(param1, param2) -> None:
    pass
"""

    @property
    def expected(self) -> str:
        return messages.E103


@_templates.register
class _PassStaticSelfN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
    class Klass:
        @staticmethod
        def method(self, param1) -> None:
            \"\"\"Proper docstring.

            Parameters
            ----------
                self : Klass
                    Pass.
                param1 : int
                    Pass.
            \"\"\"
    """

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassClassNoSelfN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class Klass:

    # against convention but not up to this package to decide
    def method(no_self) -> None:
        \"\"\"Docstring.\"\"\"
        return None
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FProtectClsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class _Klass:
    def method(self, param1, param2, **kwargs) -> None:
        \"\"\"Proper docstring.

        Parameters
        ----------
            param1 : int
                Pass.
            param2 : int
                Pass.
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
class _FDunderN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class MutableSet:
    \"\"\"Set objet to inherit from.\"\"\"

    def __init__(self) -> None:
        self._set: _t.Set[T] = set()

    def __contains__(self, x: object) -> bool:
        return self._set.__contains__(x)

    def __len__(self) -> int:
        return self._set.__len__()

    def __iter__(self) -> _t.Iterator[T]:
        return self._set.__iter__()
"""

    @property
    def expected(self) -> str:
        return messages.E103


@_templates.register
class _FDunderParamN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    def __dunder__(self, param1, param2) -> None:
        \"\"\"...

        Parameters
        ----------
            param1 : int
                Fails.
            param2 : int
                Fails.
            param3 : int
                Fails.
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def __dunder__({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"
"""


@_templates.register
class _FE112N(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param) -> None:
    \"\"\"Docstring.

    Parameters
    ----------
        pram : int
            Misspelled.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E112


@_templates.register
class _PassSphinxWNumpy(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function() -> str:
    \"\"\"Proper docstring.

    :return: Returns is an indicator this could be a numpy docstring.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _NumpyNoIdent(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param) -> None:
    \"\"\"Docstring.

    Parameters
    ----------
    param : int
        Description.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _NumpyColonSpace(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param) -> None:
    \"\"\"Docstring.

    Parameters
    ----------
    param: int
        Description.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _Issue36Param(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def modify(numericString: Union[str, int]) -> str:
    \"\"\"Do stuff.

    Parameters
    ----------
    numericString: Union[str, int]
        numeric string that should be converted.

    Returns
    -------
    str
        reformatted string
    \"\"\"
    numericString = str(numericString)
    last = numericString[-1]
    middle = numericString[-3:-1]
    first = numericString[:-3]
    finalstring = "-".join([first, middle, last])
    return finalstring
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _Issue36Return(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def check_stuff(str_lin: str) -> bool:
    \"\"\"Check if "A" or "B".

    The function checks whether the string is "A" or "B".

    Parameters
    ----------
    str_lin: str
        special string produced by function_of_y

    Returns
    -------
    bool
        Returns True, else false
    \"\"\"
    if any(s in str_lin for s in ["A", "B"]):
        return True
    return False
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassParamNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
    param1: int
        Passes.
    param2: int
        Passes.
    param3: int
        Passes.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FParamDocsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2) -> None:
    \"\"\"...

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
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
class _FParamSigNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Not proper docstring.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
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
class _PassUnderscoreParamNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, _) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
    param1: int
        Passes.
    param2: int
        Passes.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FOutOfOrderNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3):
    \"\"\"Proper docstring.

    Parameters
    ----------
    param2: int
        Fails.
    param3: int
        Fails.
    param1: int
        Fails.
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
class _PassRetTypeNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> int:
    \"\"\"Proper docstring.

    Parameters
    ----------
    param1: int
        Passes.
    param2: int
        Passes.
    param3: int
        Passes.
    
    Returns
    -------
    int
        Passes.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FRetTypeDocsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.

    Returns
    -------
        int
            Fails.
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
class _FRetTypeSigNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> int:
    \"\"\"Proper docstring.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
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
class _FE109NoRetNoTypeNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3):
    \"\"\"Proper docstring.

    Parameters
    ----------
    param1: int
        Passes.
    param2: int
        Passes.
    param3: int
        Passes.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E109


@_templates.register
class _FNoRetDocsNoTypeNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3):
    \"\"\"Proper docstring.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.

    Returns
    -------
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
class _FRetDocsAttrTypeNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
import typing as t

def function(param1) -> t.Optional[str]:
    \"\"\"Proper docstring.

    Parameters
    ----------
    param1: int
        Fails.
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
class _FRetDocsNameTypeNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
from typing import Optional

def function(param1) -> Optional[str]:
    \"\"\"Proper docstring.

    Parameters
    ----------
    param1: int
        Fails.
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
class _FE101OutOfOrder1SumNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
    param2: int
        Fails.
    param3: int
        Fails.
    param1: int
        Fails.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return messages.E101


@_templates.register
class _FE102ParamDocs1SumNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2) -> None:
    \"\"\"...

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E102


@_templates.register
class _FE103ParamSig1SumNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Not proper docstring.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E103


@_templates.register
class _FE104RetTypeDocs1SumNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.

    Returns
    -------
    :return: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E104


@_templates.register
class _FE105RetTypeSig1SumNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> int:
    \"\"\"Proper docstring.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return messages.E105


@_templates.register
class _FDupesSumNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
    param1: int
        Fails.
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E106


@_templates.register
class _PassWithArgsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, *args) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
    param1: int
        Pass.
    param2: int
        Pass.
    args: int
        Pass
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWithArgsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, *args) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
    param1: int
        Pass.
    param2: int
        Pass.
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
class _PassWithKwargsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, **kwargs) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
    param1: int
        Pass.
    param2: int
        Pass.
    kwargs: int
        Pass
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWithKwargsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, **kwargs) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
    param1: int
        Pass.
    param2: int
        Pass.
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
class _MultiFailNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function_1(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
    param2: int
        Fails.
    param3: int
        Fails.
    param1: int
        Fails.
    \"\"\"
    return 0
    
def function_2(param1, param2) -> None:
    \"\"\"...

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
    \"\"\"
    
def function_3(param1, param2, param3) -> None:
    \"\"\"Not proper docstring.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
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
class _FClassNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class Klass:
    def method(self, param1, param2, **kwargs) -> None:
        \"\"\"Proper docstring.

        Parameters
        ----------
        param1: int
            Pass.
        param2: int
            Pass.
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
class _PassClassSelfNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class Klass:
    def method(self, param1) -> None:
        \"\"\"Proper docstring.

        Parameters
        ----------
        param1: int
            Pass.
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassWithKwargsKeyNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, **kwargs) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
    param1: int
        Passes

    **kwargs
        Passes
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWithKwargsOutOfOrderNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, **kwargs) -> None:
    \"\"\"Proper docstring.

    **kwargs
        Passes

    Parameters
    ----------
    param1: int
        Fail
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassDualColonNI(_BaseTemplate):
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

    Parameters
    ----------
    attachments: int
        Iterable of kwargs to construct attachment.
    sync: int
        Don't thread if True: Defaults to False.
    kwargs: int
        Keyword args to pass to ``Message``:
        See ``flask_mail.Message``.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassOnlyParamsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(reduce: bool = False) -> tuple[str, ...]:
    \"\"\"Proper docstring.

    Parameters
    ----------
    reduce: int
        :func:`~lsfiles.utils._Tree.reduce`

    Returns
    -------
    int
        Tuple of `Path` objects or str repr.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassReturnAnyNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(*args: _t.Any, **kwargs: bool) -> _t.Any:
    \"\"\"Proper docstring.

    Parameters
    ----------
    args: int
        Manipulate string(s).

    **kwargs
        Return a string instead of a tuple if strings are passed as tuple.

    Returns
    -------
    int
        Colored string or None.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassBinOpNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def get_index(index: int, seq: _t.Sequence[_T]) -> _T | None:
    \"\"\"Fet index without throwing an error if index does not exist.

    Parameters
    ----------
    index: int
        Index to get.
    seq: int
        Sequence object that can be indexed.

    Returns
    -------
    int
        Item from index else None.
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
class _FBinOpReprNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def get_index(index: int) -> _T | None:
    \"\"\"Get index without throwing an error if index does not exist.


    Returns
    -------
    int
        Item from index else None.
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
class _PassDoubleUnderscoreParamNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, __) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
    param1: int
        Passes.
    param2: int
        Passes.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FPropertyReturnNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    @property
    def function(*_, **__) -> int:
        \"\"\"Proper docstring.
        

        Returns
        -------
        int
            Returncode.
        \"\"\"
        return 0
"""

    @property
    def expected(self) -> str:
        return messages.E108


@_templates.register
class _FE109WRetQuestionNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function():
    \"\"\"Docstring.

    Returns
    -------
    int
        Does it?
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E109


@_templates.register
class _FE110NENI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(arg, param2) -> None:
    \"\"\"Docstring.
    
    Parameters
    ----------
    param1: int
        not equal.
    para2: int
        not equal.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E110


@_templates.register
class _PassKWOnlyArgsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def docsig(
    *path: _Path,
    targets: _t.List[str] | None = None,
    disable: _t.List[str] | None = None,
) -> bool:
    \"\"\"...

    Parameters
    ----------
    path: int
        Path(s) to check.
    targets: int
        List of errors to target.
    disable: int
        List of errors to disable.

    Returns
    -------
    int
        Boolean value for whether there were any failures or not.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return """"""


@_templates.register
class _FInitNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
    \"\"\"
    
    def __init__(self, param1, param2) -> None:
        pass
"""

    @property
    def expected(self) -> str:
        return f"""\
class Klass:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"

    def __init__({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
"""


@_templates.register
class _PassInitNoRetNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    \"\"\"

    def __init__(self, param1, param2):
        pass
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassInitBadRetNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    \"\"\"

    # bad typing, but leave that up to mypy
    def __init__(self, param1, param2) -> int:
        pass
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FInitRetNoneNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.

    Returns
    -------
    int
        Fails
    \"\"\"

    def __init__(self, param1, param2) -> None:
        pass
"""

    @property
    def expected(self) -> str:
        return f"""
class Klass:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :return: {CROSS}
    \"\"\"

    def __init__({CHECK}param1, {CHECK}param2) -> {CROSS}None:
"""


@_templates.register
class _FE111NI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.

    Returns
    -------
    int
        Fails
    \"\"\"

    def __init__(param1, param2) -> None:
        pass
"""

    @property
    def expected(self) -> str:
        return messages.E111


@_templates.register
class _FProtectFuncNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def _function(param1, param2) -> None:
    \"\"\"...

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def _function({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"
"""


@_templates.register
class _FFuncPropNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
@property
def function(self) -> int:
    \"\"\"Docstring.
    
    Parameters
    ----------
    self: Klass
        Fails.
    \"\"\"
    return self._method
"""

    @property
    def expected(self) -> str:
        return messages.E105


@_templates.register
class _PassFuncPropReturnNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
@property
def function(*_, **__) -> int:
    \"\"\"Docstring.

    Returns
    -------
    int
        Returncode.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FFuncPropNoRetTypeNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
@property
def method(self):
    \"\"\"Docstring.
    
    Parameters
    ----------
    self: Klass
        Fails.
    \"\"\"
    return self._method
"""

    @property
    def expected(self) -> str:
        return messages.E109


@_templates.register
class _PassStaticSelfNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
    class Klass:
        @staticmethod
        def method(self, param1) -> None:
            \"\"\"Proper docstring.

            Parameters
            ----------
            self: Klass
                Pass.
            param1: int
                Pass.
            \"\"\"
    """

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FProtectClsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class _Klass:
    def method(self, param1, param2, **kwargs) -> None:
        \"\"\"Proper docstring.

        Parameters
        ----------
        param1: int
            Pass.
        param2: int
            Pass.
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
class _FDunderParamNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    def __dunder__(self, param1, param2) -> None:
        \"\"\"...

        Parameters
        ----------
        param1: int
            Fails.
        param2: int
            Fails.
        param3: int
            Fails.
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def __dunder__({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"
"""


@_templates.register
class _FE112NI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param) -> None:
    \"\"\"Docstring.

    Parameters
    ----------
    pram: int
        Misspelled.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E112
