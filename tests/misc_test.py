"""
tests.misc_test
===============
"""
# pylint: disable=protected-access
from __future__ import annotations

import pytest
from templatest import templates

import docsig.messages

from . import CHECK, CROSS, InitFileFixtureType, MockMainType, long, short


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
    assert "module/file.py:2" in std.out
    assert "module/file.py:11" in std.out
    assert "module/file.py:19" in std.out


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
module/file.py:6 in _Messages
-----------------------------
def fromcode({CHECK}ref) -> {CROSS}Message:
    \"\"\"
    :param ref: {CHECK}
    :return: {CROSS}
    \"\"\"

{docsig.messages.E105}

module/file.py:12 in _Messages
------------------------------
def all({CHECK}category) -> {CROSS}tuple[None]:
    \"\"\"
    :param category: {CHECK}
    :return: {CROSS}
    \"\"\"

{docsig.messages.E105}

""",
        ],
        [
            (long.check_protected_class_methods, long.check_class_constructor),
            f"""\
module/file.py:6 in _Messages
-----------------------------
def fromcode({CHECK}ref) -> {CROSS}Message:
    \"\"\"
    :param ref: {CHECK}
    :return: {CROSS}
    \"\"\"

{docsig.messages.E105}

module/file.py:12 in _Messages
------------------------------
def all({CHECK}category) -> {CROSS}tuple[None]:
    \"\"\"
    :param category: {CHECK}
    :return: {CROSS}
    \"\"\"

{docsig.messages.E105}

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
