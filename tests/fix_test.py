"""
tests.exclude_test
==================
"""

import pytest

from . import MockMainType, long


def test_fix_optional_return_statements_with_overload_func_sig502(
    main: MockMainType,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test ignore typechecker.

    :param main: Mock ``main`` function.
    :param capsys: Capture sys out.
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
    main(long.string, template)
    std = capsys.readouterr()
    assert "SIG502" not in std.out
