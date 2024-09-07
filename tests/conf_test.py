"""
tests._test
===========
"""

from __future__ import annotations

import typing as t
from pathlib import Path
from random import random

import pytest
import tomli_w

# noinspection PyProtectedMember
from docsig._config import _ArgumentParser

from . import LIST, NAME, TOML, TOOL, FixturePatchArgv, long, short, string


@pytest.mark.parametrize(
    "config,args,expected",
    [
        (
            {TOOL: {NAME: {LIST: []}}},
            [NAME, long.list, f"{string[1]},{string[2]},{string[3]}"],
            [string[1], string[2], string[3]],
        ),
        (
            {TOOL: {NAME: {LIST: [string[4]]}}},
            [NAME, long.list, f"{string[1]},{string[2]},{string[3]}"],
            [string[4], string[1], string[2], string[3]],
        ),
    ],
    ids=["empty-conf", "with-conf"],
)
def test_list_parser(
    patch_argv: FixturePatchArgv,
    config: dict[str, t.Any],
    args: tuple[str, ...],
    expected: list[str],
) -> None:
    """Test ``arcon.ArgumentParser.add_list_args``.

    :param patch_argv: Patch commandline arguments.
    :param config: Object to write to pyproject.toml.
    :param args: Arguments to pass to commandline.
    :param expected: Expected result.
    """
    Path(TOML).write_text(tomli_w.dumps(config), encoding="utf-8")
    patch_argv(*args)
    parser = _ArgumentParser()
    parser.add_list_argument(short.list, long.list)
    namespace = parser.parse_args()
    assert namespace.list.sort() == expected.sort()


def test_no_toml(patch_argv: FixturePatchArgv) -> None:
    """Test ``arcon.ArgumentParser`` with no config.

    :param patch_argv: Patch commandline arguments.
    """
    patch_argv(NAME, long.arg)
    parser = _ArgumentParser()
    parser.add_argument(short.arg, long.arg, action="store_true")
    namespace = parser.parse_args()
    assert namespace.arg


def test_regular_flags(patch_argv: FixturePatchArgv) -> None:
    """Test ``arcon.ArgumentParser`` uses proper slug.

    :param patch_argv: Patch commandline arguments.
    """
    config = {TOOL: {NAME: {"this-flag": True}}}
    Path(TOML).write_text(tomli_w.dumps(config), encoding="utf-8")
    patch_argv(NAME)
    parser = _ArgumentParser()
    parser.add_argument(short.this_flag, long.this_flag, action="store_true")
    namespace = parser.parse_args()
    assert namespace.this_flag is True


def test_list_default(patch_argv: FixturePatchArgv) -> None:
    """Test ``arcon.ArgumentParser.add_list_argument`` defaults.

    :param patch_argv: Patch commandline arguments.
    """
    patch_argv(NAME)

    # no defaults, pyproject.toml, or kwarg, but the type is list, so
    # that is its falsy value
    parser = _ArgumentParser()
    parser.add_list_argument(short.list, long.list)
    namespace = parser.parse_args()
    assert namespace.list == []

    # if the default kwarg is provided, it is the default if there is
    # nothing in pyproject.toml
    parser = _ArgumentParser()
    parser.add_list_argument(short.list, long.list, default=[1, 2, 3])
    namespace = parser.parse_args()
    assert namespace.list == [1, 2, 3]

    # if the default kwarg is provided it is added to by the
    # pyproject.toml, as this is a configured value, and a default if
    # nothing included in commandline
    config = {TOOL: {NAME: {"list": [100, 200, 300]}}}
    Path(TOML).write_text(tomli_w.dumps(config), encoding="utf-8")
    parser = _ArgumentParser()
    parser.add_list_argument(short.list, long.list, default=[1, 2, 3])
    namespace = parser.parse_args()
    assert namespace.list.sort() == [100, 200, 300, 1, 2, 3].sort()


def test_store_value_is_none(patch_argv: FixturePatchArgv) -> None:
    """Test that pyproject config is not overwritten with a None.

    :param patch_argv: Patch commandline arguments.
    """
    expected = "this-is-a-value"
    config = {TOOL: {NAME: {long.this_flag[2:]: expected}}}
    Path(TOML).write_text(tomli_w.dumps(config), encoding="utf-8")
    patch_argv(NAME)
    parser = _ArgumentParser()
    parser.add_argument(short.this_flag, long.this_flag, action="store")
    namespace = parser.parse_args()
    assert namespace.this_flag == expected


@pytest.mark.parametrize(
    "pyproject,custom,commandline,expected",
    [
        ({}, {}, [], None),
        ({long.a_str[2:]: "a"}, {}, [], "a"),
        ({long.a_str[2:]: "a"}, {long.a_str[2:]: "b"}, [], "b"),
        ({long.a_str[2:]: "a"}, {long.a_str[2:]: "b"}, [long.a_str, "c"], "c"),
    ],
    ids=["none", "pyproject", "custom", "commandline"],
)
def test_own_config(
    patch_argv: FixturePatchArgv,
    pyproject: dict[str, str],
    custom: dict[str, str],
    commandline: list[str],
    expected: str,
) -> None:
    """Test ``arcon.ArgumentParser`` using config object.

    :param patch_argv: Patch commandline arguments.
    :param pyproject: Object to write to pyproject.toml.
    :param custom: Config to pass to ``ArgumentParser``.
    :param commandline: Arguments to pass to commandline.
    :param expected: Expected result.
    """
    patch_argv(NAME, *commandline)
    Path(TOML).write_text(
        tomli_w.dumps({TOOL: {NAME: pyproject}}), encoding="utf-8"
    )
    parser = _ArgumentParser(config=custom)
    parser.add_argument(short.a_str, long.a_str, action="store")
    namespace = parser.parse_args()
    assert namespace.a_str == expected


def test_no_file_to_root(
    monkeypatch: pytest.MonkeyPatch, patch_argv: FixturePatchArgv
) -> None:
    """Test ``arcon._ArgumentParser`` with no config.

    :param monkeypatch: Mock patch environment and attributes.
    :param patch_argv: Patch commandline arguments.
    """
    monkeypatch.setattr("docsig._config.PYPROJECT_TOML", str(random()))
    patch_argv(NAME, long.arg)
    parser = _ArgumentParser()
    parser.add_argument(short.arg, long.arg, action="store_true")
    namespace = parser.parse_args()
    assert namespace.arg
