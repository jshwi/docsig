"""
tests._test
===========
"""

from __future__ import annotations

import typing as t
from random import random

import pytest

import docsig

# noinspection PyProtectedMember
from docsig._config import _ArgumentParser, _split_comma

from . import FixtureInitPyprojectTomlFile, FixturePatchArgv


@pytest.mark.parametrize(
    "config,args,expected",
    [
        (
            {
                "list": [],
            },
            [
                "name",
                "--list",
                "string_1,string_2,string_3",
            ],
            [
                "string_1",
                "string_2",
                "string_3",
            ],
        ),
        (
            {
                "list": [
                    "string_4",
                ],
            },
            [
                "name",
                "--list",
                "string_1,string_2,string_3",
            ],
            [
                "string_4",
                "string_1",
                "string_2",
                "string_3",
            ],
        ),
    ],
    ids=["empty-conf", "with-conf"],
)
def test_list_parser(
    init_pyproject_toml: FixtureInitPyprojectTomlFile,
    patch_argv: FixturePatchArgv,
    config: dict[str, t.Any],
    args: tuple[str, ...],
    expected: list[str],
) -> None:
    """Test ``arcon.ArgumentParser.add_list_args``.

    :param init_pyproject_toml: Initialize a test pyproject.toml file.
    :param patch_argv: Patch commandline arguments.
    :param config: Object to write to pyproject.toml.
    :param args: Arguments to pass to the commandline.
    :param expected: Expected result.
    """
    init_pyproject_toml(config)
    patch_argv(*args)
    parser = _ArgumentParser()
    parser.add_argument(
        "-l",
        "--list",
        action="store",
        type=_split_comma,
        default=[],
    )
    namespace = parser.parse_args()
    assert namespace.list.sort() == expected.sort()


def test_no_toml(patch_argv: FixturePatchArgv) -> None:
    """Test ``arcon.ArgumentParser`` with no config.

    :param patch_argv: Patch commandline arguments.
    """
    patch_argv("name", "--arg")
    parser = _ArgumentParser()
    parser.add_argument("-a", "--arg", action="store_true")
    namespace = parser.parse_args()
    assert namespace.arg


def test_regular_flags(
    init_pyproject_toml: FixtureInitPyprojectTomlFile,
    patch_argv: FixturePatchArgv,
) -> None:
    """Test ``arcon.ArgumentParser`` uses proper slug.

    :param init_pyproject_toml: Initialize a test pyproject.toml file.
    :param patch_argv: Patch commandline arguments.
    """
    config = {"this-flag": True}
    init_pyproject_toml(config)
    patch_argv(docsig.__name__)
    parser = _ArgumentParser()
    parser.add_argument("-t", "--this-flag", action="store_true")
    namespace = parser.parse_args()
    assert namespace.this_flag is True


def test_list_default(
    init_pyproject_toml: FixtureInitPyprojectTomlFile,
    patch_argv: FixturePatchArgv,
) -> None:
    """Test ``arcon.ArgumentParser.add_list_argument`` defaults.

    :param init_pyproject_toml: Initialize a test pyproject.toml file.
    :param patch_argv: Patch commandline arguments.
    """
    patch_argv("name")

    # no defaults, pyproject.toml, or kwarg, but the type is list, so
    # that is its falsy value
    parser = _ArgumentParser()
    parser.add_argument(
        "-l",
        "--list",
        action="store",
        type=_split_comma,
        default=[],
    )
    namespace = parser.parse_args()
    assert namespace.list == []

    # if the default kwarg is provided, it is the default if there is
    # nothing in pyproject.toml
    parser = _ArgumentParser()
    parser.add_argument(
        "-l",
        "--list",
        action="store",
        type=_split_comma,
        default=[1, 2, 3],
    )
    namespace = parser.parse_args()
    assert namespace.list == [1, 2, 3]

    # if the default kwarg is provided, it is added to by the
    # pyproject.toml, as this is a configured value, and a default if
    # nothing included in commandline
    config = {"tool": {"name": {"list": [100, 200, 300]}}}
    init_pyproject_toml(config)
    parser = _ArgumentParser()
    parser.add_argument(
        "-l",
        "--list",
        action="store",
        type=_split_comma,
        default=[1, 2, 3],
    )
    namespace = parser.parse_args()
    assert namespace.list.sort() == [100, 200, 300, 1, 2, 3].sort()


def test_store_value_is_none(
    init_pyproject_toml: FixtureInitPyprojectTomlFile,
    patch_argv: FixturePatchArgv,
) -> None:
    """Test that pyproject config is not overwritten with a None.

    :param init_pyproject_toml: Initialize a test pyproject.toml file.
    :param patch_argv: Patch commandline arguments.
    """
    expected = "this-is-a-value"
    config = {"this-flag": expected}
    init_pyproject_toml(config)
    patch_argv(docsig.__name__)
    parser = _ArgumentParser()
    parser.add_argument("-t", "--this-flag", action="store")
    namespace = parser.parse_args()
    assert namespace.this_flag == expected


def test_no_file_to_root(
    monkeypatch: pytest.MonkeyPatch,
    patch_argv: FixturePatchArgv,
) -> None:
    """Test ``arcon._ArgumentParser`` with no config.

    :param monkeypatch: Mock patch environment and attributes.
    :param patch_argv: Patch commandline arguments.
    """
    monkeypatch.setattr("docsig._config.PYPROJECT_TOML", str(random()))
    patch_argv("name", "--arg")
    parser = _ArgumentParser()
    parser.add_argument("-a", "--arg", action="store_true")
    namespace = parser.parse_args()
    assert namespace.arg
