"""
tests.exclude_test
==================
"""

# pylint: disable=protected-access

import pickle
from pathlib import Path

import pytest

import docsig

from . import FixtureMakeTree, InitFileFixtureType, MockMainType


def test_fix_optional_return_statements_with_overload_func_sig502(
    main: MockMainType,
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
) -> None:
    """Test ignore typechecker.

    :param main: Mock ``main`` function.
    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    """
    template = '''
from typing import Optional, overload


@overload
def get_something(number: int) -> str:
    """For getting a string from an integer."""


@overload
def get_something(number: None) -> None:
    """For getting a string from an integer."""


def get_something(number: Optional[int]) -> Optional[str]:
    """
    For getting a string from an integer.

    Parameters
    ----------
    number : int
        The number to convert to a string.

    Returns
    -------
    str
        The string representation of the number.
    """
    if number is None:
        return None
    return str(number)
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert "SIG502" not in std.out


def test_no_fail_on_unicode_decode_error_384(
    main: MockMainType, tmp_path: Path
) -> None:
    """Ensure unicode decode error is handled without error.

    :param main: Patch package entry point.
    :param tmp_path: Create and return temporary directory.
    """
    pkl = tmp_path / "test.pkl"
    serialize = [1, 2, 3]
    with open(pkl, "wb") as fout:
        pickle.dump(serialize, fout)

    assert main(pkl, test_flake8=False) == 0


def test_exclude_dirs_392(
    monkeypatch: pytest.MonkeyPatch,
    main: MockMainType,
    make_tree: FixtureMakeTree,
) -> None:
    """Test dir regexes are correctly excluded.

    :param monkeypatch: Mock patch environment and attributes.
    :param main: Patch package entry point.
    :param make_tree: Create directory tree from dict mapping.
    """
    pyproject_toml = Path.cwd() / "pyproject.toml"
    pyproject_toml.write_text(
        r"""
[tool.docsig]
exclude = '''.*src[\\/]design[\\/].*'''
""",
        encoding="utf-8",
    )
    path_obj = docsig._core._Paths  # define to avoid recursion
    paths_list = []

    def _paths(*args, **kwargs) -> docsig._core._Paths:
        paths = path_obj(*args, **kwargs)
        paths_list.append(paths)
        return paths

    monkeypatch.setattr("docsig._core._Paths", _paths)
    make_tree(
        Path.cwd(),
        {
            "src": {"design": {"file1.py": []}},
            "ssrc": {"design": {"file2.py": []}},
            "parent": {"src": {"design": {"file3.py": []}}},
        },
    )
    main(".", test_flake8=False)
    assert not any(
        i in paths_list[0]
        for i in [
            Path("src") / "design" / "file1.py",
            Path("ssrc") / "design" / "file2.py",
            Path("parent") / "src" / "design" / "file3.py",
        ]
    )
