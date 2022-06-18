"""
tests
=====

Test package for ``docsig``.
"""
import typing as t
from pathlib import Path

from templatest import BaseTemplate as _BaseTemplate
from templatest import templates as _templates

MockMainType = t.Callable[..., int]
InitFileFixtureType = t.Callable[[str], Path]

CHECK = "\u2713"
CROSS = "\u2716"


@_templates.register
class _FunctionPass(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function_1(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    :param param1: Passes.
    :param param2: Passes.
    :param param3: Passes.
    :return: Passes.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FunctionFailTooManyInDocs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function_2(param1, param2) -> None:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :return: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function_2({CHECK}param1, {CHECK}param2, {CROSS}None):
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"
"""


@_templates.register
class _FunctionFailTooManyInSig(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function_3(param1, param2, param3) -> None:
    \"\"\"Not proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    :return: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function_3({CHECK}param1, {CHECK}param2, {CROSS}param3):
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _FunctionNoDocstring(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function_4(param1, param2, param3) -> None:
    pass
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FunctionNoParams(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function_5() -> None:
    \"\"\"No params.\"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FunctionUnderscoreParam(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function_1(param1, param2, _) -> None:
    \"\"\"Proper docstring.

    :param param1: Passes.
    :param param2: Passes.
    :return: Passes.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""
