"""
tests.disable_test.py
=====================
"""
# pylint: disable=too-many-lines
import pytest
from templatest.utils import VarSeq

from . import InitFileFixtureType, MockMainType

function = VarSeq("function", "_")

RULE = "rule"
ES = "E101", "E102", "E103", "E104", "E105", "E106", "E107"
DISABLE_FILE_1 = """
def function_1(param1, param2, param3) -> None:
    \"\"\"E101.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    \"\"\"


def function_2(param1, param2) -> None:
    \"\"\"E102.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"


def function_3(param1, param2, param3) -> None:
    \"\"\"E103.

    :param param1: Fails.
    :param param2: Fails.
    \"\"\"


def function_4(param1, param2, param3) -> None:
    \"\"\"E104.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :return: Fails.
    \"\"\"


def function_5(param1, param2, param3) -> int:
    \"\"\"E105.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"


def function_6(param1, param2, param3) -> None:
    \"\"\"E106.

    :param param1: Fails.
    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"


def function_7(param1, param2, param3) -> None:
    \"\"\"E107.

    :param param1: Fails.
    :param param1: Fails.
    :param param2: Fails.
    :param: Fails.
    \"\"\"
"""
DISABLE_FILE_2 = """
# docsig: disable
def function_1(param1, param2, param3) -> None:
    \"\"\"E101.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    \"\"\"


def function_2(param1, param2) -> None:
    \"\"\"E102.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"


def function_3(param1, param2, param3) -> None:
    \"\"\"E103.

    :param param1: Fails.
    :param param2: Fails.
    \"\"\"


def function_4(param1, param2, param3) -> None:
    \"\"\"E104.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :return: Fails.
    \"\"\"


def function_5(param1, param2, param3) -> int:
    \"\"\"E105.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"


def function_6(param1, param2, param3) -> None:
    \"\"\"E106.

    :param param1: Fails.
    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"


def function_7(param1, param2, param3) -> None:
    \"\"\"E107.

    :param param1: Fails.
    :param param1: Fails.
    :param param2: Fails.
    :param: Fails.
    \"\"\"
"""
DISABLE_FILE_3 = """
def function_1(param1, param2, param3) -> None:  # docsig: disable
    \"\"\"E101.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    \"\"\"


def function_2(param1, param2) -> None:
    \"\"\"E102.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"


def function_3(param1, param2, param3) -> None:
    \"\"\"E103.

    :param param1: Fails.
    :param param2: Fails.
    \"\"\"


def function_4(param1, param2, param3) -> None:
    \"\"\"E104.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :return: Fails.
    \"\"\"


def function_5(param1, param2, param3) -> int:
    \"\"\"E105.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"


def function_6(param1, param2, param3) -> None:
    \"\"\"E106.

    :param param1: Fails.
    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"


def function_7(param1, param2, param3) -> None:
    \"\"\"E107.

    :param param1: Fails.
    :param param1: Fails.
    :param param2: Fails.
    :param: Fails.
    \"\"\"
"""
ENABLE_FILE_1 = """
# docsig: disable
# docsig: enable
def function_1(param1, param2, param3) -> None:
    \"\"\"E101.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    \"\"\"


def function_2(param1, param2) -> None:
    \"\"\"E102.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"


def function_3(param1, param2, param3) -> None:
    \"\"\"E103.

    :param param1: Fails.
    :param param2: Fails.
    \"\"\"


def function_4(param1, param2, param3) -> None:
    \"\"\"E104.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :return: Fails.
    \"\"\"


def function_5(param1, param2, param3) -> int:
    \"\"\"E105.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"


def function_6(param1, param2, param3) -> None:
    \"\"\"E106.

    :param param1: Fails.
    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"


def function_7(param1, param2, param3) -> None:
    \"\"\"E107.

    :param param1: Fails.
    :param param1: Fails.
    :param param2: Fails.
    :param: Fails.
    \"\"\"

"""


def test_no_disables(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
) -> None:
    """Test series of functions with no disable comments.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(DISABLE_FILE_1)
    main(".")
    std = capsys.readouterr()
    assert all(i in std.out for i in ES)


@pytest.mark.parametrize(RULE, ES)
def test_commandline_disables(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
    rule: str,
) -> None:
    """Test series of functions with disable commandline arg.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param rule: Rule to disable.
    """
    init_file(DISABLE_FILE_1)
    main(".", "--disable", rule)
    std = capsys.readouterr()
    assert rule not in std.out
    assert all(i in std.out for i in ES if i != rule)


def test_module_disables(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
) -> None:
    """Test disabling entire module with disable comment.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(DISABLE_FILE_2)
    main(".")
    std = capsys.readouterr()
    assert not any(i in std.out for i in ES)


def test_single_function_disable(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
) -> None:
    """Test disabling single function with disable comment.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(DISABLE_FILE_3)
    main(".")
    std = capsys.readouterr()
    assert function[1] not in std.out
    assert all(f"function_{i}" in std.out for i in range(2, 8))


def test_module_enables(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
) -> None:
    """Test individual  checks.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(ENABLE_FILE_1)
    main(".")
    std = capsys.readouterr()
    assert all(i in std.out for i in ES)
