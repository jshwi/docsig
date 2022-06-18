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
class _PassParam(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
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
class _FailParamDocs(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2) -> None:
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
def function({CHECK}param1, {CHECK}param2, {CROSS}None):
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
    :return: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CROSS}param3):
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
    :return: Passes.
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
def function({CROSS}param1, {CROSS}param2, {CROSS}param3):
    \"\"\"...

    :param param2: {CROSS}
    :param param3: {CROSS}
    :param param1: {CROSS}
    \"\"\"
"""
