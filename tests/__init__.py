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
from templatest.utils import VarPrefix as _VarPrefix

from docsig.messages import TEMPLATE as T
from docsig.messages import E

MockMainType = t.Callable[..., t.Union[str, int]]


class InitFileFixtureType(
    t.Protocol
):  # pylint: disable=too-few-public-methods
    """Type for ``fixture_init_file``."""

    def __call__(self, content: str, path: Path = ..., /) -> Path:
        """Type for ``fixture_init_file``."""


short = _VarPrefix("-")
long = _VarPrefix("--", "-")
passed = _VarPrefix("p-", "-")
fail = _VarPrefix("f-", "-")

CHECK = "\u2713"
CROSS = "\u2716"

MULTI = "m"
NAME = "name"
TEMPLATE = "template"
EXPECTED = "expected"
E10 = "e-1-0"
FAIL = "f"
PASS = "p"
CHECK_ARGS = (
    long.check_class,
    long.check_protected,
    long.check_overridden,
    long.check_dunders,
    long.check_property_returns,
    long.check_protected_class_methods,
)
FAIL_CHECK_ARGS = tuple(f"f-{i[8:]}" for i in CHECK_ARGS)
ENABLE = "enable"
UNKNOWN = "unknown"
PATH = Path("module") / "file.py"


@_templates.register
class _PParamS(_BaseTemplate):
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
    \"\"\"
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
    \"\"\"
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
        return E[113].fstring(T)


@_templates.register
class _PNoParamsS(_BaseTemplate):
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
class _PUnderscoreParamS(_BaseTemplate):
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
    \"\"\"
    :param param2: {CROSS}
    :param param3: {CROSS}
    :param param1: {CROSS}
    \"\"\"
"""


@_templates.register
class _PRetTypeS(_BaseTemplate):
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
    \"\"\"
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
    \"\"\"
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
        return E[109].fstring(T)


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
    \"\"\"
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
    \"\"\"
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
    \"\"\"
    :param param1: {CHECK}
    :return: {CROSS}
    \"\"\"
"""


@_templates.register
class _FE101OutOfOrderSingleErrorS(_BaseTemplate):
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
        return E[101].fstring(T)


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
    \"\"\"
    :param param1: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _FE102ParamDocsSingleErrorS(_BaseTemplate):
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
        return E[102].fstring(T)


@_templates.register
class _FE103ParamSigSingleErrorS(_BaseTemplate):
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
        return E[103].fstring(T)


@_templates.register
class _FE104RetTypeDocsSingleErrorS(_BaseTemplate):
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
        return E[104].fstring(T)


@_templates.register
class _FE105RetTypeSigSingleErrorS(_BaseTemplate):
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
        return E[105].fstring(T)


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
        return E[106].fstring(T)


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
        return E[107].fstring(T)


@_templates.register
class _PWArgsS(_BaseTemplate):
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
class _FWArgsS(_BaseTemplate):
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
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _PWKwargsS(_BaseTemplate):
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
class _FWKwargsS(_BaseTemplate):
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
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _MFailS(_BaseTemplate):
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
{PATH}:2
----------------
def function_1({CROSS}param1, {CROSS}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param2: {CROSS}
    :param param3: {CROSS}
    :param param1: {CROSS}
    \"\"\"

{E[101].fstring(T)}

{PATH}:11
-----------------
def function_2({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"

{E[102].fstring(T)}

{PATH}:19
-----------------
def function_3({CHECK}param1, {CHECK}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"

{E[103].fstring(T)}

"""


@_templates.register
class _FMethodWKwargsS(_BaseTemplate):
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
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _PClassSelfS(_BaseTemplate):
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
class _FPropertyReturnsClassS(_BaseTemplate):
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
        return E[105].fstring(T)


@_templates.register
class _PWKwargsKeyS(_BaseTemplate):
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
class _FKwargsOutOfOrderS(_BaseTemplate):
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
        return f"""
def function({CROSS}param1, {CROSS}**kwargs) -> {CHECK}None:
    \"\"\"
    :key (**): {CROSS}
    :param param1: {CROSS}
    \"\"\"
"""


@_templates.register
class _PDualColonWKwargsS(_BaseTemplate):
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
class _POnlyParamsS(_BaseTemplate):
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
class _PReturnAnyWArgsWKwargsS(_BaseTemplate):
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
        return E[116].fstring(T)


@_templates.register
class _FE115NoSpaceS(_BaseTemplate):
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
        return E[115].fstring(T)


@_templates.register
class _PBinOpS(_BaseTemplate):
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
    \"\"\"
    :param None: {CROSS}
    :return: {CHECK}
    \"\"\"
"""


@_templates.register
class _PDoubleUnderscoreParamS(_BaseTemplate):
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
class _PUnderscoreArgsKwargsS(_BaseTemplate):
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
class _FPropertyReturnsS(_BaseTemplate):
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
        return E[105].fstring(T)


@_templates.register
class _PPropertyReturnS(_BaseTemplate):
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
        return ""


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
        return E[105].hint or ""


@_templates.register
class _FOverriddenS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
import typing as _t

T = _t.TypeVar("T")


class MutableSet(_t.MutableSet[T]):
    \"\"\"Set object to inherit from.\"\"\"

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
        return E[113].fstring(T)


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
        return E[113].fstring(T)


@_templates.register
class _PInconsistentSpaceS(_BaseTemplate):
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
        return E[109].fstring(T)


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
        return E[109].fstring(T)


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
        return E[110].fstring(T)


@_templates.register
class _FMethodHeaderWKwargsS(_BaseTemplate):
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
        return f"{PATH}:4 in Klass"


@_templates.register
class _PKWOnlyArgsWArgsS(_BaseTemplate):
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
class _FClassS(_BaseTemplate):
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
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"

    def __init__({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
"""


@_templates.register
class _FPropertyReturnsTypeS(_BaseTemplate):
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
        return E[109].fstring(T)


@_templates.register
class _PInitNoRetS(_BaseTemplate):
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
class _PInitBadRetS(_BaseTemplate):
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
class _FClassRetNoneS(_BaseTemplate):
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
    \"\"\"
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
        return E[111].fstring(T)


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
    \"\"\"
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
        return E[105].fstring(T)


@_templates.register
class _PFuncPropReturnS(_BaseTemplate):
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
        return E[109].fstring(T)


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
        return E[113].fstring(T)


@_templates.register
class _PStaticSelfS(_BaseTemplate):
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
class _PClassNoSelfS(_BaseTemplate):
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
class _FProtectClsWKwargsS(_BaseTemplate):
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
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _FDundersS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class MutableSet:
    \"\"\"Set object to inherit from.\"\"\"

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
        return E[113].fstring(T)


@_templates.register
class _FDundersParamS(_BaseTemplate):
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
    \"\"\"
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
        return E[112].fstring(T)


@_templates.register
class _PParamN(_BaseTemplate):
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
    \"\"\"
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
    \"\"\"
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
        return E[113].fstring(T)


@_templates.register
class _PNoParamsN(_BaseTemplate):
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
class _PUnderscoreParamN(_BaseTemplate):
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
    \"\"\"
    :param param2: {CROSS}
    :param param3: {CROSS}
    :param param1: {CROSS}
    \"\"\"
"""


@_templates.register
class _PRetTypeN(_BaseTemplate):
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
    \"\"\"
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
    \"\"\"
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
        return E[109].fstring(T)


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
        int
            :return: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CHECK}param3)?:
    \"\"\"
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
    \"\"\"
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
    \"\"\"
    :param param1: {CHECK}
    :return: {CROSS}
    \"\"\"
"""


@_templates.register
class _FE101OutOfOrderSingleErrorN(_BaseTemplate):
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
        return E[101].fstring(T)


@_templates.register
class _FE102ParamDocsSingleErrorN(_BaseTemplate):
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
        return E[102].fstring(T)


@_templates.register
class _FE103ParamSigSingleErrorN(_BaseTemplate):
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
        return E[103].fstring(T)


@_templates.register
class _FE104RetTypeDocsSingleErrorN(_BaseTemplate):
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
        :return: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return E[104].fstring(T)


@_templates.register
class _FE105RetTypeSigSingleErrorN(_BaseTemplate):
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
        return E[105].fstring(T)


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
        return E[106].fstring(T)


@_templates.register
class _PWArgsN(_BaseTemplate):
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
        *args : int
            Pass
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWArgsN(_BaseTemplate):
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
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _PWKwargsN(_BaseTemplate):
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
        **kwargs : int
            Pass
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWKwargsN(_BaseTemplate):
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
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _MFailN(_BaseTemplate):
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
{PATH}:2
----------------
def function_1({CROSS}param1, {CROSS}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param2: {CROSS}
    :param param3: {CROSS}
    :param param1: {CROSS}
    \"\"\"

{E[101].fstring(T)}

{PATH}:16
-----------------
def function_2({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"

{E[102].fstring(T)}

{PATH}:29
-----------------
def function_3({CHECK}param1, {CHECK}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"

{E[103].fstring(T)}

"""


@_templates.register
class _FMethodWKwargsN(_BaseTemplate):
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
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _PClassSelfN(_BaseTemplate):
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
class _FPropertyReturnsClassN(_BaseTemplate):
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
        return E[105].fstring(T)


@_templates.register
class _PWKwargsKeyN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, **kwargs) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
        param1 : int
            Passes
        **kwargs : int
            Passes
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FKwargsOutOfSectN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, **kwargs) -> None:
    \"\"\"Proper docstring.

    **kwargs : int
        Passes

    Parameters
    ----------
        param1 : int Fail
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return E[103].fstring(T)


@_templates.register
class _FKwargsOutOfOrderN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, **kwargs) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
        **kwargs : int
            Passes
        param1 : int
            Fail
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _PDualColonWKwargsN(_BaseTemplate):
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
        **kwargs : int
            Keyword args to pass to ``Message``:
            See ``flask_mail.Message``.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _POnlyParamsN(_BaseTemplate):
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
class _PReturnAnyWArgsWKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(*args: _t.Any, **kwargs: bool) -> _t.Any:
    \"\"\"Proper docstring.

    Parameters
    ----------
        *args : int
            Manipulate string(s).
        **kwargs : int
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
class _PBinOpN(_BaseTemplate):
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
    \"\"\"
    :param None: {CROSS}
    :return: {CHECK}
    \"\"\"
"""


@_templates.register
class _PDoubleUnderscoreParamN(_BaseTemplate):
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
class _PUnderscoreArgsKwargsN(_BaseTemplate):
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
class _FPropertyReturnsN(_BaseTemplate):
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
        return E[105].fstring(T)


@_templates.register
class _PPropertyReturnN(_BaseTemplate):
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
        return ""


@_templates.register
class _PPropertyReturnCachedN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    @cached_property
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
        return ""


@_templates.register
class _PPropertyReturnFunctoolsCachedN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
import functools

class Klass:
    @functools.cached_property
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
        return ""


@_templates.register
class _FOverriddenN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
import typing as _t

T = _t.TypeVar("T")


class MutableSet(_t.MutableSet[T]):
    \"\"\"Set object to inherit from.\"\"\"

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
        return E[113].fstring(T)


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
        return E[113].fstring(T)


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
        return E[109].fstring(T)


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
        return E[109].fstring(T)


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
        return E[110].fstring(T)


@_templates.register
class _FMethodHeaderWKwargsN(_BaseTemplate):
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
        return f"{PATH}:4 in Klass"


@_templates.register
class _PKWOnlyArgsWArgsN(_BaseTemplate):
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
class _FClassN(_BaseTemplate):
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
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"

    def __init__({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
"""


@_templates.register
class _FPropertyReturnsTypeN(_BaseTemplate):
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
        return E[109].fstring(T)


@_templates.register
class _PInitNoRetN(_BaseTemplate):
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
class _PInitBadRetN(_BaseTemplate):
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
class _FClassRetNoneN(_BaseTemplate):
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
    \"\"\"
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
        return E[111].fstring(T)


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
    \"\"\"
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
        return E[105].fstring(T)


@_templates.register
class _PFuncPropReturnN(_BaseTemplate):
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
        return E[109].fstring(T)


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
        return E[113].fstring(T)


@_templates.register
class _PStaticSelfN(_BaseTemplate):
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
class _PClassNoSelfN(_BaseTemplate):
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
class _FProtectClsWKwargsN(_BaseTemplate):
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
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _FDundersN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class MutableSet:
    \"\"\"Set object to inherit from.\"\"\"

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
        return E[113].fstring(T)


@_templates.register
class _FDundersParamN(_BaseTemplate):
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
    \"\"\"
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
        return E[112].fstring(T)


@_templates.register
class _PSphinxWNumpy(_BaseTemplate):
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
class _PNoIdentN(_BaseTemplate):
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
class _PColonSpaceN(_BaseTemplate):
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
class _PIssue36ParamN(_BaseTemplate):
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
class _PIssue36ReturnN(_BaseTemplate):
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
class _PParamNI(_BaseTemplate):
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
    \"\"\"
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
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _PUnderscoreParamNI(_BaseTemplate):
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
    \"\"\"
    :param param2: {CROSS}
    :param param3: {CROSS}
    :param param1: {CROSS}
    \"\"\"
"""


@_templates.register
class _PRetTypeNI(_BaseTemplate):
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
    \"\"\"
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
    \"\"\"
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
        return E[109].fstring(T)


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
    int
        :return: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CHECK}param3)?:
    \"\"\"
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
    \"\"\"
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
    \"\"\"
    :param param1: {CHECK}
    :return: {CROSS}
    \"\"\"
"""


@_templates.register
class _FE101OutOfOrderSingleErrorNI(_BaseTemplate):
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
        return E[101].fstring(T)


@_templates.register
class _FE102ParamDocsSingleErrorNI(_BaseTemplate):
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
        return E[102].fstring(T)


@_templates.register
class _FE103ParamSigSingleErrorNI(_BaseTemplate):
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
        return E[103].fstring(T)


@_templates.register
class _FE104RetTypeDocsSingleErrorNI(_BaseTemplate):
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
        :return: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return E[104].fstring(T)


@_templates.register
class _FE105RetTypeSigSingleErrorNI(_BaseTemplate):
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
        return E[105].fstring(T)


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
        return E[106].fstring(T)


@_templates.register
class _PWArgsNI(_BaseTemplate):
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
    *args: int
        Pass
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWArgsNI(_BaseTemplate):
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
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _PWKwargsNI(_BaseTemplate):
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
    **kwargs: int
        Pass
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWKwargsNI(_BaseTemplate):
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
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _MFailNI(_BaseTemplate):
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
{PATH}:2
----------------
def function_1({CROSS}param1, {CROSS}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param2: {CROSS}
    :param param3: {CROSS}
    :param param1: {CROSS}
    \"\"\"

{E[101].fstring(T)}

{PATH}:16
-----------------
def function_2({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"

{E[102].fstring(T)}

{PATH}:29
-----------------
def function_3({CHECK}param1, {CHECK}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"

{E[103].fstring(T)}

"""


@_templates.register
class _FMethodWKwargsNI(_BaseTemplate):
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
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _PClassSelfNI(_BaseTemplate):
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
class _PWKwargsKeyNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, **kwargs) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
    param1: int
        Passes
    **kwargs: int
        Passes
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWKwargsOutOfSectNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, **kwargs) -> None:
    \"\"\"Proper docstring.

    **kwargs: int
        Passes

    Parameters
    ----------
    param1: int
        Fail
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return E[103].fstring(T)


@_templates.register
class _FKwargsOutOfOrderNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, **kwargs) -> None:
    \"\"\"Proper docstring.

    Parameters
    ----------
    **kwargs : int
        Passes
    param1 : int
        Fail
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _PDualColonWKwargsNI(_BaseTemplate):
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
    **kwargs: int
        Keyword args to pass to ``Message``:
        See ``flask_mail.Message``.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _POnlyParamsNI(_BaseTemplate):
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
class _PReturnAnyWArgsWKwargsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(*args: _t.Any, **kwargs: bool) -> _t.Any:
    \"\"\"Proper docstring.

    Parameters
    ----------
    *args: int
        Manipulate string(s).
    **kwargs: int
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
class _PBinOpNI(_BaseTemplate):
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
    \"\"\"
    :param None: {CROSS}
    :return: {CHECK}
    \"\"\"
"""


@_templates.register
class _PDoubleUnderscoreParamNI(_BaseTemplate):
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
class _PPropertyReturnNI(_BaseTemplate):
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
        return ""


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
        return E[109].fstring(T)


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
        return E[110].fstring(T)


@_templates.register
class _PKWOnlyArgsWArgsNI(_BaseTemplate):
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
class _FClassNI(_BaseTemplate):
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
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"

    def __init__({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
"""


@_templates.register
class _PInitNoRetNI(_BaseTemplate):
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
class _PInitBadRetNI(_BaseTemplate):
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
class _FClassRetNoneNI(_BaseTemplate):
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
    \"\"\"
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
        return E[111].fstring(T)


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
    \"\"\"
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
        return E[105].fstring(T)


@_templates.register
class _PFuncPropReturnNI(_BaseTemplate):
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
        return E[109].fstring(T)


@_templates.register
class _PStaticSelfNI(_BaseTemplate):
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
class _FProtectClsWKwargsNI(_BaseTemplate):
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
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _FDundersParamNI(_BaseTemplate):
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
    \"\"\"
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
        return E[112].fstring(T)


@_templates.register
class _PRetTypeSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> int:
    \"\"\"Proper docstring.

    :param param1: Passes.
    :param param2: Passes.
    :param param3: Passes.
    :returns: Passes.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FRetTypeDocsSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :returns: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CHECK}param3) -> {CROSS}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CHECK}
    :return: {CROSS}
    \"\"\"
"""


@_templates.register
class _FNoRetDocsNoTypeSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3):
    \"\"\"Proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :returns: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CHECK}param3)?:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CHECK}
    :return: {CROSS}
    \"\"\"
"""


@_templates.register
class _FE104RetTypeDocsSingleErrorSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :returns: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return E[104].fstring(T)


@_templates.register
class _POnlyParamsSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(reduce: bool = False) -> _t.Tuple[str, ...]:
    \"\"\"Proper docstring.

    :param reduce: :func:`~lsfiles.utils._Tree.reduce`
    :returns: Tuple of `Path` objects or str repr.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PReturnAnyWArgsWKwargsSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(*args: _t.Any, **kwargs: bool) -> _t.Any:
    \"\"\"Proper docstring.

    :param args: Manipulate string(s).
    :key format: Return a string instead of a tuple if strings are
        passed as tuple.
    :returns: Colored string or None.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FMsgPoorIndentSRs(_BaseTemplate):
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
     :returns: Post's connection object.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return E[116].fstring(T)


@_templates.register
class _PBinOpSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def get_index(index: int, seq: _t.Sequence[_T]) -> _T | None:
    \"\"\"Fet index without throwing an error if index does not exist.

    :param index: Index to get.
    :param seq: Sequence object that can be indexed.
    :returns: Item from index else None.
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
class _FBinOpReprSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def get_index(index: int) -> _T | None:
    \"\"\"Get index without throwing an error if index does not exist.

    :returns: Item from index else None.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""
def get_index({CROSS}index) -> {CHECK}_T | None:
    \"\"\"
    :param None: {CROSS}
    :return: {CHECK}
    \"\"\"
"""


@_templates.register
class _PPropertyReturnSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    @property
    def function(*_, **__) -> int:
        \"\"\"Proper docstring.

        :returns: Returncode.
        \"\"\"
        return 0
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FHintMissingReturnSRs(_BaseTemplate):
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
        return E[105].hint or ""


@_templates.register
class _PInconsistentSpaceSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
@pytest.fixture(name="main")
def fixture_main(monkeypatch) -> t.Callable[..., None]:
    \"\"\"Function for passing mock ``main`` commandline arguments
    to package's main function.

    :param monkeypatch: ``pytest`` fixture for mocking attributes.
    :returns:            Function for using this fixture.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FE109WRetQuestionSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function():
    \"\"\"Docstring.

    :returns: Does it?
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return E[109].fstring(T)


@_templates.register
class _PKWOnlyArgsWArgsSRs(_BaseTemplate):
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
    :returns: Boolean value for whether there were any failures or not.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return """"""


@_templates.register
class _FClassRetNoneSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :returns: Fails
    \"\"\"

    def __init__(self, param1, param2) -> None:
        pass
"""

    @property
    def expected(self) -> str:
        return f"""
class Klass:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :return: {CROSS}
    \"\"\"

    def __init__({CHECK}param1, {CHECK}param2) -> {CROSS}None:
"""


@_templates.register
class _FE111SRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :returns: Fails
    \"\"\"

    def __init__(param1, param2) -> None:
        pass
"""

    @property
    def expected(self) -> str:
        return E[111].fstring(T)


@_templates.register
class _PFuncPropReturnSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
@property
def function(*_, **__) -> int:
    \"\"\"Docstring.

    :returns: Returncode.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PParamG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    Args:
        param1 (int): Passes.
        param2 (int): Passes.
        param3 (int): Passes.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FParamDocsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2) -> None:
    \"\"\"...

    Args:
        param1 (int): Passes.
        param2 (int): Passes.
        param3 (int): Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"
"""


@_templates.register
class _FParamSigG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Not proper docstring.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _FOutOfOrderG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3):
    \"\"\"Proper docstring.

    Args:
        param2 (int): Fails.
        param3 (int): Fails.
        param1 (int): Fails.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CROSS}param1, {CROSS}param2, {CROSS}param3)?:
    \"\"\"
    :param param2: {CROSS}
    :param param3: {CROSS}
    :param param1: {CROSS}
    \"\"\"
"""


@_templates.register
class _PRetTypeG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> int:
    \"\"\"Proper docstring.

    Args:
        param1 (int): Pass.
        param2 (int): Pass.
        param3 (int): Pass.

    Returns:
        bool: Pass.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FRetTypeDocsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.

    Returns:
        bool: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CHECK}param3) -> {CROSS}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CHECK}
    :return: {CROSS}
    \"\"\"
"""


@_templates.register
class _FRetTypeSigG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> int:
    \"\"\"Proper docstring.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CHECK}param3) -> {CROSS}int:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CHECK}
    :return: {CROSS}
    \"\"\"
"""


@_templates.register
class _FE109NoRetNoTypeG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3):
    \"\"\"Proper docstring.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return E[109].fstring(T)


@_templates.register
class _FNoRetDocsNoTypeG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3):
    \"\"\"Proper docstring.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.

    Returns:
        bool: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CHECK}param3)?:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CHECK}
    :return: {CROSS}
    \"\"\"
"""


@_templates.register
class _FRetDocsAttrTypeG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
import typing as t

def function(param1) -> t.Optional[str]:
    \"\"\"Proper docstring.

    Args:
        param1 (int): Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1) -> {CROSS}Optional[str]:
    \"\"\"
    :param param1: {CHECK}
    :return: {CROSS}
    \"\"\"
"""


@_templates.register
class _FRetDocsNameTypeG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
from typing import Optional

def function(param1) -> Optional[str]:
    \"\"\"Proper docstring.

    Args:
        param1 (int): Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1) -> {CROSS}Optional[str]:
    \"\"\"
    :param param1: {CHECK}
    :return: {CROSS}
    \"\"\"
"""


@_templates.register
class _FE101OutOfOrderSingleErrorG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    Args:
        param2 (int): Fails.
        param3 (int): Fails.
        param1 (int): Fails.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _FE102ParamDocsSingleErrorG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2) -> None:
    \"\"\"...

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return E[102].fstring(T)


@_templates.register
class _FE103ParamSigSingleErrorG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Not proper docstring.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return E[103].fstring(T)


@_templates.register
class _FE104RetTypeDocsSingleErrorG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.

    Returns:
        bool: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return E[104].fstring(T)


@_templates.register
class _FE105RetTypeSigSingleErrorG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> int:
    \"\"\"Proper docstring.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return E[105].fstring(T)


@_templates.register
class _FDupesSumG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    Args:
        param1 (int): Fails.
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return E[106].fstring(T)


@_templates.register
class _PWArgsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, *args) -> None:
    \"\"\"Proper docstring.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        *args (int): Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWArgsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, *args) -> None:
    \"\"\"Proper docstring.

    Args:
        param1 (int): Pass.
        param2 (int): Pass.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CROSS}*args) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _PWKwargsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, **kwargs) -> None:
    \"\"\"Proper docstring.

    Args:
        param1 (int): Pass.
        param2 (int): Pass.
        **kwargs (int): Pass.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWKwargsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, **kwargs) -> None:
    \"\"\"Proper docstring.

    Args:
        param1 (int): Pass.
        param2 (int): Pass.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CROSS}**kwargs) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _MFailG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function_1(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    Args:
        param2 (int): Fails.
        param3 (int): Fails.
        param1 (int): Fails.
    \"\"\"
    return 0

def function_2(param1, param2) -> None:
    \"\"\"...

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    \"\"\"

def function_3(param1, param2, param3) -> None:
    \"\"\"Not proper docstring.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2
----------------
def function_1({CROSS}param1, {CROSS}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param2: {CROSS}
    :param param3: {CROSS}
    :param param1: {CROSS}
    \"\"\"

{E[101].fstring(T)}

{PATH}:12
-----------------
def function_2({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"

{E[102].fstring(T)}

{PATH}:21
-----------------
def function_3({CHECK}param1, {CHECK}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"

{E[103].fstring(T)}

"""


@_templates.register
class _FMethodWKwargsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class Klass:
    def method(self, param1, param2, **kwargs) -> None:
        \"\"\"Proper docstring.

    Args:
        param1 (int): Pass.
        param2 (int): Pass.
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def method({CHECK}param1, {CHECK}param2, {CROSS}**kwargs) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _PClassSelfG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class Klass:
    def method(self, param1) -> None:
        \"\"\"Proper docstring.

        Args:
            param1 (int): Pass.
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PWKwargsKeyG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, **kwargs) -> None:
    \"\"\"Proper docstring.

    Args:
        param1 (int): Pass.
        **kwargs (int): Pass.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWKwargsOutOfSectG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, **kwargs) -> None:
    \"\"\"Proper docstring.

    **kwargs (int): Fails

    Args:
        param1 (int): Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return E[103].fstring(T)


@_templates.register
class _FKwargsOutOfOrderG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, **kwargs) -> None:
    \"\"\"Proper docstring.

    Args:
        **kwargs (int): Fails.
        param1 (int): Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _PDualColonWKwargsG(_BaseTemplate):
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

    Args:
        attachments (int): Iterable of kwargs to construct attachment.
        sync (int): Don't thread if True: Defaults to False.
        **kwargs (int): Keyword args to pass to ``Message``: See
            ``flask_mail.Message``.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _POnlyParamsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(reduce: bool = False) -> _t.Tuple[str, ...]:
    \"\"\"Proper docstring.

    Args:
        reduce (int): :func:`~lsfiles.utils._Tree.reduce`

    Returns:
        int: Tuple of `Path` objects or str repr.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PReturnAnyWArgsWKwargsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(*args: _t.Any, **kwargs: bool) -> _t.Any:
    \"\"\"Proper docstring.

    Args:
        *args (int): Manipulate string(s).
        **kwargs (int): Return a string instead of a tuple if strings
            are passed as tuple.

    Returns:
        int: Colored string or None.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PBinOpG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def get_index(index: int, seq: _t.Sequence[_T]) -> _T | None:
    \"\"\"Fet index without throwing an error if index does not exist.

    Args:
        index (int): Index to get.
        seq (int): Sequence object that can be indexed.

    Returns:
        int: Item from index else None.
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
class _FBinOpReprG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def get_index(index: int) -> _T | None:
    \"\"\"Get index without throwing an error if index does not exist.


    Returns:
        int: Item from index else None.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""
def get_index({CROSS}index) -> {CHECK}_T | None:
    \"\"\"
    :param None: {CROSS}
    :return: {CHECK}
    \"\"\"
"""


@_templates.register
class _PDoubleUnderscoreParamG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, __) -> None:
    \"\"\"Proper docstring.

    Args:
        param1 (int): Passes.
        param2 (int): Passes.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PPropertyReturnG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    @property
    def function(*_, **__) -> int:
        \"\"\"Proper docstring.

        Returns:
            int: Returncode.
        \"\"\"
        return 0
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FE109WRetQuestionG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function():
    \"\"\"Docstring.

    Returns:
        int: Does it?
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return E[109].fstring(T)


@_templates.register
class _FE110NEG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(arg, param2) -> None:
    \"\"\"Docstring.

    Args:
        param1 (int): Not equal.
        para2 (int): Not equal.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return E[110].fstring(T)


@_templates.register
class _PKWOnlyArgsWArgsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def docsig(
    *path: _Path,
    targets: _t.List[str] | None = None,
    disable: _t.List[str] | None = None,
) -> bool:
    \"\"\"...

    Args:
        path (int): Path(s) to check.
        targets (int): List of errors to target.
        disable (int): List of errors to disable.

    Returns:
        int: Boolean value for whether there were any failures or not.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return """"""


@_templates.register
class _FClassG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    \"\"\"

    def __init__(self, param1, param2) -> None:
        pass
"""

    @property
    def expected(self) -> str:
        return f"""\
class Klass:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"

    def __init__({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
"""


@_templates.register
class _PInitNoRetG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
    \"\"\"

    def __init__(self, param1, param2):
        pass
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PInitBadRetG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
    \"\"\"

    # bad typing, but leave that up to mypy
    def __init__(self, param1, param2) -> int:
        pass
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FClassRetNoneG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    Args:
        param1 (int): Fails.
        param2 (int): Fails.

    Returns:
        int: Fails
    \"\"\"

    def __init__(self, param1, param2) -> None:
        pass
"""

    @property
    def expected(self) -> str:
        return f"""
class Klass:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :return: {CROSS}
    \"\"\"

    def __init__({CHECK}param1, {CHECK}param2) -> {CROSS}None:
"""


@_templates.register
class _FE111G(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    Args:
        param1 (int): Fails.
        param2 (int): Fails.

    Returns:
        int: Fails
    \"\"\"

    def __init__(param1, param2) -> None:
        pass
"""

    @property
    def expected(self) -> str:
        return E[111].fstring(T)


@_templates.register
class _FProtectFuncG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def _function(param1, param2) -> None:
    \"\"\"...

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def _function({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"
"""


@_templates.register
class _FFuncPropG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
@property
def function(self) -> int:
    \"\"\"Docstring.

    Args:
        self (Klass): Fails.
    \"\"\"
    return self._method
"""

    @property
    def expected(self) -> str:
        return E[105].fstring(T)


@_templates.register
class _PFuncPropReturnG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
@property
def function(*_, **__) -> int:
    \"\"\"Docstring.

    Returns:
        int: Returncode.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FFuncPropNoRetTypeG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
@property
def method(self):
    \"\"\"Docstring.

    Returns:
        int: Returncode.
    \"\"\"
    return self._method
"""

    @property
    def expected(self) -> str:
        return E[109].fstring(T)


@_templates.register
class _PStaticSelfG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
    class Klass:
        @staticmethod
        def method(self, param1) -> None:
            \"\"\"Proper docstring.

            Args:
                self (Klass): Pass.
                param1 (int): Pass.
            \"\"\"
    """

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FProtectClsWKwargsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class _Klass:
    def method(self, param1, param2, **kwargs) -> None:
        \"\"\"Proper docstring.

        Args:
            param1 (int): Pass.
            param2 (int): Pass.
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def method({CHECK}param1, {CHECK}param2, {CROSS}**kwargs) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _FDundersParamG(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    def __dunder__(self, param1, param2) -> None:
        \"\"\"...

        Args:
            param1 (int): Fail.
            param2 (int): Fail.
            param3 (int): Fail.
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def __dunder__({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"
"""


@_templates.register
class _FE112G(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param) -> None:
    \"\"\"Docstring.

    Args:
        pram (int): Misspelled.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return E[112].fstring(T)


@_templates.register
class _PEscapedKwargWKwargsS(_BaseTemplate):
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
    :param **kwargs: Keyword args to pass to ``Message``:
        See ``flask_mail.Message``.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FNoKwargsIncludedWKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, **kwargs) -> None:
    \"\"\"Proper docstring.

    :param param1: Fail
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""
def function({CHECK}param1, {CROSS}**kwargs) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _FNoDocClassS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:

    def __init__(param1, param2, param3) -> None:
        pass
"""

    @property
    def expected(self) -> str:
        return E[114].fstring(T)


@_templates.register
class _FIssue36OffIndentN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def check_stuff(str_lin: str, a: str) -> bool:
    \"\"\"Check if "A" or "B".

    The function checks whether the string is "A" or "B".

    Parameters
    ----------
    str_lin: str
        special string produced by function_of_y ["a"]
            a second wrong indent line
    a: str
        string stuff

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
        return f"""\
def check_stuff({CHECK}str_lin, {CHECK}a) -> {CHECK}bool:
    \"\"\"
    :param str_lin: {CHECK}
    :param a: {CHECK}
    :return: {CHECK}
    \"\"\"

{E[115].fstring(T)}
"""


@_templates.register
class _FOverriddenAncestorsMultipleS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
from __future__ import annotations

import typing as _t

T = _t.TypeVar("T")
KT = _t.TypeVar("KT")
VT = _t.TypeVar("VT")


class _MutableSequence(_t.MutableSequence[T]):
    \"\"\"List-object to inherit from.\"\"\"

    def __init__(self) -> None:
        self._list: list[T] = []

    def insert(self, index: int, value: T) -> None:
        self._list.insert(index, value)

    @_t.overload
    def __getitem__(self, i: int) -> T:
        ...

    @_t.overload
    def __getitem__(self, s: slice) -> _t.MutableSequence[T]:
        ...

    def __getitem__(self, i):
        return self._list.__getitem__(i)

    @_t.overload
    def __setitem__(self, i: int, o: T) -> None:
        ...

    @_t.overload
    def __setitem__(self, s: slice, o: _t.Iterable[T]) -> None:
        ...

    def __setitem__(self, i, o):
        return self._list.__setitem__(i, o)

    @_t.overload
    def __delitem__(self, i: int) -> None:
        ...

    @_t.overload
    def __delitem__(self, i: slice) -> None:
        ...

    def __delitem__(self, i):
        return self._list.__delitem__(i)

    def __len__(self):
        return self._list.__len__()


# without this, the test will fail (not ideal)
# TODO: remove this to test for why
class Param(_t.NamedTuple):
    \"\"\"A tuple of param types and their names.\"\"\"

    kind: str = "param"
    name: str | None = None
    description: str | None = None
    indent: int = 0


class Params(_MutableSequence[Param]):
    \"\"\"Represents collection of parameters.\"\"\"

    def insert(self, index: int, value: Param) -> None:
        pass
"""

    @property
    def expected(self) -> str:
        return E[113].fstring(T)


@_templates.register
class _PStringAnnotation(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def example(some_input: int) -> "int":
    \"\"\"
    Do something.

    Args:
        some_input: Random integer

    Returns:
        Unchanged input
    \"\"\"
    return some_input
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FNoParamS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def example(some_input: int) -> int:
    \"\"\"Return input.\"\"\"
    return some_input
"""

    @property
    def expected(self) -> str:
        return E[103].fstring(T)


@_templates.register
class _FMethodReturnHintS(_BaseTemplate):
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
        return E[111].hint or ""


@_templates.register
class _PIssue114PosOnlyArgsWArgsWKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def starmap(
    fun: Callable[..., Any],
    iterable: Sequence[Sequence[Any]],
    /,
    *args: Any,
    timeout: float = 0,
    show_progress: bool | None = None,
    **kwargs: Any,
) -> list[Job]:
    \"\"\"Submits many jobs to the queue.

    One for each sequence in the iterable.
    Waits for all to finish, then returns the results.

    Args:
        fun: ...
        iterable: ...
        *args: static arguments passed to the function.
        timeout: ...
        show_progress: ...
        **kwargs: static keyword-arguments passed to the function.

    Returns:
        ...
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PIssue114PosOnlyArgsSelfWArgsWKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    def starmap(
        self,
        fun: Callable[..., Any],
        iterable: Sequence[Sequence[Any]],
        /,
        *args: Any,
        timeout: float = 0,
        show_progress: bool | None = None,
        **kwargs: Any,
    ) -> list[Job]:
        \"\"\"Submits many jobs to the queue.

        One for each sequence in the iterable.
        Waits for all to finish, then returns the results.

        Args:
            fun: ...
            iterable: ...
            *args: static arguments passed to the function.
            timeout: ...
            show_progress: ...
            **kwargs: static keyword-arguments passed to the function.

        Returns:
            ...
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MPassOverloadS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
from typing import overload


@overload
def process(response: None) -> None:
    ...


@overload
def process(response: int) -> tuple[int, str]:
    ...


@overload
def process(response: bytes) -> str:
    ...


def process(response):
    \"\"\"process a response.

    :param response: the response to process
    :return: something depending on what the response is
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MFailOverloadMissingReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
from typing import overload


@overload
def process(response: None) -> None:
    ...


@overload
def process(response: int) -> tuple[int, str]:
    ...


@overload
def process(response: bytes) -> str:
    ...


def process(response):
    \"\"\"process a response.

    :param response: the response to process
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:20
-----------------
def process({CHECK}response) -> {CROSS}str:
    \"\"\"
    :param response: {CHECK}
    :return: {CROSS}
    \"\"\"

{E[105].fstring(T)}

"""


@_templates.register
class _MFailOverloadMissingParamS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
from typing import overload


@overload
def process(response: None) -> None:
    ...


@overload
def process(response: int) -> tuple[int, str]:
    ...


@overload
def process(response: bytes) -> str:
    ...


def process(response):
    \"\"\"process a response.

    :return: something depending on what the response is
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:20
-----------------
def process({CROSS}response) -> {CHECK}str:
    \"\"\"
    :param None: {CROSS}
    :return: {CHECK}
    \"\"\"

{E[103].fstring(T)}

"""


@_templates.register
class _MPassOverloadNoReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
from typing import overload


@overload
def process(response: None) -> None:
    ...


@overload
def process(response: int) -> None:
    ...


@overload
def process(response: bytes) -> None:
    ...


def process(response):
    \"\"\"process a response.

    :param response: the response to process
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MPassMultiOverloadsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
from typing import overload


@overload
def process(response: None) -> None:
    ...


@overload
def process(response: int) -> tuple[int, str]:
    ...


@overload
def process(response: bytes) -> str:
    ...


def process(response):
    \"\"\"process a response.

    :param response: the response to process
    :return: something depending on what the response is
    \"\"\"

@overload
def another_process(response: int) -> tuple[int, str]:
    ...


@overload
def another_process(response: bool) -> None:
    ...


@overload
def another_process(response: str) -> int:
    ...


def another_process(response):
    \"\"\"process another response.

    :param response: the response to process
    :return: something depending on what the response is
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MFailOverloadNoReturnDocumentedS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
from typing import overload


@overload
def process(response: None) -> None:
    ...


@overload
def process(response: int) -> None:
    ...


@overload
def process(response: bytes) -> None:
    ...


def process(response):
    \"\"\"process a response.

    :param response: the response to process
    :return: NoneType
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:20
-----------------
def process({CHECK}response) -> {CROSS}None:
    \"\"\"
    :param response: {CHECK}
    :return: {CROSS}
    \"\"\"

{E[104].fstring(T)}

"""


@_templates.register
class _MPassOverloadMethodS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
from typing import overload

class SomeClass:
    @overload
    def process(self, response: None) -> None:
        ...

    @overload
    def process(self, response: int) -> tuple[int, str]:
        ...

    @overload
    def process(self, response: bytes) -> str:
        ...

    def process(self, response):
        \"\"\"process a response.

        :param response: the response to process
        :return: something depending on what the response is
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MFailOverloadMethodMissingReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
from typing import overload

class SomeClass:
    @overload
    def process(self, response: None) -> None:
        ...

    @overload
    def process(self, response: int) -> tuple[int, str]:
        ...

    @overload
    def process(self, response: bytes) -> str:
        ...

    def process(self, response):
        \"\"\"process a response.

        :param response: the response to process
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:17 in SomeClass
------------------------------
def process({CHECK}response) -> {CROSS}str:
    \"\"\"
    :param response: {CHECK}
    :return: {CROSS}
    \"\"\"

{E[105].fstring(T)}

"""


@_templates.register
class _MFailOverloadMethodMissingParamS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
from typing import overload

class SomeClass:
    @overload
    def process(self, response: None) -> None:
        ...

    @overload
    def process(self, response: int) -> tuple[int, str]:
        ...

    @overload
    def process(self, response: bytes) -> str:
        ...

    def process(self, response):
        \"\"\"process a response.

        :return: something depending on what the response is
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:17 in SomeClass
------------------------------
def process({CROSS}response) -> {CHECK}str:
    \"\"\"
    :param None: {CROSS}
    :return: {CHECK}
    \"\"\"

{E[103].fstring(T)}

"""


@_templates.register
class _MPassOverloadMethodNoReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
from typing import overload

class SomeClass:
    @overload
    def process(self, response: None) -> None:
        ...

    @overload
    def process(self, response: int) -> tuple[int, str]:
        ...

    @overload
    def process(self, response: bytes) -> None:
        ...

    def process(self, response):
        \"\"\"process a response.

        :param response: the response to process
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MPassMultiOverloadMethodsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
from typing import overload

class SomeClass:
    @overload
    def process(self, response: None) -> None:
        ...

    @overload
    def process(self, response: int) -> tuple[int, str]:
        ...

    @overload
    def process(self, response: bytes) -> str:
        ...

    def process(self, response):
        \"\"\"process a response.

        :param response: the response to process
        :return: something depending on what the response is
        \"\"\"

    @overload
    def another_process(self, response: int) -> tuple[int, str]:
        ...

    @overload
    def another_process(self, response: bool) -> None:
        ...

    @overload
    def another_process(self, response: str) -> int:
        ...

    def another_process(self, response):
        \"\"\"process another response.

        :param response: the response to process
        :return: something depending on what the response is
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MFailOverloadMethodNoReturnDocumentedS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
from typing import overload

class SomeClass:
    @overload
    def process(self, response: None) -> None:
        ...

    @overload
    def process(self, response: int) -> tuple[int, str]:
        ...

    @overload
    def process(self, response: bytes) -> None:
        ...

    def process(self, response):
        \"\"\"process a response.

        :param response: the response to process
        :return: NoneType
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:17 in SomeClass
------------------------------
def process({CHECK}response) -> {CROSS}None:
    \"\"\"
    :param response: {CHECK}
    :return: {CROSS}
    \"\"\"

{E[104].fstring(T)}

"""


@_templates.register
class _PParamDocsCommentModuleS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
# docsig: disable
def function(param1, param2) -> None:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PParamDocsCommentFuncS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2) -> None:  # docsig: disable
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MFailCommentDisableFuncS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function_1(param1, param2, param3) -> None:  # docsig: disable
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
{PATH}:11
-----------------
def function_2({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"

{E[102].fstring(T)}

{PATH}:19
-----------------
def function_3({CHECK}param1, {CHECK}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"

{E[103].fstring(T)}

"""


@_templates.register
class _MPassCommentDisableModuleFirstS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
# docsig: disable
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
        return ""


@_templates.register
class _MFailCommentDisableModuleSecondS(_BaseTemplate):
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

# docsig: disable
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
{PATH}:2
----------------
def function_1({CROSS}param1, {CROSS}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param2: {CROSS}
    :param param3: {CROSS}
    :param param1: {CROSS}
    \"\"\"

{E[101].fstring(T)}

"""


@_templates.register
class _MFailCommentDisableModuleThirdS(_BaseTemplate):
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

# docsig: disable
def function_3(param1, param2, param3) -> None:
    \"\"\"Not proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2
----------------
def function_1({CROSS}param1, {CROSS}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param2: {CROSS}
    :param param3: {CROSS}
    :param param1: {CROSS}
    \"\"\"

{E[101].fstring(T)}

{PATH}:11
-----------------
def function_2({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"

{E[102].fstring(T)}

"""


@_templates.register
class _MFailCommentDisableModuleEnableS(_BaseTemplate):
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

# docsig: disable
def function_2(param1, param2) -> None:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
# docsig: enable

def function_3(param1, param2, param3) -> None:
    \"\"\"Not proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2
----------------
def function_1({CROSS}param1, {CROSS}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param2: {CROSS}
    :param param3: {CROSS}
    :param param1: {CROSS}
    \"\"\"

{E[101].fstring(T)}

{PATH}:21
-----------------
def function_3({CHECK}param1, {CHECK}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"

{E[103].fstring(T)}

"""


@_templates.register
class _MFailCommentDisableMixedS(_BaseTemplate):
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

# docsig: disable
def function_2(param1, param2) -> None:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
# docsig: enable

def function_3(param1, param2, param3) -> None:
    \"\"\"Not proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    \"\"\"

def function_4(param1, param2, param3) -> None:  # docsig: disable
    \"\"\"Proper docstring.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    \"\"\"
    return 0

# docsig: disable
def function_5(param1, param2) -> None:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
# docsig: enable

def function_6(param1, param2, param3) -> None:
    \"\"\"Not proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2
----------------
def function_1({CROSS}param1, {CROSS}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param2: {CROSS}
    :param param3: {CROSS}
    :param param1: {CROSS}
    \"\"\"

{E[101].fstring(T)}

{PATH}:21
-----------------
def function_3({CHECK}param1, {CHECK}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"

{E[103].fstring(T)}

{PATH}:47
-----------------
def function_6({CHECK}param1, {CHECK}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"

{E[103].fstring(T)}

"""


@_templates.register
class _PParamDocsCommentNoSpaceAfterCommentS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2) -> None:  #docsig:disable
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PParamDocsCommentNoSpaceAfterColonS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2) -> None:  # docsig:disable
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MFailCommentDisableEnableOneFuncS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
# docsig: disable
def function_1(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    \"\"\"
    return 0

def function_2(param1, param2) -> None:  # docsig: enable
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
{PATH}:12
-----------------
def function_2({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"

{E[102].fstring(T)}

"""


@_templates.register
class _MPassBadInlineDirective(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
# docsig: disable
def function_1(param1, param2, param3) -> None:  # docsig: ena
    \"\"\"

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    \"\"\"

def function_2(param1, param2) -> None:  # docsig: ena
    \"\"\"

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:3
----------------
def function_1({CROSS}param1, {CROSS}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param2: {CROSS}
    :param param3: {CROSS}
    :param param1: {CROSS}
    \"\"\"

{E[202].fstring(T).format(directive="ena")}

{PATH}:11
-----------------
def function_2({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"

{E[202].fstring(T).format(directive="ena")}

"""


@_templates.register
class _MPassBadModuleDirective(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
# docsig: disa
def function_1(param1, param2) -> None:
    \"\"\"

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"

def function_2(param1, param2, param3) -> None:
    \"\"\"

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:3
----------------
def function_1({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"

{E[102].fstring(T)}
{E[201].fstring(T).format(directive="disa")}

{PATH}:11
-----------------
def function_2({CROSS}param1, {CROSS}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param2: {CROSS}
    :param param3: {CROSS}
    :param param1: {CROSS}
    \"\"\"

{E[101].fstring(T)}
{E[201].fstring(T).format(directive="disa")}

"""


@_templates.register
class _MPylintDirective(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
# docsig: unknown
def function_1(param1, param2, param3) -> None:  # pylint: disable
    \"\"\"


    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    \"\"\"


# pylint: disable=unknown,unknown-the-third
def function_2(param1, param2) -> None:
    \"\"\"

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"


def function_3(  # docsig: enable=unknown,unknown-the-third
    param1, param2, param3
) -> None:
    \"\"\"

    :param param1: Fails.
    :param param2: Fails.
    \"\"\"


def function_4(param1, param2, param3) -> None:
    \"\"\"

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :return: Fails.
    \"\"\"


def function_5(param1, param2, param3) -> int:
    \"\"\"

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"


def f6(param, param2, param3) -> None:
    \"\"\"

    :param param: Fails.
    :param param: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"


def f7(param, param2, param3) -> None:
    \"\"\"

    :param param: Fails.
    :param param: Fails.
    :param param2: Fails.
    :param: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:3
----------------
def function_1({CROSS}param1, {CROSS}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param2: {CROSS}
    :param param3: {CROSS}
    :param param1: {CROSS}
    \"\"\"

{E[101].fstring(T)}
{E[201].fstring(T).format(directive=UNKNOWN)}

{PATH}:14
-----------------
def function_2({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"

{E[102].fstring(T)}
{E[201].fstring(T).format(directive=UNKNOWN)}

{PATH}:23
-----------------
def function_3({CHECK}param1, {CHECK}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"

{E[103].fstring(T)}
{E[201].fstring(T).format(directive=UNKNOWN)}
{E[204].fstring(T).format(directive=ENABLE, option=UNKNOWN)}
{E[204].fstring(T).format(directive=ENABLE, option="unknown-the-third")}

{PATH}:33
-----------------
def function_4({CHECK}param1, {CHECK}param2, {CHECK}param3) -> {CROSS}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CHECK}
    :return: {CROSS}
    \"\"\"

{E[104].fstring(T)}
{E[201].fstring(T).format(directive=UNKNOWN)}

{PATH}:43
-----------------
def function_5({CHECK}param1, {CHECK}param2, {CHECK}param3) -> {CROSS}int:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CHECK}
    :return: {CROSS}
    \"\"\"

{E[105].fstring(T)}
{E[201].fstring(T).format(directive=UNKNOWN)}

{PATH}:52
-----------------
def f6({CHECK}param, {CROSS}param2, {CROSS}param3, {CROSS}None) -> {CHECK}None:
    \"\"\"
    :param param: {CHECK}
    :param param: {CROSS}
    :param param2: {CROSS}
    :param param3: {CROSS}
    \"\"\"

{E[101].fstring(T)}
{E[102].fstring(T)}
{E[106].fstring(T)}
{E[201].fstring(T).format(directive=UNKNOWN)}

{PATH}:62
-----------------
def f7({CHECK}param, {CROSS}param2, {CROSS}param3, {CROSS}None) -> {CHECK}None:
    \"\"\"
    :param param: {CHECK}
    :param param: {CROSS}
    :param param2: {CROSS}
    :param None: {CROSS}
    \"\"\"

{E[101].fstring(T)}
{E[102].fstring(T)}
{E[106].fstring(T)}
{E[107].fstring(T)}
{E[201].fstring(T).format(directive=UNKNOWN)}

"""


@_templates.register
class _MInvalidDirectiveOptions(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
# docsig: unknown
def function_1(param1, param2, param3) -> None:  # pylint: disable
    \"\"\"E101


    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    \"\"\"


# pylint: disable=unknown,unknown-the-third
def function_2(param1, param2) -> None:
    \"\"\"

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"


def function_3(  # docsig: enable=unknown,unknown-the-third
    param1, param2, param3
) -> None:
    \"\"\"

    :param param1: Fails.
    :param param2: Fails.
    \"\"\"


def function_4(param1, param2, param3) -> None:
    \"\"\"

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :return: Fails.
    \"\"\"


def function_5(param1, param2, param3) -> int:
    \"\"\"

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"


def f6(param, param2, param3) -> None:
    \"\"\"

    :param param: Fails.
    :param param: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"


def f7(param, param2, param3) -> None:
    \"\"\"

    :param param: Fails.
    :param param: Fails.
    :param param2: Fails.
    :param: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:3
----------------
def function_1({CROSS}param1, {CROSS}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param2: {CROSS}
    :param param3: {CROSS}
    :param param1: {CROSS}
    \"\"\"

{E[101].fstring(T)}
{E[201].fstring(T).format(directive=UNKNOWN)}

{PATH}:14
-----------------
def function_2({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"

{E[102].fstring(T)}
{E[201].fstring(T).format(directive=UNKNOWN)}

{PATH}:23
-----------------
def function_3({CHECK}param1, {CHECK}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"

{E[103].fstring(T)}
{E[201].fstring(T).format(directive=UNKNOWN)}
{E[204].fstring(T).format(directive=ENABLE, option=UNKNOWN)}
{E[204].fstring(T).format(directive=ENABLE, option="unknown-the-third")}

{PATH}:33
-----------------
def function_4({CHECK}param1, {CHECK}param2, {CHECK}param3) -> {CROSS}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CHECK}
    :return: {CROSS}
    \"\"\"

{E[104].fstring(T)}
{E[201].fstring(T).format(directive=UNKNOWN)}

{PATH}:43
-----------------
def function_5({CHECK}param1, {CHECK}param2, {CHECK}param3) -> {CROSS}int:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CHECK}
    :return: {CROSS}
    \"\"\"

{E[105].fstring(T)}
{E[201].fstring(T).format(directive=UNKNOWN)}

{PATH}:52
-----------------
def f6({CHECK}param, {CROSS}param2, {CROSS}param3, {CROSS}None) -> {CHECK}None:
    \"\"\"
    :param param: {CHECK}
    :param param: {CROSS}
    :param param2: {CROSS}
    :param param3: {CROSS}
    \"\"\"

{E[101].fstring(T)}
{E[102].fstring(T)}
{E[106].fstring(T)}
{E[201].fstring(T).format(directive=UNKNOWN)}

{PATH}:62
-----------------
def f7({CHECK}param, {CROSS}param2, {CROSS}param3, {CROSS}None) -> {CHECK}None:
    \"\"\"
    :param param: {CHECK}
    :param param: {CROSS}
    :param param2: {CROSS}
    :param None: {CROSS}
    \"\"\"

{E[101].fstring(T)}
{E[102].fstring(T)}
{E[106].fstring(T)}
{E[107].fstring(T)}
{E[201].fstring(T).format(directive=UNKNOWN)}

"""


@_templates.register
class _MInvalidSingleDirectiveOptions(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function_3(  # docsig: enable=unknown
    param1, param2, param3
) -> None:
    \"\"\"

    :param param1: Fails.
    :param param2: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2
----------------
def function_3({CHECK}param1, {CHECK}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"

{E[103].fstring(T)}
{E[204].fstring(T).format(directive=ENABLE, option=UNKNOWN)}

"""


@_templates.register
class _FWClassConstructorFS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...\"\"\"

    def __init__(self, param1, param2) -> None:
        \"\"\"...

        :param param1: Fails.
        :param param2: Fails.
        :param param3: Fails.
        \"\"\"
        pass
"""

    @property
    def expected(self) -> str:
        return E[103].fstring(T)


@_templates.register
class _FWClassConstructorInitNoRetS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...\"\"\"

    def __init__(self, param1, param2):
        \"\"\"...

        :param param1: Fails.
        :param param2: Fails.
        \"\"\"
        pass
"""

    @property
    def expected(self) -> str:
        return E[103].fstring(T)


@_templates.register
class _FWClassConstructorInitBadRetS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...\"\"\"

    # bad typing, but leave that up to mypy
    def __init__(self, param1, param2) -> int:
        \"\"\"...

        :param param1: Fails.
        :param param2: Fails.
        \"\"\"
        pass
"""

    @property
    def expected(self) -> str:
        return E[103].fstring(T)


@_templates.register
class _FWClassConstructorRetNoneFS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...\"\"\"

    def __init__(self, param1, param2) -> None:
        \"\"\"...

        :param param1: Fails.
        :param param2: Fails.
        :return: Fails
        \"\"\"
        pass
"""

    @property
    def expected(self) -> str:
        return E[103].fstring(T)


@_templates.register
class _FWClassConstructorE111FS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...\"\"\"

    def __init__(param1, param2) -> None:
        \"\"\"...

        :param param1: Fails.
        :param param2: Fails.
        :return: Fails
        \"\"\"
        pass
"""

    @property
    def expected(self) -> str:
        return E[103].fstring(T)


@_templates.register
class _MInvalidSingleModuleDirectiveOptions(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
# docsig: enable=unknown
def function_3(param1, param2, param3) -> None:
    \"\"\"

    :param param1: Fails.
    :param param2: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:3
----------------
def function_3({CHECK}param1, {CHECK}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"
    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"

{E[103].fstring(T)}
{E[203].fstring(T).format(directive=ENABLE, option=UNKNOWN)}

"""


@_templates.register
class _MFailProtectedMethods(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class _Messages(_t.Dict[int, Message]):
    def __init__(self) -> None:
        self._this_should_not_need_a_docstring

    def fromcode(self, ref: str) -> Message:
        \"\"\"

        :param ref: Codes or symbolic reference.
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:3 in _Messages
-----------------------------
class _Messages:
    ...

    def __init__() -> {CHECK}None:

{E[114].fstring(T)}

{PATH}:6 in _Messages
-----------------------------
def fromcode({CHECK}ref) -> {CROSS}Message:
    \"\"\"
    :param ref: {CHECK}
    :return: {CROSS}
    \"\"\"

{E[105].fstring(T)}

"""


@_templates.register
class _MFDisableClassInlineCommentS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class _MessageSequence(_t.List[str]):  # docsig: disable
    def __init__(
        self,
        targets: list[_Message],
        disable: list[_Message],
    ) -> None:
        pass

    def add(self, value: _Message, hint: bool = False, **kwargs) -> None:
        \"\"\"Add an error to the container.

        :param value: Value to add.
        :param hint: Whether to print a hint or not.
        :param kwargs: Variable(s) if format string.
        \"\"\"


class Report(_MessageSequence):
    def order(self, sig: _Param, doc: _Param) -> None:
        if any(sig.name == i.name for i in self._func.docstring.args) or any(
            doc.name == i.name for i in self._func.signature.args
        ):
            self.add(_E[101])
"""

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:20 in Report
---------------------------
def order({CROSS}sig, {CROSS}doc) -> {CHECK}None:
    ...

{E[113].fstring(T)}

"""


@_templates.register
class _MFDisableClassModuleCommentDisableEnableS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
# docsig: disable
class _MessageSequence(_t.List[str]):
    def __init__(
        self,
        targets: list[_Message],
        disable: list[_Message],
    ) -> None:
        pass

    def add(self, value: _Message, hint: bool = False, **kwargs) -> None:
        \"\"\"Add an error to the container.

        :param value: Value to add.
        :param hint: Whether to print a hint or not.
        :param kwargs: Variable(s) if format string.
        \"\"\"


# docsig: enable


class Report(_MessageSequence):
    def order(self, sig: _Param, doc: _Param) -> None:
        if any(sig.name == i.name for i in self._func.docstring.args) or any(
            doc.name == i.name for i in self._func.signature.args
        ):
            self.add(_E[101])
"""

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:24 in Report
---------------------------
def order({CROSS}sig, {CROSS}doc) -> {CHECK}None:
    ...

{E[113].fstring(T)}

"""


@_templates.register
class _MFDisableClassModuleCommentDisableS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
# docsig: disable
class _MessageSequence(_t.List[str]):
    def __init__(
        self,
        targets: list[_Message],
        disable: list[_Message],
    ) -> None:
        pass

    def add(self, value: _Message, hint: bool = False, **kwargs) -> None:
        \"\"\"Add an error to the container.

        :param value: Value to add.
        :param hint: Whether to print a hint or not.
        :param kwargs: Variable(s) if format string.
        \"\"\"


class Report(_MessageSequence):
    def order(self, sig: _Param, doc: _Param) -> None:
        if any(sig.name == i.name for i in self._func.docstring.args) or any(
            doc.name == i.name for i in self._func.signature.args
        ):
            self.add(_E[101])
"""

    @property
    def expected(self) -> str:
        return ""
