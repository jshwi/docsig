"""
tests.misc_test
===============
"""

# pylint: disable=protected-access
from __future__ import annotations

from pathlib import Path

import pytest
from templatest import templates

import docsig
from docsig.messages import TEMPLATE as T
from docsig.messages import E

from . import PATH, InitFileFixtureType, MockMainType, long, short


@pytest.mark.parametrize("arg", (short.V, long.version))
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


def test_class_and_class_constructor_in_interpreter_with_config(
    monkeypatch: pytest.MonkeyPatch,
    main: MockMainType,
) -> None:
    """Test that docsig errors when passed incompatible options.

    :param monkeypatch: Mock patch environment and attributes.
    :param main: Patch package entry point.
    """
    pyproject_toml = Path.cwd() / "pyproject.toml"
    pyproject_toml.write_text(
        """
[tool.docsig]
check-class = true
check-class_constructor = true
check-protected-class-methods = true
""",
        encoding="utf-8",
    )
    monkeypatch.setattr("sys.stdin.isatty", lambda: True)
    assert main(".") == (
        "argument to check class constructor not allowed with argument to"
        " check class\n"
        "please check your pyproject.toml configuration"
    )


@pytest.mark.parametrize("error", ["E106", "E107"])
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
    template = '''
def function_3(param1, param2, param3) -> None:
    """E101,E102,E106,E107.

    :param param1: Fails.
    :param param1: Fails.
    :param param2: Fails.
    :param: Fails.
    """
'''
    _errors = "E102", "E106", "E107"
    init_file(template)
    main(".", "--target", error)
    std = capsys.readouterr()
    assert E.from_ref(error).ref in std.out
    assert not any(E.from_ref(e).ref in std.out for e in _errors if e != error)


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
    assert docsig._stub.Param() != object


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
{PATH}:6 in _Messages.fromcode
    {E[503].fstring(T)}
{PATH}:12 in _Messages.all
    {E[503].fstring(T)}
""",
        ],
        [
            (long.check_protected_class_methods, long.check_class_constructor),
            f"""\
{PATH}:6 in _Messages.fromcode
    {E[503].fstring(T)}
{PATH}:12 in _Messages.all
    {E[503].fstring(T)}
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
    template = '''
class _Messages(_t.Dict[int, Message]):
    def __init__(self) -> None:
        self._this_should_not_need_a_docstring

    def fromcode(self, ref: str) -> Message:
        """

        :param ref: Codes or symbolic reference.
        """

    def all(self, category: int) -> tuple[Message, ...]:
        """

        :param category: Category to get.
        """
'''
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
    assert all(i.ref in std.out for i in E.values())


def test_bad_py_file(
    init_file: InitFileFixtureType,
    main: MockMainType,
) -> None:
    """Test invalid syntax on .py file.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = """
#!/usr/bin/env bash
new-ssl() {
  domain="${1}"
  config="${2:-"${domain}.conf"}"
  openssl \
    req \
    -new \
    -newkey \
    rsa:2048 \
    -nodes \
    -sha256 \
    -out "${domain}.csr" \
    -keyout "${domain}.key" \
    -config "${config}"
}

new-ssl "${@}"
"""
    init_file(template)
    assert main(".") == 1


def test_bash_script(
    main: MockMainType,
) -> None:
    """Test bash script.

    :param main: Mock ``main`` function.
    """
    template = """
#!/usr/bin/env bash
pygmentize-cat() {
  stdin="${1}"
  if command -v pygmentize >/dev/null 2>&1; then
    if pygmentize --help >/dev/null 2>&1; then
      pygmentize -O style=monokai -f console256 -g "${stdin}"
      return 0
    fi
  fi
  cat "${stdin}"
}

pygmentize-cat "${@}"
"""
    assert main(long.string, template) == 0


def test_verbose(main: MockMainType, capsys: pytest.CaptureFixture) -> None:
    """Test verbose.

    :param main: Mock ``main`` function.
    :param capsys: Capture sys out.
    """
    template = """\
#!/bin/bash
echo "Hello, world"
"""
    main(long.string, template, long.verbose)
    std = capsys.readouterr()
    assert "invalid syntax" in std.out


def test_no_color_with_pipe(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Ensure colors are removed when piping output to a file.

    :param monkeypatch: Mock patch environment and attributes.
    :param capsys: Capture sys out.
    """
    template = '''
def function(param1, param2) -> None:
    """...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """
'''
    monkeypatch.setattr("sys.stdout.isatty", lambda: True)
    docsig.docsig(string=template)
    std = capsys.readouterr()
    assert "\033[35m" in std.out
    monkeypatch.setattr("sys.stdout.isatty", lambda: False)
    docsig.docsig(string=template)
    std = capsys.readouterr()
    assert "\033[35m" not in std.out


@pytest.mark.parametrize(
    "args",
    [(long.summary,), (long.disable, "E201")],
    ids=["summary", "disable"],
)
def test_deprecated(main: MockMainType, args: tuple[str, ...]) -> None:
    """Test deprecation.

    :param main: Mock ``main`` function.
    :param args: Arguments to trigger deprecation warning.
    """
    with pytest.deprecated_call():
        main(".", *args)


@pytest.mark.parametrize(
    "template,expected",
    [
        (
            '''
def function(*_, **__) -> None:
    """Proper docstring.

    :return: Returncode.
    """
    return 0
''',
            E[502].fstring(T),
        ),
        (
            '''
def function(*_, **__) -> int:
    """Proper docstring."""
    return 0
''',
            E[503].fstring(T),
        ),
        (
            '''
def function(*_, **__):
    """Proper docstring.


    Returns
    -------
        int
            Returncode.
    """
    return 0
''',
            E[501].fstring(T),
        ),
        (
            '''
class Klass:
    @property
    def function() -> int:
        """Proper docstring.


    Returns
    -------
    int
    Returncode.
"""
return 0
''',
            E[505].fstring(T),
        ),
    ],
    ids=[
        "none-type-documented",
        "type-not-documented",
        "no-type-with-document",
        "property-type-documented",
    ],
)
def test_ignore_typechecker_and_no_prop_returns(
    main: MockMainType,
    capsys: pytest.CaptureFixture,
    template: str,
    expected: str,
) -> None:
    """Test ignore typechecker.

    :param main: Mock ``main`` function.
    :param capsys: Capture sys out.
    :param template: Template to test.
    :param expected: Expected message.
    """
    assert main(long.string, template) == 1
    std = capsys.readouterr()
    assert expected in std.out
    assert main(long.string, template, long.ignore_typechecker) == 0
    std = capsys.readouterr()
    assert expected not in std.out
