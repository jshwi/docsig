"""
tests._test
===========
"""

# pylint: disable=protected-access

from __future__ import annotations

from pathlib import Path

import pytest

import docsig

from . import InitFileFixtureType, MockMainType

# noinspection PyProtectedMember


def test_config_resolution(
    monkeypatch: pytest.MonkeyPatch,
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Some additional flake8 and regular run tests.

    :param monkeypatch: Mock patch environment and attributes.
    :param main: Mock ``main`` function.
    :param init_file: Initialize a test file.
    """
    template = '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    :param param1: Passes.
    :param param2: Passes.
    :param param3: Passes.
    """
'''
    init_file(template)
    pyproject_toml = Path.cwd() / "pyproject.toml"
    tox_ini = Path.cwd() / "tox.ini"
    pyproject_toml.write_text(
        """\
[tool.docsig]
check-class = true
check-dunders = false
""",
        encoding="utf-8",
    )
    kwargs_dict = {}

    def _runner(*_, **kwargs):
        kwargs_dict.update(kwargs)
        # noinspection PyUnresolvedReferences
        return docsig._report.Failures(), 0

    monkeypatch.setattr("docsig._core.runner", _runner)
    monkeypatch.setattr("docsig.plugin.runner", _runner)
    main(".")
    assert kwargs_dict["check_class"] is True
    assert kwargs_dict["check_dunders"] is False
    tox_ini.write_text(
        """\
[flake8]
sig-check-class = true
sig-check-dunders = true
"""
    )
    main(".")
    assert kwargs_dict["check_class"] is True
    assert kwargs_dict["check_dunders"] is True
