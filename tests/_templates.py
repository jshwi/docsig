"""
tests
=====

Test package for ``docsig``.
"""

# pylint: disable=too-many-lines
from pathlib import Path

from templatest import BaseTemplate as _BaseTemplate
from templatest import templates as _templates

from docsig.messages import TEMPLATE as T
from docsig.messages import E

PATH = Path("module") / "file.py"


@_templates.register
class _PParamS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FParamDocsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FParamSigS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


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
        return E[101].fstring(T)


@_templates.register
class _PNoParamsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function() -> None:
    """Docstring summary."""
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PUnderscoreParamS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, _) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FOutOfOrderS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _PRetTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FRetTypeDocsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """
'''

    @property
    def expected(self) -> str:
        return E[502].fstring(T)


@_templates.register
class _FRetTypeSigS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FSIG501NoRetNoTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FNoRetDocsNoTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FRetDocsAttrTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1) -> t.Optional[str]:
    """Docstring summary.

    :param param1: Description of param1.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FRetDocsNameTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1) -> Optional[str]:
    """Docstring summary.

    :param param1: Description of param1.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FSIG402OutOfOrderSingleErrorS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _FIncorrectDocS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param: Description of param.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FSIG202ParamDocsSingleErrorS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FSIG203ParamSigSingleErrorS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FSIG502RetTypeDocsSingleErrorS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """
'''

    @property
    def expected(self) -> str:
        return E[502].fstring(T)


@_templates.register
class _FSIG503RetTypeSigSingleErrorS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FDupesSumS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """
'''

    @property
    def expected(self) -> str:
        return E[201].fstring(T)


@_templates.register
class _FIncorrectDocSumS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param: Description of param.
    """
'''

    @property
    def expected(self) -> str:
        return E[303].fstring(T)


@_templates.register
class _PWArgsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, *args) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param args: Pass
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWArgsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, *args) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PWKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, **kwargs) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param kwargs: Pass
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, **kwargs) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _MFailS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function_1(param1, param2, param3) -> None:
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2 in function_1
    {E[402].fstring(T)}
{PATH}:10 in function_2
    {E[202].fstring(T)}
{PATH}:18 in function_3
    {E[203].fstring(T)}
"""


@_templates.register
class _FMethodWKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:
    def method(self, param1, param2, **kwargs) -> None:
        """Docstring summary.

        :param param1: Description of param1.
        :param param2: Description of param2.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PClassSelfS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:
    def method(self, param1) -> None:
        """Docstring summary.

        :param param1: Description of param1.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FPropertyReturnsClassS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:
    @property
    def method(self) -> int:
        """Docstring summary."""
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _PWKwargsKeyS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Docstring summary.

    :param param1: Passes
    :key kwarg1: Pass
    :keyword kwarg2: Pass
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FKwargsOutOfOrderS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Docstring summary.

    :keyword kwarg1: Fail
    :keyword kwarg3: Fail
    :param param1: Description of param1
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _PDualColonWKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(attachments, sync, **kwargs) -> None:
    """Docstring summary.

    Note: Keyword args (dict) to pass to ``attachments``:

        See ``flask_mail.Message.attach``.

        * filename:     filename of attachment
        * content_type: file mimetype
        * data:         the raw file data

    :param attachments: Iterable of kwargs to construct attachment.
    :param sync: Don't thread if True: Defaults to False.
    :param kwargs: Keyword args to pass to ``Message``:
        See ``flask_mail.Message``.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _POnlyParamsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(reduce: bool = False) -> _t.Tuple[str, ...]:
    """Docstring summary.

    :param reduce: :func:`~lsfiles.utils._Tree.reduce`
    :return: Tuple of `Path` objects or str repr.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PReturnAnyWArgsWKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(*args: _t.Any, **kwargs: bool) -> _t.Any:
    """Docstring summary.

    :param args: Manipulate string(s).
    :key format: Return a string instead of a tuple if strings are
        passed as tuple.
    :return: Colored string or None.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FMsgPoorIndentS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(
        id: int, version: t.Optional[int] = None, checkauthor: bool = True
) -> Post:
    """Get post by post's ID or abort with ``404: Not Found.``

    Standard behaviour would be to return None, so do not bypass
     silently.

     :param id: The post's ID.
     :param version: If provided populate session object with
        version.
     :param checkauthor: Rule whether to check for author ID.
     :return: Post's connection object.
    """
'''

    @property
    def expected(self) -> str:
        return E[401].fstring(T)


@_templates.register
class _FSIG302NoSpaceS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1) -> None:
    """Docstring summary.

    :param param1:Passes.
    """
'''

    @property
    def expected(self) -> str:
        return E[302].fstring(T)


@_templates.register
class _PBinOpS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(index: int, seq: _t.Sequence[_T]) -> _T | None:
    """Fet index without throwing an error if index does not exist.

    :param index: Index to get.
    :param seq: Sequence object that can be indexed.
    :return: Item from index else None.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FBinOpReprS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(index: int) -> _T | None:
    """Get index without throwing an error if index does not exist.

    :return: Item from index else None.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PDoubleUnderscoreParamS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, __) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PUnderscoreArgsKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(*_, **__) -> None:
    """Docstring summary."""
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FPropertyReturnsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @property
    def function(*_, **__) -> int:
        """Docstring summary."""
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _PPropertyReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @property
    def function(*_, **__) -> int:
        """Docstring summary.

        :return: Return description.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FHintMissingReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function() -> Post:
    """Docstring summary.

     return: Post's connection object.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].hint or ""


@_templates.register
class _FOverriddenS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
import typing as _t

T = _t.TypeVar("T")

class MutableSet(_t.MutableSet[T]):
    """Set object to inherit from."""

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
'''

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


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
        return E[101].fstring(T)


@_templates.register
class _PInconsistentSpaceS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@pytest.fixture(name="main")
def fixture_main(monkeypatch) -> t.Callable[..., None]:
    """Function for passing mock ``main`` commandline arguments
    to package's main function.

    :param monkeypatch: ``pytest`` fixture for mocking attributes.
    :return:            Function for using this fixture.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FSIG501WRetQuestionS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function():
    """Docstring summary.

    :return: Return description.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FSIG501WORetQuestionS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function():
    """Docstring summary."""
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FSIG404NES(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(arg, param2) -> None:
    """Docstring summary.

    :param param1: Not equal.
    :param para2: Not equal.
    """
'''

    @property
    def expected(self) -> str:
        return E[404].fstring(T)


@_templates.register
class _FMethodHeaderWKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:
    def method(self, param1, param2, **kwargs) -> None:
        """Docstring summary.

        :param param1: Description of param1.
        :param param2: Description of param2.
        """
'''

    @property
    def expected(self) -> str:
        return f"{PATH}:4 in Klass"


@_templates.register
class _PKWOnlyArgsWArgsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(
    *path: _Path,
    targets: _t.List[str] | None = None,
    disable: _t.List[str] | None = None,
) -> bool:
    """Docstring summary.

    :param path: Path(s) to check.
    :param targets: List of errors to target.
    :param disable: List of errors to disable.
    :return: Boolean value for whether there were any failures or not.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FClassS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

    def __init__(self, param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FPropertyReturnsTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:
    @property
    def method(self):
        """Docstring summary."""
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _PInitNoRetS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """

    def __init__(self, param1, param2):
        pass
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PInitBadRetS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """

    # bad typing, but leave that up to mypy
    def __init__(self, param1, param2) -> int:
        pass
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FClassRetNoneS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :return: Return description.
    """

    def __init__(self, param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[504].fstring(T)


@_templates.register
class _FSIG504S(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :return: Return description.
    """

    def __init__(param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[504].fstring(T)


@_templates.register
class _FProtectFuncS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def _function(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FFuncPropS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def function(self) -> int:
    """Docstring summary.

    :param self: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _PFuncPropReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def function(*_, **__) -> int:
    """Docstring summary.

    :return: Return description.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FFuncPropNoRetTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def function(self):
    """Docstring summary.

    :param self: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


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
        return E[101].fstring(T)


@_templates.register
class _PStaticSelfS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @staticmethod
    def method(self, param1) -> None:
        """Docstring summary.

        :param self: Pass.
        :param param1: Description of param1.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PClassNoSelfS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:

    # against convention but not up to this package to decide
    def method(no_self) -> None:
        """Docstring summary."""
        return None
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FProtectClsWKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class _Klass:
    def method(self, param1, param2, **kwargs) -> None:
        """Docstring summary.

        :param param1: Description of param1.
        :param param2: Description of param2.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FDundersS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class MutableSet:
    """Set object to inherit from."""

    def __init__(self) -> None:
        self._set: _t.Set[T] = set()

    def __contains__(self, x: object) -> bool:
        return self._set.__contains__(x)

    def __len__(self) -> int:
        return self._set.__len__()

    def __iter__(self) -> _t.Iterator[T]:
        return self._set.__iter__()
'''

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _FDundersParamS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    def __dunder__(self, param1, param2) -> None:
        """Docstring summary.

        :param param1: Description of param1.
        :param param2: Description of param2.
        :param param3: Description of param3.
        """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FSIG403S(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param) -> None:
    """Docstring summary.

    :param pram: Misspelled.
    """
'''

    @property
    def expected(self) -> str:
        return E[403].fstring(T)


@_templates.register
class _PParamN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Passes.
        param2 : int
            Passes.
        param3 : int
            Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FParamDocsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2) -> None:
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FParamSigN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


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
        return E[101].fstring(T)


@_templates.register
class _PNoParamsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function() -> None:
    """Docstring summary."""
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PUnderscoreParamN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, _) -> None:
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Passes.
        param2 : int
            Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FOutOfOrderN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Docstring summary.

    Parameters
    ----------
        param2 : int
            Fails.
        param3 : int
            Fails.
        param1 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _PRetTypeN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Docstring summary.

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
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FRetTypeDocsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

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
    """
'''

    @property
    def expected(self) -> str:
        return E[502].fstring(T)


@_templates.register
class _FRetTypeSigN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FSIG501NoRetNoTypeN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Passes.
        param2 : int
            Passes.
        param3 : int
            Passes.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FNoRetDocsNoTypeN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Docstring summary.

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
            :return: Return description.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FRetDocsAttrTypeN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1) -> t.Optional[str]:
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FRetDocsNameTypeN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1) -> Optional[str]:
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FSIG402OutOfOrderSingleErrorN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    Parameters
    ----------
        param2 : int
            Fails.
        param3 : int
            Fails.
        param1 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _FSIG202ParamDocsSingleErrorN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2) -> None:
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FSIG203ParamSigSingleErrorN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FSIG502RetTypeDocsSingleErrorN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

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
        :return: Return description.
    """
'''

    @property
    def expected(self) -> str:
        return E[502].fstring(T)


@_templates.register
class _FSIG503RetTypeSigSingleErrorN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FDupesSumN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

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
    """
'''

    @property
    def expected(self) -> str:
        return E[201].fstring(T)


@_templates.register
class _PWArgsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, *args) -> None:
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Pass.
        param2 : int
            Pass.
        *args : int
            Pass
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWArgsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, *args) -> None:
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Pass.
        param2 : int
            Pass.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PWKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, **kwargs) -> None:
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Pass.
        param2 : int
            Pass.
        **kwargs : int
            Pass
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, **kwargs) -> None:
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Pass.
        param2 : int
            Pass.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _MFailN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function_1(param1, param2, param3) -> None:
    """Docstring summary.

    Parameters
    ----------
        param2 : int
            Fails.
        param3 : int
            Fails.
        param1 : int
            Fails.
    """

def function_2(param1, param2) -> None:
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2 in function_1
    {E[402].fstring(T)}
{PATH}:15 in function_2
    {E[202].fstring(T)}
{PATH}:28 in function_3
    {E[203].fstring(T)}
"""


@_templates.register
class _FMethodWKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    def method(self, param1, param2, **kwargs) -> None:
        """Docstring summary.

        Parameters
        ----------
            param1 : int
                Pass.
            param2 : int
                Pass.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PClassSelfN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    def method(self, param1) -> None:
        """Docstring summary.

        Parameters
        ----------
            param1 : int
                Pass.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FPropertyReturnsClassN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @property
    def method(self) -> int:
        """Docstring summary."""
        return self._method
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _PWKwargsKeyN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Passes
        **kwargs : int
            Passes
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FKwargsOutOfSectN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Docstring summary.

    **kwargs : int
        Passes

    Parameters
    ----------
        param1 : int Fail
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FKwargsOutOfOrderN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Docstring summary.

    Parameters
    ----------
        **kwargs : int
            Passes
        param1 : int
            Fail
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _PDualColonWKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(attachments, sync, **kwargs) -> None:
    """Docstring summary.

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
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _POnlyParamsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(reduce: bool = False) -> _t.Tuple[str, ...]:
    """Docstring summary.

    Parameters
    ----------
        reduce : int
            :func:`~lsfiles.utils._Tree.reduce`

    Returns
    -------
        int
            Tuple of `Path` objects or str repr.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PReturnAnyWArgsWKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(*args: _t.Any, **kwargs: bool) -> _t.Any:
    """Docstring summary.

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
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PBinOpN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(index: int, seq: _t.Sequence[_T]) -> _T | None:
    """Fet index without throwing an error if index does not exist.

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
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FBinOpReprN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(index: int) -> _T | None:
    """Get index without throwing an error if index does not exist.

    Returns
    -------
        int
            Item from index else None.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PDoubleUnderscoreParamN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, __) -> None:
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Passes.
        param2 : int
            Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PUnderscoreArgsKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(*_, **__) -> None:
    """Docstring summary."""
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FPropertyReturnsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @property
    def function(*_, **__) -> int:
        """Docstring summary."""
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _PPropertyReturnN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @property
    def function(*_, **__) -> int:
        """Docstring summary.

        Returns
        -------
            int
                Returncode.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PPropertyReturnCachedN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @cached_property
    def function(*_, **__) -> int:
        """Docstring summary.

        Returns
        -------
            int
                Returncode.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PPropertyReturnFunctoolsCachedN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @functools.cached_property
    def function(*_, **__) -> int:
        """Docstring summary.

        Returns
        -------
            int
                Returncode.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FOverriddenN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
import typing as _t

T = _t.TypeVar("T")

class MutableSet(_t.MutableSet[T]):
    """Set object to inherit from."""

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
'''

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


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
        return E[101].fstring(T)


@_templates.register
class _FSIG501WRetQuestionN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function():
    """Docstring summary.

    Returns
    -------
        int
            Does it?
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FSIG501WORetQuestionN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function():
    """Docstring summary."""
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FSIG404NEN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(arg, param2) -> None:
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Not equal.
        para2 : int
            Not equal.
    """
'''

    @property
    def expected(self) -> str:
        return E[404].fstring(T)


@_templates.register
class _FMethodHeaderWKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:
    def method(self, param1, param2, **kwargs) -> None:
        """Docstring summary.

        Parameters
        ----------
            param1 : int
                Pass.
            param2 : int
                Pass.
        """
'''

    @property
    def expected(self) -> str:
        return f"{PATH}:4 in Klass"


@_templates.register
class _PKWOnlyArgsWArgsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(
    *path: _Path,
    targets: _t.List[str] | None = None,
    disable: _t.List[str] | None = None,
) -> bool:
    """Docstring summary.

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
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FClassN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
    """

    def __init__(self, param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FPropertyReturnsTypeN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:
    @property
    def method(self):
        """Docstring summary."""
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _PInitNoRetN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
    """

    def __init__(self, param1, param2):
        pass
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PInitBadRetN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

    Parameters
    ----------
    param1 : int
        Fails.
    param2 : int
        Fails.
    """

    # bad typing, but leave that up to mypy
    def __init__(self, param1, param2) -> int:
        pass
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FClassRetNoneN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

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
    """

    def __init__(self, param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[504].fstring(T)


@_templates.register
class _FSIG504N(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

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
    """

    def __init__(param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[504].fstring(T)


@_templates.register
class _FProtectFuncN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def _function(param1, param2) -> None:
    """Docstring summary.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FFuncPropN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def function(self) -> int:
    """Docstring summary.

    Parameters
    ----------
        self : Klass
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _PFuncPropReturnN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def function(*_, **__) -> int:
    """Docstring summary.

    Returns
    -------
        int
            Returncode.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FFuncPropNoRetTypeN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def function(self):
    """Docstring summary.

    Parameters
    ----------
        self : Klass
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


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
        return E[101].fstring(T)


@_templates.register
class _PStaticSelfN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @staticmethod
    def method(self, param1) -> None:
        """Docstring summary.

        Parameters
        ----------
            self : Klass
                Pass.
            param1 : int
                Pass.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PClassNoSelfN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:

    # against convention but not up to this package to decide
    def method(no_self) -> None:
        """Docstring summary."""
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FProtectClsWKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class _Klass:
    def method(self, param1, param2, **kwargs) -> None:
        """Docstring summary.

        Parameters
        ----------
            param1 : int
                Pass.
            param2 : int
                Pass.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FDundersN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class MutableSet:
    """Set object to inherit from."""

    def __init__(self) -> None:
        self._set: _t.Set[T] = set()

    def __contains__(self, x: object) -> bool:
        return self._set.__contains__(x)

    def __len__(self) -> int:
        return self._set.__len__()

    def __iter__(self) -> _t.Iterator[T]:
        return self._set.__iter__()
'''

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _FDundersParamN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    def __dunder__(self, param1, param2) -> None:
        """Docstring summary.

        Parameters
        ----------
            param1 : int
                Fails.
            param2 : int
                Fails.
            param3 : int
                Fails.
        """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FSIG403N(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param) -> None:
    """Docstring summary.

    Parameters
    ----------
        pram : int
            Misspelled.
    """
'''

    @property
    def expected(self) -> str:
        return E[403].fstring(T)


@_templates.register
class _PSphinxWNumpy(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function() -> str:
    """Docstring summary.

    :return: Returns is an indicator this could be a numpy docstring.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PNoIdentN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param) -> None:
    """Docstring summary.

    Parameters
    ----------
    param : int
        Description.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PColonSpaceN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param) -> None:
    """Docstring summary.

    Parameters
    ----------
    param: int
        Description.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PIssue36ParamN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(numericString: Union[str, int]) -> str:
    """Do stuff.

    Parameters
    ----------
    numericString: Union[str, int]
        Numeric string that should be converted.

    Returns
    -------
    str
        Reformatted string
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PIssue36ReturnN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(str_lin: str) -> bool:
    """Check if "A" or "B".

    The function checks whether the string is "A" or "B".

    Parameters
    ----------
    str_lin: str
        Special string produced by function_of_y

    Returns
    -------
    bool
        Returns True, else false
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PParamNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Passes.
    param2: int
        Passes.
    param3: int
        Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FParamDocsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2) -> None:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FParamSigNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PUnderscoreParamNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, _) -> None:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Passes.
    param2: int
        Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FOutOfOrderNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Docstring summary.

    Parameters
    ----------
    param2: int
        Fails.
    param3: int
        Fails.
    param1: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _PRetTypeNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Docstring summary.

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
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FRetTypeDocsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

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
    """
'''

    @property
    def expected(self) -> str:
        return E[502].fstring(T)


@_templates.register
class _FRetTypeSigNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FSIG501NoRetNoTypeNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Passes.
    param2: int
        Passes.
    param3: int
        Passes.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FNoRetDocsNoTypeNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Docstring summary.

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
        :return: Return description.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FRetDocsAttrTypeNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1) -> t.Optional[str]:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FRetDocsNameTypeNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1) -> Optional[str]:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FSIG402OutOfOrderSingleErrorNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    Parameters
    ----------
    param2: int
        Fails.
    param3: int
        Fails.
    param1: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _FSIG202ParamDocsSingleErrorNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2) -> None:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FSIG203ParamSigSingleErrorNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FSIG502RetTypeDocsSingleErrorNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

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
        :return: Return description.
    """
'''

    @property
    def expected(self) -> str:
        return E[502].fstring(T)


@_templates.register
class _FSIG503RetTypeSigSingleErrorNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FDupesSumNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

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
    """
'''

    @property
    def expected(self) -> str:
        return E[201].fstring(T)


@_templates.register
class _PWArgsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, *args) -> None:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Pass.
    param2: int
        Pass.
    *args: int
        Pass
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWArgsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, *args) -> None:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Pass.
    param2: int
        Pass.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PWKwargsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, **kwargs) -> None:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Pass.
    param2: int
        Pass.
    **kwargs: int
        Pass
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWKwargsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, **kwargs) -> None:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Pass.
    param2: int
        Pass.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _MFailNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function_1(param1, param2, param3) -> None:
    """Docstring summary.

    Parameters
    ----------
    param2: int
        Fails.
    param3: int
        Fails.
    param1: int
        Fails.
    """

def function_2(param1, param2) -> None:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2 in function_1
    {E[402].fstring(T)}
{PATH}:15 in function_2
    {E[202].fstring(T)}
{PATH}:28 in function_3
    {E[203].fstring(T)}
"""


@_templates.register
class _FMethodWKwargsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:
    def method(self, param1, param2, **kwargs) -> None:
        """Docstring summary.

        Parameters
        ----------
        param1: int
            Pass.
        param2: int
            Pass.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PClassSelfNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:
    def method(self, param1) -> None:
        """Docstring summary.

        Parameters
        ----------
        param1: int
            Pass.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PWKwargsKeyNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Passes
    **kwargs: int
        Passes
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWKwargsOutOfSectNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Docstring summary.

    **kwargs: int
        Passes

    Parameters
    ----------
    param1: int
        Fail
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FKwargsOutOfOrderNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Docstring summary.

    Parameters
    ----------
    **kwargs : int
        Passes
    param1 : int
        Fail
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _PDualColonWKwargsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(attachments, sync, **kwargs) -> None:
    """Docstring summary.

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
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _POnlyParamsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(reduce: bool = False) -> tuple[str, ...]:
    """Docstring summary.

    Parameters
    ----------
    reduce: int
        :func:`~lsfiles.utils._Tree.reduce`

    Returns
    -------
    int
        Tuple of `Path` objects or str repr.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PReturnAnyWArgsWKwargsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(*args: _t.Any, **kwargs: bool) -> _t.Any:
    """Docstring summary.

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
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PBinOpNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(index: int, seq: _t.Sequence[_T]) -> _T | None:
    """Fet index without throwing an error if index does not exist.

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
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FBinOpReprNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(index: int) -> _T | None:
    """Get index without throwing an error if index does not exist.

    Returns
    -------
    int
        Item from index else None.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PDoubleUnderscoreParamNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, __) -> None:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Passes.
    param2: int
        Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PPropertyReturnNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @property
    def function(*_, **__) -> int:
        """Docstring summary.

        Returns
        -------
        int
            Returncode.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FSIG501WRetQuestionNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function():
    """Docstring summary.

    Returns
    -------
    int
        Does it?
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FSIG404NENI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(arg, param2) -> None:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Not equal.
    para2: int
        Not equal.
    """
'''

    @property
    def expected(self) -> str:
        return E[404].fstring(T)


@_templates.register
class _PKWOnlyArgsWArgsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(
    *path: _Path,
    targets: _t.List[str] | None = None,
    disable: _t.List[str] | None = None,
) -> bool:
    """Docstring summary.

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
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FClassNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
    """

    def __init__(self, param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _PInitNoRetNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    """

    def __init__(self, param1, param2):
        pass
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PInitBadRetNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    """

    # bad typing, but leave that up to mypy
    def __init__(self, param1, param2) -> int:
        pass
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FClassRetNoneNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

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
    """

    def __init__(self, param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[504].fstring(T)


@_templates.register
class _FSIG504NI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

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
    """

    def __init__(param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[504].fstring(T)


@_templates.register
class _FProtectFuncNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def _function(param1, param2) -> None:
    """Docstring summary.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FFuncPropNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def function(self) -> int:
    """Docstring summary.

    Parameters
    ----------
    self: Klass
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _PFuncPropReturnNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def function(*_, **__) -> int:
    """Docstring summary.

    Returns
    -------
    int
        Returncode.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FFuncPropNoRetTypeNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def function(self):
    """Docstring summary.

    Parameters
    ----------
    self: Klass
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _PStaticSelfNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @staticmethod
    def method(self, param1) -> None:
        """Docstring summary.

        Parameters
        ----------
        self: Klass
            Pass.
        param1: int
            Pass.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FProtectClsWKwargsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class _Klass:
    def method(self, param1, param2, **kwargs) -> None:
        """Docstring summary.

        Parameters
        ----------
        param1: int
            Pass.
        param2: int
            Pass.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FDundersParamNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    def __dunder__(self, param1, param2) -> None:
        """Docstring summary.

        Parameters
        ----------
        param1: int
            Fails.
        param2: int
            Fails.
        param3: int
            Fails.
        """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FSIG403NI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param) -> None:
    """Docstring summary.

    Parameters
    ----------
    pram: int
        Misspelled.
    """
'''

    @property
    def expected(self) -> str:
        return E[403].fstring(T)


@_templates.register
class _PRetTypeSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :returns: Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FRetTypeDocsSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :returns: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[502].fstring(T)


@_templates.register
class _FNoRetDocsNoTypeSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :returns: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FSIG502RetTypeDocsSingleErrorSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :returns: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[502].fstring(T)


@_templates.register
class _POnlyParamsSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(reduce: bool = False) -> _t.Tuple[str, ...]:
    """Docstring summary.

    :param reduce: :func:`~lsfiles.utils._Tree.reduce`
    :returns: Tuple of `Path` objects or str repr.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PReturnAnyWArgsWKwargsSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(*args: _t.Any, **kwargs: bool) -> _t.Any:
    """Docstring summary.

    :param args: Manipulate string(s).
    :key format: Return a string instead of a tuple if strings are
        passed as tuple.
    :returns: Colored string or None.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FMsgPoorIndentSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(
        id: int, version: t.Optional[int] = None, checkauthor: bool = True
) -> Post:
    """Get post by post's ID or abort with ``404: Not Found.``

    Standard behaviour would be to return None, so do not bypass
     silently.

     :param id: The post's ID.
     :param version: If provided populate session object with
        version.
     :param checkauthor: Rule whether to check for author ID.
     :returns: Post's connection object.
    """
'''

    @property
    def expected(self) -> str:
        return E[401].fstring(T)


@_templates.register
class _PBinOpSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(index: int, seq: _t.Sequence[_T]) -> _T | None:
    """Fet index without throwing an error if index does not exist.

    :param index: Index to get.
    :param seq: Sequence object that can be indexed.
    :returns: Item from index else None.
    """
    try:
        return seq[index]
    except IndexError:
        return None
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FBinOpReprSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(index: int) -> _T | None:
    """Get index without throwing an error if index does not exist.

    :returns: Item from index else None.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PPropertyReturnSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @property
    def function(*_, **__) -> int:
        """Docstring summary.

        :returns: Returncode.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FHintMissingReturnSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function() -> Post:
    """Docstring summary.

     return: Post's connection object.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].hint or ""


@_templates.register
class _PInconsistentSpaceSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@pytest.fixture(name="main")
def fixture_main(monkeypatch) -> t.Callable[..., None]:
    """Function for passing mock ``main`` commandline arguments
    to package's main function.

    :param monkeypatch: ``pytest`` fixture for mocking attributes.
    :returns:            Function for using this fixture.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FSIG501WRetQuestionSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function():
    """Docstring summary.

    :returns: Does it?
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _PKWOnlyArgsWArgsSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(
    *path: _Path,
    targets: _t.List[str] | None = None,
    disable: _t.List[str] | None = None,
) -> bool:
    """Docstring summary.

    :param path: Path(s) to check.
    :param targets: List of errors to target.
    :param disable: List of errors to disable.
    :returns: Boolean value for whether there were any failures or not.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FClassRetNoneSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :returns: Fails
    """

    def __init__(self, param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[504].fstring(T)


@_templates.register
class _FSIG504SRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :returns: Fails
    """

    def __init__(param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[504].fstring(T)


@_templates.register
class _PFuncPropReturnSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def function(*_, **__) -> int:
    """Docstring summary.

    :returns: Returncode.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PParamG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    Args:
        param1 (int): Passes.
        param2 (int): Passes.
        param3 (int): Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FParamDocsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2) -> None:
    """Docstring summary.

    Args:
        param1 (int): Passes.
        param2 (int): Passes.
        param3 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FParamSigG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FOutOfOrderG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Docstring summary.

    Args:
        param2 (int): Fails.
        param3 (int): Fails.
        param1 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _PRetTypeG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Docstring summary.

    Args:
        param1 (int): Pass.
        param2 (int): Pass.
        param3 (int): Pass.

    Returns:
        bool: Pass.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FRetTypeDocsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.

    Returns:
        bool: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[502].fstring(T)


@_templates.register
class _FRetTypeSigG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Docstring summary.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FSIG501NoRetNoTypeG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Docstring summary.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FNoRetDocsNoTypeG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Docstring summary.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.

    Returns:
        bool: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FRetDocsAttrTypeG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1) -> t.Optional[str]:
    """Docstring summary.

    Args:
        param1 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FRetDocsNameTypeG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1) -> Optional[str]:
    """Docstring summary.

    Args:
        param1 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FSIG402OutOfOrderSingleErrorG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    Args:
        param2 (int): Fails.
        param3 (int): Fails.
        param1 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _FSIG202ParamDocsSingleErrorG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2) -> None:
    """Docstring summary.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FSIG203ParamSigSingleErrorG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FSIG502RetTypeDocsSingleErrorG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.

    Returns:
        bool: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[502].fstring(T)


@_templates.register
class _FSIG503RetTypeSigSingleErrorG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Docstring summary.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FDupesSumG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Docstring summary.

    Args:
        param1 (int): Fails.
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[201].fstring(T)


@_templates.register
class _PWArgsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, *args) -> None:
    """Docstring summary.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        *args (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWArgsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, *args) -> None:
    """Docstring summary.

    Args:
        param1 (int): Pass.
        param2 (int): Pass.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PWKwargsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, **kwargs) -> None:
    """Docstring summary.

    Args:
        param1 (int): Pass.
        param2 (int): Pass.
        **kwargs (int): Pass.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWKwargsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, **kwargs) -> None:
    """Docstring summary.

    Args:
        param1 (int): Pass.
        param2 (int): Pass.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _MFailG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function_1(param1, param2, param3) -> None:
    """Docstring summary.

    Args:
        param2 (int): Fails.
        param3 (int): Fails.
        param1 (int): Fails.
    """

def function_2(param1, param2) -> None:
    """Docstring summary.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2 in function_1
    {E[402].fstring(T)}
{PATH}:11 in function_2
    {E[202].fstring(T)}
{PATH}:20 in function_3
    {E[203].fstring(T)}
"""


@_templates.register
class _FMethodWKwargsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:
    def method(self, param1, param2, **kwargs) -> None:
        """Docstring summary.

    Args:
        param1 (int): Pass.
        param2 (int): Pass.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PClassSelfG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:
    def method(self, param1) -> None:
        """Docstring summary.

        Args:
            param1 (int): Pass.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PWKwargsKeyG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Docstring summary.

    Args:
        param1 (int): Pass.
        **kwargs (int): Pass.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWKwargsOutOfSectG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Docstring summary.

    **kwargs (int): Fails

    Args:
        param1 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FKwargsOutOfOrderG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Docstring summary.

    Args:
        **kwargs (int): Fails.
        param1 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _PDualColonWKwargsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(attachments, sync, **kwargs) -> None:
    """Docstring summary.

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
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _POnlyParamsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(reduce: bool = False) -> _t.Tuple[str, ...]:
    """Docstring summary.

    Args:
        reduce (int): :func:`~lsfiles.utils._Tree.reduce`

    Returns:
        int: Tuple of `Path` objects or str repr.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PReturnAnyWArgsWKwargsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(*args: _t.Any, **kwargs: bool) -> _t.Any:
    """Docstring summary.

    Args:
        *args (int): Manipulate string(s).
        **kwargs (int): Return a string instead of a tuple if strings
            are passed as tuple.

    Returns:
        int: Colored string or None.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PBinOpG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(index: int, seq: _t.Sequence[_T]) -> _T | None:
    """Fet index without throwing an error if index does not exist.

    Args:
        index (int): Index to get.
        seq (int): Sequence object that can be indexed.

    Returns:
        int: Item from index else None.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FBinOpReprG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(index: int) -> _T | None:
    """Get index without throwing an error if index does not exist.

    Returns:
        int: Item from index else None.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PDoubleUnderscoreParamG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, __) -> None:
    """Docstring summary.

    Args:
        param1 (int): Passes.
        param2 (int): Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PPropertyReturnG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @property
    def function(*_, **__) -> int:
        """Docstring summary.

        Returns:
            int: Returncode.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FSIG501WRetQuestionG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function():
    """Docstring summary.

    Returns:
        int: Does it?
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FSIG404NEG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(arg, param2) -> None:
    """Docstring summary.

    Args:
        param1 (int): Not equal.
        para2 (int): Not equal.
    """
'''

    @property
    def expected(self) -> str:
        return E[404].fstring(T)


@_templates.register
class _PKWOnlyArgsWArgsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(
    *path: _Path,
    targets: _t.List[str] | None = None,
    disable: _t.List[str] | None = None,
) -> bool:
    """Docstring summary.

    Args:
        path (int): Path(s) to check.
        targets (int): List of errors to target.
        disable (int): List of errors to disable.

    Returns:
        int: Boolean value for whether there were any failures or not.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FClassG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    """

    def __init__(self, param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _PInitNoRetG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
    """

    def __init__(self, param1, param2):
        pass
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PInitBadRetG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
    """

    # bad typing, but leave that up to mypy
    def __init__(self, param1, param2) -> int:
        pass
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FClassRetNoneG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.

    Returns:
        int: Fails
    """

    def __init__(self, param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[504].fstring(T)


@_templates.register
class _FSIG504G(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.

    Returns:
        int: Fails
    """

    def __init__(param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[504].fstring(T)


@_templates.register
class _FProtectFuncG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def _function(param1, param2) -> None:
    """Docstring summary.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FFuncPropG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def function(self) -> int:
    """Docstring summary.

    Args:
        self (Klass): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _PFuncPropReturnG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def function(*_, **__) -> int:
    """Docstring summary.

    Returns:
        int: Returncode.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FFuncPropNoRetTypeG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def function(self):
    """Docstring summary.

    Returns:
        int: Returncode.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _PStaticSelfG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @staticmethod
    def method(self, param1) -> None:
        """Docstring summary.

        Args:
            self (Klass): Pass.
            param1 (int): Pass.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FProtectClsWKwargsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class _Klass:
    def method(self, param1, param2, **kwargs) -> None:
        """Docstring summary.

        Args:
            param1 (int): Pass.
            param2 (int): Pass.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FDundersParamG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    def __dunder__(self, param1, param2) -> None:
        """Docstring summary.

        Args:
            param1 (int): Fail.
            param2 (int): Fail.
            param3 (int): Fail.
        """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FSIG403G(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param) -> None:
    """Docstring summary.

    Args:
        pram (int): Misspelled.
    """
'''

    @property
    def expected(self) -> str:
        return E[403].fstring(T)


@_templates.register
class _PEscapedKwargWKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(attachments, sync, **kwargs) -> None:
    """Docstring summary.

    Note: Keyword args (dict) to pass to ``attachments``:

        See ``flask_mail.Message.attach``.

        * filename:     filename of attachment
        * content_type: file mimetype
        * data:         the raw file data

    :param attachments: Iterable of kwargs to construct attachment.
    :param sync: Don't thread if True: Defaults to False.
    :param **kwargs: Keyword args to pass to ``Message``:
        See ``flask_mail.Message``.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FNoKwargsIncludedWKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Docstring summary.

    :param param1: Description of param1
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


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
        return E[102].fstring(T)


@_templates.register
class _FIssue36OffIndentN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(str_lin: str, a: str) -> bool:
    """Check if "A" or "B".

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
    """
'''

    @property
    def expected(self) -> str:
        return E[302].fstring(T)


@_templates.register
class _FOverriddenAncestorsMultipleS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
import typing as _t

T = _t.TypeVar("T")
KT = _t.TypeVar("KT")
VT = _t.TypeVar("VT")

class _MutableSequence(_t.MutableSequence[T]):
    """List-object to inherit from."""

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
    """A tuple of param types and their names."""

    kind: str = "param"
    name: str | None = None
    description: str | None = None
    indent: int = 0

class Params(_MutableSequence[Param]):
    """Represents collection of parameters."""

    def insert(self, index: int, value: Param) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _PStringAnnotation(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(some_input: int) -> "int":
    """
    Do something.

    Args:
        some_input: Random integer

    Returns:
        Unchanged input
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FNoParamS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(some_input: int) -> int:
    """Return input."""
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FMethodReturnHintS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :return: Return description.
    """

    def __init__(param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[504].hint or ""


@_templates.register
class _PIssue114PosOnlyArgsWArgsWKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(
    fun: Callable[..., Any],
    iterable: Sequence[Sequence[Any]],
    /,
    *args: Any,
    timeout: float = 0,
    show_progress: bool | None = None,
    **kwargs: Any,
) -> list[Job]:
    """Submits many jobs to the queue.

    One for each sequence in the iterable.
    Waits for all to finish, then returns the results.

    Args:
        fun: ...
        iterable: ...
        *args: Static arguments passed to the function.
        timeout: ...
        show_progress: ...
        **kwargs: Static keyword-arguments passed to the function.

    Returns:
        ...
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PIssue114PosOnlyArgsSelfWArgsWKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
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
        """Submits many jobs to the queue.

        One for each sequence in the iterable.
        Waits for all to finish, then returns the results.

        Args:
            fun: ...
            iterable: ...
            *args: Static arguments passed to the function.
            timeout: ...
            show_progress: ...
            **kwargs: Static keyword-arguments passed to the function.

        Returns:
            ...
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MPassOverloadS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@overload
def function(response: None) -> None:
    ...

@overload
def function(response: int) -> tuple[int, str]:
    ...

@overload
def function(response: bytes) -> str:
    ...

def function(response):
    """process a response.

    :param response: The response to process
    :return: Something depending on what the response is
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MFailOverloadMissingReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@overload
def function(response: None) -> None:
    ...

@overload
def function(response: int) -> tuple[int, str]:
    ...

@overload
def function(response: bytes) -> str:
    ...

def function(response):
    """process a response.

    :param response: The response to process
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:14 in function
    {E[503].fstring(T)}
"""


@_templates.register
class _MFailOverloadMissingParamS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@overload
def function(response: None) -> None:
    ...

@overload
def function(response: int) -> tuple[int, str]:
    ...

@overload
def function(response: bytes) -> str:
    ...

def function(response):
    """process a response.

    :return: something depending on what the response is
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:14 in function
    {E[203].fstring(T)}
"""


@_templates.register
class _MPassOverloadNoReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@overload
def function(response: None) -> None:
    ...

@overload
def function(response: int) -> None:
    ...

@overload
def function(response: bytes) -> None:
    ...

def function(response):
    """process a response.

    :param response: The response to process
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MPassMultiOverloadsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@overload
def function_1(response: None) -> None:
    ...

@overload
def function_1(response: int) -> tuple[int, str]:
    ...

@overload
def function_1(response: bytes) -> str:
    ...

def function_1(response):
    """process a response.

    :param response: The response to process
    :return: something depending on what the response is
    """

@overload
def function_2(response: int) -> tuple[int, str]:
    ...

@overload
def function_2(response: bool) -> None:
    ...

@overload
def function_2(response: str) -> int:
    ...

def function_2(response):
    """process another response.

    :param response: The response to process
    :return: something depending on what the response is
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MFailOverloadNoReturnDocumentedS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@overload
def function(response: None) -> None:
    ...

@overload
def function(response: int) -> None:
    ...

@overload
def function(response: bytes) -> None:
    ...

def function(response):
    """process a response.

    :param response: The response to process
    :return: NoneType
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:14 in function
    {E[502].fstring(T)}
"""


@_templates.register
class _MPassOverloadMethodS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
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
        """process a response.

        :param response: The response to process
        :return: something depending on what the response is
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MFailOverloadMethodMissingReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
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
        """process a response.

        :param response: The response to process
        """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:15 in SomeClass.process
    {E[503].fstring(T)}
"""


@_templates.register
class _MFailOverloadMethodMissingParamS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
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
        """process a response.

        :return: something depending on what the response is
        """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:15 in SomeClass.process
    {E[203].fstring(T)}
"""


@_templates.register
class _MFailOverloadMethodNoReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
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
        """process a response.

        :param response: The response to process
        """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:15 in SomeClass.process
    {E[503].fstring(T)}
"""


@_templates.register
class _MPassMultiOverloadMethodsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
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
        """process a response.

        :param response: The response to process
        :return: something depending on what the response is
        """

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
        """process another response.

        :param response: The response to process
        :return: something depending on what the response is
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MPassOverloadMethodNoReturnDocumentedS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
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
        """process a response.

        :param response: The response to process
        :return: Optional
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PParamDocsCommentModuleS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
# docsig: disable
def function(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PParamDocsCommentFuncS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2) -> None:  # docsig: disable
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MFailCommentDisableFuncS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function_1(param1, param2, param3) -> None:  # docsig: disable
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:10 in function_2
    {E[202].fstring(T)}
{PATH}:18 in function_3
    {E[203].fstring(T)}
"""


@_templates.register
class _MPassCommentDisableModuleFirstS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
# docsig: disable
def function_1(param1, param2, param3) -> None:
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MFailCommentDisableModuleSecondS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function_1(param1, param2, param3) -> None:
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

# docsig: disable
def function_2(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2 in function_1
    {E[402].fstring(T)}
"""


@_templates.register
class _MFailCommentDisableModuleThirdS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function_1(param1, param2, param3) -> None:
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

# docsig: disable
def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2 in function_1
    {E[402].fstring(T)}
{PATH}:10 in function_2
    {E[202].fstring(T)}
"""


@_templates.register
class _MFailCommentDisableModuleEnableS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function_1(param1, param2, param3) -> None:
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

# docsig: disable
def function_2(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """
# docsig: enable

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2 in function_1
    {E[402].fstring(T)}
{PATH}:20 in function_3
    {E[203].fstring(T)}
"""


@_templates.register
class _MFailCommentDisableMixedS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function_1(param1, param2, param3) -> None:
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

# docsig: disable
def function_2(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """
# docsig: enable

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """

def function_4(param1, param2, param3) -> None:  # docsig: disable
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

# docsig: disable
def function_5(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """
# docsig: enable

def function_6(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2 in function_1
    {E[402].fstring(T)}
{PATH}:20 in function_3
    {E[203].fstring(T)}
{PATH}:45 in function_6
    {E[203].fstring(T)}
"""


@_templates.register
class _PParamDocsCommentNoSpaceAfterCommentS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2) -> None:  #docsig:disable
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PParamDocsCommentNoSpaceAfterColonS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2) -> None:  # docsig:disable
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MFailCommentDisableEnableOneFuncS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
# docsig: disable
def function_1(param1, param2, param3) -> None:
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:  # docsig: enable
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:11 in function_2
    {E[202].fstring(T)}
"""


@_templates.register
class _MPassBadInlineDirective(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
# docsig: disable
def function_1(param1, param2, param3) -> None:  # docsig: ena
    """

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:  # docsig: ena
    """

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:3 in function_1
    {E[2].fstring(T).format(directive="ena")}
{PATH}:11 in function_2
    {E[2].fstring(T).format(directive="ena")}
"""


@_templates.register
class _MPassBadModuleDirective(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
# docsig: disa
def function_1(param1, param2) -> None:
    """

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_2(param1, param2, param3) -> None:
    """

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:3 in function_1
    {E[1].fstring(T).format(directive="disa")}
    {E[202].fstring(T)}
{PATH}:11 in function_2
    {E[1].fstring(T).format(directive="disa")}
    {E[402].fstring(T)}
"""


@_templates.register
class _MPylintDirective(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
# docsig: unknown
def function_1(param1, param2, param3) -> None:  # pylint: disable
    """

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

# pylint: disable=unknown,unknown-the-third
def function_2(param1, param2) -> None:
    """

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(  # docsig: enable=unknown,unknown-the-third
    param1, param2, param3
) -> None:
    """

    :param param1: Description of param1.
    :param param2: Description of param2.
    """

def function_4(param1, param2, param3) -> None:
    """

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """

def function_5(param1, param2, param3) -> int:
    """

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_6(param, param2, param3) -> None:
    """

    :param param: Description of params.
    :param param: Description of params.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_7(param, param2, param3) -> None:
    """

    :param param: Description of params.
    :param param: Description of params.
    :param param2: Description of param2.
    :param: Description of param.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:3 in function_1
    {E[1].fstring(T).format(directive="unknown")}
    {E[402].fstring(T)}
{PATH}:12 in function_2
    {E[1].fstring(T).format(directive="unknown")}
    {E[202].fstring(T)}
{PATH}:20 in function_3
    {E[1].fstring(T).format(directive="unknown")}
    {E[4].fstring(T).format(directive='enable', option="unknown")}
    {E[4].fstring(T).format(directive='enable', option="unknown-the-third")}
    {E[203].fstring(T)}
{PATH}:29 in function_4
    {E[1].fstring(T).format(directive="unknown")}
    {E[502].fstring(T)}
{PATH}:38 in function_5
    {E[1].fstring(T).format(directive="unknown")}
    {E[503].fstring(T)}
{PATH}:46 in function_6
    {E[1].fstring(T).format(directive="unknown")}
    {E[201].fstring(T)}
{PATH}:55 in function_7
    {E[1].fstring(T).format(directive="unknown")}
    {E[201].fstring(T)}
    {E[303].fstring(T)}
"""


@_templates.register
class _MInvalidDirectiveOptions(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
# docsig: unknown
def function_1(param1, param2, param3) -> None:  # pylint: disable
    """Description summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

# pylint: disable=unknown,unknown-the-third
def function_2(param1, param2) -> None:
    """

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(  # docsig: enable=unknown,unknown-the-third
    param1, param2, param3
) -> None:
    """

    :param param1: Description of param1.
    :param param2: Description of param2.
    """

def function_4(param1, param2, param3) -> None:
    """

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """

def function_5(param1, param2, param3) -> int:
    """

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_6(param, param2, param3) -> None:
    """

    :param param: Description of params.
    :param param: Description of params.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_7(param, param2, param3) -> None:
    """

    :param param: Description of params.
    :param param: Description of params.
    :param param2: Description of param2.
    :param: Description of param.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:3 in function_1
    {E[1].fstring(T).format(directive="unknown")}
    {E[402].fstring(T)}
{PATH}:12 in function_2
    {E[1].fstring(T).format(directive="unknown")}
    {E[202].fstring(T)}
{PATH}:20 in function_3
    {E[1].fstring(T).format(directive="unknown")}
    {E[4].fstring(T).format(directive='enable', option="unknown")}
    {E[4].fstring(T).format(directive='enable', option="unknown-the-third")}
    {E[203].fstring(T)}
{PATH}:29 in function_4
    {E[1].fstring(T).format(directive="unknown")}
    {E[502].fstring(T)}
{PATH}:38 in function_5
    {E[1].fstring(T).format(directive="unknown")}
    {E[503].fstring(T)}
{PATH}:46 in function_6
    {E[1].fstring(T).format(directive="unknown")}
    {E[201].fstring(T)}
{PATH}:55 in function_7
    {E[1].fstring(T).format(directive="unknown")}
    {E[201].fstring(T)}
    {E[303].fstring(T)}
"""


@_templates.register
class _MInvalidSingleDirectiveOptions(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(  # docsig: enable=unknown
    param1, param2, param3
) -> None:
    """

    :param param1: Description of param1.
    :param param2: Description of param2.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2 in function
    {E[4].fstring(T).format(directive='enable', option="unknown")}
    {E[203].fstring(T)}
"""


@_templates.register
class _FWClassConstructorFS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary."""

    def __init__(self, param1, param2) -> None:
        """Docstring summary.

        :param param1: Description of param1.
        :param param2: Description of param2.
        :param param3: Description of param3.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FWClassConstructorInitNoRetS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary."""

    def __init__(self, param1, param2):
        """Docstring summary.

        :param param1: Description of param1.
        :param param2: Description of param2.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FWClassConstructorInitBadRetS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary."""

    # bad typing, but leave that up to mypy
    def __init__(self, param1, param2) -> int:
        """Docstring summary.

        :param param1: Description of param1.
        :param param2: Description of param2.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FWClassConstructorRetNoneFS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary."""

    def __init__(self, param1, param2) -> None:
        """Docstring summary.

        :param param1: Description of param1.
        :param param2: Description of param2.
        :return: Return description.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FWClassConstructorSIG504FS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """Docstring summary."""

    def __init__(param1, param2) -> None:
        """Docstring summary.

        :param param1: Description of param1.
        :param param2: Description of param2.
        :return: Return description.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _MInvalidSingleModuleDirectiveOptions(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
# docsig: enable=unknown
def function(param1, param2, param3) -> None:
    """

    :param param1: Description of param1.
    :param param2: Description of param2.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:3 in function
    {E[3].fstring(T).format(directive='enable', option="unknown")}
    {E[203].fstring(T)}
"""


@_templates.register
class _MFailProtectedMethods(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class _Messages(_t.Dict[int, Message]):
    def __init__(self) -> None:
        self._this_should_not_need_a_docstring

    def fromcode(self, ref: str) -> Message:
        """

        :param ref: Codes or symbolic reference.
        """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:3 in _Messages.__init__
    {E[102].fstring(T)}
{PATH}:6 in _Messages.fromcode
    {E[503].fstring(T)}
"""


@_templates.register
class _MFDisableClassInlineCommentS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class _MessageSequence(_t.List[str]):  # docsig: disable
    def __init__(
        self,
        targets: list[_Message],
        disable: list[_Message],
    ) -> None:
        pass

    def add(self, value: _Message, hint: bool = False, **kwargs) -> None:
        """Add an error to the container.

        :param value: Value to add.
        :param hint: Whether to print a hint or not.
        :param kwargs: Variable(s) if format string.
        """

class Report(_MessageSequence):
    def order(self, sig: _Param, doc: _Param) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:19 in Report.order
    {E[101].fstring(T)}
"""


@_templates.register
class _MFDisableClassModuleCommentDisableEnableS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
# docsig: disable
class _MessageSequence(_t.List[str]):
    def __init__(
        self,
        targets: list[_Message],
        disable: list[_Message],
    ) -> None:
        pass

    def add(self, value: _Message, hint: bool = False, **kwargs) -> None:
        """Add an error to the container.

        :param value: Value to add.
        :param hint: Whether to print a hint or not.
        :param kwargs: Variable(s) if format string.
        """

# docsig: enable

class Report(_MessageSequence):
    def order(self, sig: _Param, doc: _Param) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:22 in Report.order
    {E[101].fstring(T)}
"""


@_templates.register
class _MFDisableClassModuleCommentDisableS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
# docsig: disable
class _MessageSequence(_t.List[str]):
    def __init__(
        self,
        targets: list[_Message],
        disable: list[_Message],
    ) -> None:
        pass

    def add(self, value: _Message, hint: bool = False, **kwargs) -> None:
        """Add an error to the container.

        :param value: Value to add.
        :param hint: Whether to print a hint or not.
        :param kwargs: Variable(s) if format string.
        """

class Report(_MessageSequence):
    def order(self, sig: _Param, doc: _Param) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FFuncInIfStatementN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(argument: int = 42) -> int:
    """
    Function that prints a message and returns the argument + 1

    Parameters
    ----------
    argument : int, optional
        The input argument, by default 42

    Returns
    -------
    int
        The input argument + 1
    """

if True:
    my_function(42)
    def nested_function(argument: int = 42) -> int:
        pass
'''

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _FKlassInIfStatementN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
if True:
    class Klass:
        """Class is OK."""
        def my_external_function(self, argument: int = 42) -> int:
            pass
'''

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _FFuncInIfInIfStatementN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
if True:
    if True:
        def function(argument: int = 42) -> int:
            pass
"""

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _FKlassNotMethodOkN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    def __init__(self, this) -> None:
        self.this = this
    def my_external_function(self, argument: int = 42) -> int:
        """This is a method.

        :param argument: An int.
        :return: An int.
        """
'''

    @property
    def expected(self) -> str:
        return E[102].fstring(T)


@_templates.register
class _FFuncInForLoopN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
container = []

for argument in container:
    def function(argument: int = 42) -> int:
        pass
"""

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _FFuncInForLoopIfN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
for argument in container:
    if argument > 0:
        def function(argument: int = 42) -> int:
            pass
"""

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _FNestedFuncN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(argument: int = 42) -> int:
    """
    Function that prints a message and returns the argument + 1

    Parameters
    ----------
    argument : int, optional
        The input argument, by default 42

    Returns
    -------
    int
        The input argument + 1
    """
    def nested_function(argument: int = 42) -> int:
        pass
'''

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


# starts with `M` for multi instead of `F` so we don't run
# `test_single_flag` with this as it needs `-N/--check-nested` and
# `-c/--check-class` to fail
@_templates.register
class _MNestedKlassNotMethodOkN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(argument: int = 42) -> int:
    """
    Function that prints a message and returns the argument + 1

    Parameters
    ----------
    argument : int, optional
        The input argument, by default 42

    Returns
    -------
    int
        The input argument + 1
    """
    class Klass:
        def __init__(self, this) -> None:
            pass
        def my_external_function(self, argument: int = 42) -> int:
            """This is a method.

            :param argument: An int.
            :return: An int.
            """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:17 in Klass.__init__
    {E[102].fstring(T)}
"""


@_templates.register
class _MNestedKlassNotMethodNotN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(argument: int = 42) -> int:
    """
    Function that prints a message and returns the argument + 1

    Parameters
    ----------
    argument : int, optional
        The input argument, by default 42

    Returns
    -------
    int
        The input argument + 1
    """
    class Klass:
        def __init__(self, this) -> None:
            pass
        def my_external_function(self, argument: int = 42) -> int:
            pass
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:17 in Klass.__init__
    {E[102].fstring(T)}
{PATH}:19 in Klass.my_external_function
    {E[101].fstring(T)}
"""


@_templates.register
class _MPassOverloadNoReturnAliasS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
from typing import overload as _overload

@_overload
def function(response: None) -> None:
    ...

@_overload
def function(response: int) -> None:
    ...

@_overload
def function(response: bytes) -> None:
    ...

@_overload
def function(response):
    """process a response.

    :param response: The response to process
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PPropertyReturnFunctoolsCachedAliasN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
from functools import cached_property as _cached_property

class Klass:
    @_cached_property
    def function(*_, **__) -> int:
        """Docstring summary.

        Returns
        -------
            int
                Returncode.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FIncorrectDocDotS(_BaseTemplate):
    @property
    def template(self) -> str:
        return r'''
def function(
    define: tuple[tuple[str, str], ...],
    data: list[_t.Any],
    sort_by_field: int | None = None,
    summary_line: _t.Iterable[_t.Any] | None = None,
    print_field_total: int | None = None,
) -> None:
    """Display data as a table.

    :param define: Define the headers and the format of the fields
        belonging to the headers.
    :param data: Data to display.
    :param sort_by_field. Sort the table by the index of the field to
        sort by.
    :param summary_line: Add a row to the end of the table that will not
        be sorted if `sort_by_field` is provided.
    :param print_field_total: Print the total number in the same format
        of the index of the field provided.
    """
'''

    @property
    def expected(self) -> str:
        return E[304].fstring(T).format(token=".")


@_templates.register
class _FPropertyReturnMissingDescS(_BaseTemplate):
    @property
    def template(self) -> str:
        return r'''
def function(ticker: str) -> str:
    """Normalize ticket names.

    :param ticker: Ticker to normalize.
    :return:
    """
'''

    @property
    def expected(self) -> str:
        return E[506].fstring(T)
