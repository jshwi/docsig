"""
tests.misc_test
===============
"""
# pylint: disable=protected-access
from __future__ import annotations

import pytest
from templatest import templates

import docsig
from docsig.messages import TEMPLATE as T
from docsig.messages import E

from . import (
    CHECK,
    CROSS,
    PATH,
    InitFileFixtureType,
    MockMainType,
    long,
    short,
)


@pytest.mark.parametrize("arg", (short.v, long.version))
def test_print_version(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    arg: str,
) -> None:
    """Test printing of version on commandline.

    :param monkeypatch: Mock patch environment and attributes.
    :param capsys: Capture sys out.
    :param main: Patch package entry point.
    :param arg: Version argument.
    """
    monkeypatch.setattr("docsig._config.__version__", "1.0.0")
    with pytest.raises(SystemExit):
        main(arg)

    std = capsys.readouterr()
    assert std.out.strip() == "1.0.0"


def test_class_and_class_constructor(
    capsys: pytest.CaptureFixture, main: MockMainType
) -> None:
    """Test that docsig command lines errors when passed incompatible
    options.

    :param capsys: Capture sys out.
    :param main: Patch package entry point.
    """
    with pytest.raises(SystemExit):
        main(".", "--check-class", "--check-class-constructor")

    std = capsys.readouterr()
    assert "not allowed with argument" in std.err.strip()


def test_class_and_class_constructor_in_interpreter() -> None:
    """Test that docsig errors when passed incompatible options."""
    assert docsig.docsig(
        string="def func(): pass",
        check_class=True,
        check_class_constructor=True,
    ) == (
        "argument to check class constructor not allowed with argument to"
        " check class"
    )


@pytest.mark.parametrize("error", ["E101", "E102", "E106", "E107"])
def test_target_report(
    main: MockMainType,
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    error: str,
) -> None:
    """Test report only adds the target error provided.

    The test should fail as it matches with the selected target.

    Assert that the error appears in the report to confirm it has
    triggered.

    :param main: Mock ``main`` function.
    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param error: Error to target.
    """
    template = """
def function_3(param1, param2, param3) -> None:
    '''E101,E102,E106,E107.

    :param param1: Fails.
    :param param1: Fails.
    :param param2: Fails.
    :param: Fails.
    '''
"""
    _errors = "E101", "E102", "E106", "E107"
    init_file(template)
    main(".", "--target", error)
    std = capsys.readouterr()
    assert error in std.out
    assert not any(e in std.out for e in _errors if e != error)


def test_invalid_target(main: MockMainType) -> None:
    """Test invalid target provided.

    :param main: Mock ``main`` function.
    """
    assert (
        main(".", long.target, "unknown")
        == "unknown option to target 'unknown'"
    )


def test_lineno(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
) -> None:
    """Test printing of three function errors with line number.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(
        templates.registered.getbyname("m-fail-s").template  # type: ignore
    )
    main(".")
    std = capsys.readouterr()
    assert f"{PATH}:2" in std.out
    assert f"{PATH}:11" in std.out
    assert f"{PATH}:19" in std.out


def test_param_ne() -> None:
    """Get coverage on `Param.__eq__`."""
    # noinspection PyUnresolvedReferences
    assert docsig._function.Param() != object


def test_file_not_found_error(main: MockMainType) -> None:
    """Test file not found error for incorrect path arg.

    :param main: Mock ``main`` function.
    """
    with pytest.raises(FileNotFoundError) as err:
        main("does-not-exist")

    assert str(err.value) == "does-not-exist"


@pytest.mark.parametrize(
    "args,expected",
    [
        [(long.check_class,), ""],
        [(long.check_class_constructor,), ""],
        [
            (long.check_protected_class_methods, long.check_class),
            f"""\
{PATH}:6 in _Messages
-----------------------------
def fromcode({CHECK}ref) -> {CROSS}Message:
    \"\"\"
    :param ref: {CHECK}
    :return: {CROSS}
    \"\"\"

{E[105].fstring(T)}

{PATH}:12 in _Messages
------------------------------
def all({CHECK}category) -> {CROSS}tuple[None]:
    \"\"\"
    :param category: {CHECK}
    :return: {CROSS}
    \"\"\"

{E[105].fstring(T)}

""",
        ],
        [
            (long.check_protected_class_methods, long.check_class_constructor),
            f"""\
{PATH}:6 in _Messages
-----------------------------
def fromcode({CHECK}ref) -> {CROSS}Message:
    \"\"\"
    :param ref: {CHECK}
    :return: {CROSS}
    \"\"\"

{E[105].fstring(T)}

{PATH}:12 in _Messages
------------------------------
def all({CHECK}category) -> {CROSS}tuple[None]:
    \"\"\"
    :param category: {CHECK}
    :return: {CROSS}
    \"\"\"

{E[105].fstring(T)}

""",
        ],
    ],
    ids=[
        "no-arg-check-class",
        "no-arg=check-class-constructor",
        "arg-check-class",
        "arg=check-class-constructor",
    ],
)
def test_check_protected_class_methods(
    main: MockMainType,
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    args: tuple[str],
    expected: str,
) -> None:
    """Test methods are flagged for protected class.

    :param main: Mock ``main`` function.
    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param args: Args to pass to main.
    :param expected: Expected stdout.
    """
    template = """
class _Messages(_t.Dict[int, Message]):
    def __init__(self) -> None:
        self._this_should_not_need_a_docstring

    def fromcode(self, ref: str) -> Message:
        \"\"\"

        :param ref: Codes or symbolic reference.
        \"\"\"

    def all(self, category: int) -> tuple[Message, ...]:
        \"\"\"

        :param category: Category to get.
        \"\"\"
"""
    init_file(template)
    main(".", *args)
    std = capsys.readouterr()
    assert std.out == expected


def test_no_path_or_string(main: MockMainType) -> None:
    """Test error raised when missing essential arguments.

    :param main: Mock ``main`` function.
    """
    assert main() == "the following arguments are required: path(s) or string"


def test_str_path_via_api() -> None:
    """Test passing a path as a string when using api.

    No need to make any assertions, just need to avoid the following:

        AttributeError: 'str' object has no attribute 'exists'
    """
    docsig.docsig(".")


def test_no_duplicate_codes() -> None:
    """Test there are no accidental duplicate codes."""
    codes = [i.code for i in E.values()]
    assert not any(codes.count(x) > 1 for x in codes)


def test_no_duplicate_descriptions() -> None:
    """Test there are no accidental duplicate descriptions."""
    descriptions = [i.description for i in E.values()]
    assert not any(descriptions.count(x) > 1 for x in descriptions)


def test_no_duplicate_symbolic_messages() -> None:
    """Test there are no accidental duplicate symbolic messages."""
    symbolic_messages = [i.symbolic for i in E.values()]
    assert not any(symbolic_messages.count(x) > 1 for x in symbolic_messages)


def test_list_checks(
    main: MockMainType, capsys: pytest.CaptureFixture
) -> None:
    """Test listing of all available checks.

    :param main: Mock ``main`` function.
    :param capsys: Capture sys out.
    """
    main(long.list_checks)
    std = capsys.readouterr()
    assert all(i.code in std.out for i in E.values())
