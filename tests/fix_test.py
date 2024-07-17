"""
tests.exclude_test
==================
"""

import pickle
from pathlib import Path

import pytest

from . import InitFileFixtureType, MockMainType


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
