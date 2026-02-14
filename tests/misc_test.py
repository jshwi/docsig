"""
tests.misc_test
===============
"""

# pylint: disable=protected-access
from __future__ import annotations

import io
import os
import pickle
from pathlib import Path

import pytest
from templatest import templates

import docsig
from docsig.messages import FLAKE8 as F
from docsig.messages import TEMPLATE as T
from docsig.messages import E

from . import (
    CHECK_ARGS,
    FixtureInitPyprojectTomlFile,
    FixtureMakeTree,
    InitFileFixtureType,
    MockMainType,
)
from ._templates import PATH


@pytest.mark.parametrize("arg", ("-V", "--version"))
def test_print_version(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    arg: str,
) -> None:
    """Test printing of the program's version on the commandline.

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
    capsys: pytest.CaptureFixture,
    main: MockMainType,
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
        string="def function(): pass",
        check_class=True,
        check_class_constructor=True,
    ) == (
        "argument to check class constructor not allowed with argument to"
        " check class"
    )


def test_class_and_class_constructor_in_interpreter_with_config(
    monkeypatch: pytest.MonkeyPatch,
    init_pyproject_toml: FixtureInitPyprojectTomlFile,
    main: MockMainType,
) -> None:
    """Test that docsig errors when passed incompatible options.

    :param monkeypatch: Mock patch environment and attributes.
    :param init_pyproject_toml: Initialize a test pyproject.toml file.
    :param main: Patch package entry point.
    """
    init_pyproject_toml(
        {
            "check-class": True,
            "check-class_constructor": True,
            "check-protected-class-methods": True,
        },
    )
    monkeypatch.setattr("sys.stdin.isatty", lambda: True)
    assert main(".", test_flake8=False) == (
        "argument to check class constructor not allowed with argument to"
        " check class\n"
        "please check your pyproject.toml configuration"
    )


@pytest.mark.parametrize("error", ["SIG201", "SIG303"])
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
    """Description summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param: Description of param.
    """
'''
    _errors = "SIG202", "SIG201", "SIG303"
    init_file(template)
    main(".", "--target", error, test_flake8=False)
    std = capsys.readouterr()
    assert E.from_ref(error).ref in std.out
    assert not any(E.from_ref(e).ref in std.out for e in _errors if e != error)


def test_invalid_target(main: MockMainType) -> None:
    """Test invalid target provided.

    :param main: Mock ``main`` function.
    """
    assert (
        main(".", "--target", "unknown", test_flake8=False)
        == "unknown option to target 'unknown'"
    )


def test_lineno(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
) -> None:
    """Test printing of three function errors with the line number.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(
        templates.registered.getbyname("m-fail-s").template,  # type: ignore
    )
    main(".")
    std = capsys.readouterr()
    assert f"{PATH}:2" in std.out
    assert f"{PATH}:10" in std.out
    assert f"{PATH}:18" in std.out


def test_file_not_found_error(main: MockMainType) -> None:
    """Test file-not-found error for incorrect path arg.

    :param main: Mock ``main`` function.
    """
    with pytest.raises(FileNotFoundError) as err:
        main("does-not-exist")

    assert str(err.value) == "does-not-exist"


@pytest.mark.parametrize(
    "args,expected",
    [
        [("--check-class",), ""],
        [("--check-class-constructor",), ""],
        [
            ("--check-protected-class-methods", "--check-class"),
            f"""\
{PATH}:6 in _Messages.fromcode
    {E[503].fstring(T)}
{PATH}:12 in _Messages.all
    {E[503].fstring(T)}
.{os.sep}{PATH}:6:1: {E[503].fstring(F)} '_Messages.fromcode'
.{os.sep}{PATH}:12:1: {E[503].fstring(F)} '_Messages.all'
""",
        ],
        [
            ("--check-protected-class-methods", "--check-class-constructor"),
            f"""\
{PATH}:6 in _Messages.fromcode
    {E[503].fstring(T)}
{PATH}:12 in _Messages.all
    {E[503].fstring(T)}
.{os.sep}{PATH}:6:1: {E[503].fstring(F)} '_Messages.fromcode'
.{os.sep}{PATH}:12:1: {E[503].fstring(F)} '_Messages.all'
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
    assert (
        main(test_flake8=False)
        == "the following arguments are required: path(s) or string"
    )


def test_str_path_via_api() -> None:
    """Test passing a path as a string when using api.

    No need to make any assertions, we only need to avoid the following:

        AttributeError: 'str' object has no attribute 'exists'
    """
    docsig.docsig(".")


def test_no_duplicate_codes() -> None:
    """Test there are no accidental duplicate codes."""
    codes = [i.ref for i in E.values()]
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
    main: MockMainType,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test listing of all available checks.

    :param main: Mock ``main`` function.
    :param capsys: Capture sys out.
    """
    main("--list-checks", test_flake8=False)
    std = capsys.readouterr()
    assert all(i.ref in std.out for i in E.values())


def test_bad_py_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
) -> None:
    """Test invalid syntax on a python file.

    :param tmp_path: Create and return the temporary directory.
    :param monkeypatch: Mock patch environment and attributes.
    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template1 = """
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
    template2 = '''
def function(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """
'''
    monkeypatch.setattr("sys.stdout.isatty", lambda: True)
    init_file(template1, tmp_path / "module" / "file1.py")
    init_file(template2, tmp_path / "module" / "file2.py")
    assert main(".", test_flake8=False, no_ansi=False) == 123
    std = capsys.readouterr()
    assert E[901].fstring(T) in std.out


def test_bash_script(
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Test bash script.

    :param main: Mock ``main`` function.
    :param init_file: Initialize a test file.
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
    init_file(template, Path("module") / "file")
    assert main(".") == 0


def test_verbose(
    main: MockMainType,
    init_file: InitFileFixtureType,
    patch_logger: io.StringIO,
) -> None:
    """Test verbose.

    :param main: Mock ``main`` function.
    :param init_file: Initialize a test file.
    :param patch_logger: Logs as an io instance.
    """
    template = """\
#!/bin/bash
echo "Hello, world"
"""
    init_file(template, Path("module") / "file")
    main(".", "--verbose", test_flake8=False)
    assert "invalid syntax" in patch_logger.getvalue()


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
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
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
    "template,expected",
    [
        (
            '''
def function(*_, **__) -> None:
    """Docstring summary.

    :return: Return description.
    """
''',
            E[502].fstring(T),
        ),
        (
            '''
def function(*_, **__) -> int:
    """Docstring summary."""
''',
            E[503].fstring(T),
        ),
        (
            '''
def function(*_, **__):
    """Docstring summary.

    Returns
    -------
        int
            Returncode.
    """
''',
            E[501].fstring(T),
        ),
        (
            '''
class Klass:
    @property
    def function() -> int:
        """Docstring summary.

        Returns
        -------
        int
        Returncode.
        """
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
    init_file: InitFileFixtureType,
    template: str,
    expected: str,
) -> None:
    """Test ignore typechecker.

    :param main: Mock ``main`` function.
    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param template: The template to test.
    :param expected: Expected message.
    """
    init_file(template)
    assert main(".") == 1
    std = capsys.readouterr()
    assert expected in std.out
    assert main(".", "--ignore-typechecker") == 0
    std = capsys.readouterr()
    assert expected not in std.out


def test_sorted(
    main: MockMainType,
    init_file: InitFileFixtureType,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test modules evaluated in sorted order.

    :param main: Patch package entry point.
    :param init_file: Initialize a test file.
    :param capsys: Capture sys out.
    """
    template = '''
def function(*_, **__) -> None:
    """Docstring summary.

    :return: Return description.
    """
'''
    init_file(template, Path("module") / "file1.py")
    init_file(template, Path("module") / "file2.py")
    init_file(template, Path("module") / "file3.py")
    init_file(template, Path("module") / "file4.py")
    main(
        ".",
        *CHECK_ARGS,
        test_flake8=False,  # won't need, flake runs one file at a time
    )
    std = capsys.readouterr()
    assert std.out == f"""\
{Path('module') / 'file1'}.py:2 in function
    SIG502: return statement documented for None (return-documented-for-none)
{Path('module') / 'file2'}.py:2 in function
    SIG502: return statement documented for None (return-documented-for-none)
{Path('module') / 'file3'}.py:2 in function
    SIG502: return statement documented for None (return-documented-for-none)
{Path('module') / 'file4'}.py:2 in function
    SIG502: return statement documented for None (return-documented-for-none)
"""


def test_multiple_exit_codes(
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Test multiple files, where the last exit code is 0.

    Ensure 0 does not override 1.

    :param main: Patch package entry point.
    :param init_file: Initialize a test file.
    """
    init_file(
        templates.registered.getbyname(
            "f-param-docs-s",
        ).template,  # type: ignore
        Path("module") / "file1.py",
    )
    init_file(
        templates.registered.getbyname(
            "f-param-sig-s",
        ).template,  # type: ignore
        Path("module") / "file2.py",
    )
    init_file(
        templates.registered.getbyname(
            "f-no-doc-no-ret-s",
        ).template,  # type: ignore
        Path("module") / "file3.py",
    )
    init_file(
        templates.registered.getbyname("p-param-s").template,  # type: ignore
        Path("module") / "file4.py",
    )
    assert (
        main(
            ".",
            *CHECK_ARGS,
            test_flake8=False,  # won't need, flake runs one file at a time
        )
        == 1
    )


def test_sys_excepthook(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Get coverage on except hook.

    Unsure what errors are relevant after removing the syntax error from
    this hook.

    :param monkeypatch: Mock patch environment and attributes.
    :param capsys: Capture sys out.
    """
    monkeypatch.setattr("sys.stdout.isatty", lambda: True)

    # noinspection PyUnresolvedReferences
    docsig._utils.pretty_print_error(
        BaseException,
        "a base exception",
        no_ansi=False,
    )
    std = capsys.readouterr()
    assert (
        std.err.strip() == "\033[1;31mBaseException\033[0m: a base exception"
    )


def test_ignore_args_ignore_kwargs_index_error(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Test the necessity of handling index error when getting args.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    :param init_file: Initialize a test file.
    """
    template = '''\
class ArgumentParser(_a.ArgumentParser):
    def add_list_argument(self, *args: str, **kwargs: _t.Any) -> None:
        """Parse a comma separated list of strings into a list.

        :param args: Long and/or short form argument(s).
        :param kwargs: Kwargs to pass to ``add_argument``.
        """
'''
    init_file(template)
    main(".", "-a", "--ignore-kwargs", test_flake8=False)
    std = capsys.readouterr()
    assert docsig.messages.E[202].description in std.out


def test_always_fail_on_astroid_syntax_error_with_string(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
) -> None:
    """Test invalid syntax on .py file.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    """
    template = """\
#!/bin/bash
echo "Hello, world"
"""
    assert main("--string", template, test_flake8=False, no_ansi=False) == 123
    std = capsys.readouterr()
    assert E[901].fstring(T) in std.out


def test_fail_on_unicode_decode_error_if_py_file(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    tmp_path: Path,
) -> None:
    """Ensure that the unicode-decode error is handled without error.

    :param capsys: Capture sys out.
    :param main: Patch package entry point.
    :param tmp_path: Create and return the temporary directory.
    """
    pkl = tmp_path / "test.py"
    serialize = [1, 2, 3]
    with open(pkl, "wb") as fout:
        pickle.dump(serialize, fout)  # type: ignore

    assert main(pkl, test_flake8=False) == 1
    std = capsys.readouterr()
    assert E[902].fstring(T) in std.out


def test_pre_commit_compatibility_issue_with_pythonpath_522(
    main: MockMainType,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test compatibility issues with a Python path.

    :param main: Patch package entry point.
    :param tmp_path: Create and return the temporary directory.
    :param capsys: Capture sys out.
    """
    t1 = '''\
class BaseClass:
    """My base class."""

    def method(self, arg) -> None:
        """Does something.

        :param arg: Some argument
        """
'''
    t2 = '''\
from .bases.base_class import BaseClass

class Implementation(BaseClass):
    """My implementation."""

    def method(self, arg) -> None:
        """Does something."""
'''
    root = tmp_path / "folder"
    bases = root / "bases"
    bases.mkdir(exist_ok=True, parents=True)
    (root / "__init__.py").touch()
    p1 = bases / "base_class.py"
    p2 = root / "implementation1.py"
    p1.write_text(t1)
    p2.write_text(t2)
    main(".")
    std = capsys.readouterr()
    assert not std.out


def test_enforce_capitalisation_should_591(
    main: MockMainType,
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
) -> None:
    """Test enforce capitalisation.

    :param main: Patch package entry point.
    :param capsys: Capture sys out.
    :param init_file: Initialise a test file.
    """
    t1 = '''
def foo(a) -> None:
    """Test for docsig.

    :param a: this is all lower case.
    """
'''
    t2 = '''
def foo(a) -> None:
    """Test for docsig.

    :param a: This is all lower case. but this is not.
    """
'''
    init_file(t1)
    init_file(t2)
    assert main(".") == 1
    std = capsys.readouterr()
    assert docsig.messages.E[305].description in std.out


def test_enforce_capitalisation_should_not_591(
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Test enforce capitalization.

    :param main: Patch package entry point.
    :param init_file: Initialize a test file.
    """
    template = '''
def function(a) -> None:
    """Function summary.

    :param a: Description of param e.g. not a new sentence.
    """
'''
    init_file(template)
    assert main(".") == 0


def test_check_nested_numpy(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Test check-nested in numpy format.

    :param capsys: Capture sys out.
    :param main: Patch package entry point.
    :param init_file: Initialize a test file.
    """
    template = '''
def my_function(argument: int = 42) -> int:
    """
    Function that prints a message and returns the argument + 1

    Parameters
    ----------
    argument : int, optional
        The input argument, by default 42

    Returns
    -------
    int
        The input argument + 1
    """
    def my_external_function(argument: int = 42) -> int:
        pass
'''
    init_file(template)
    assert main(".") == 0
    main(".", "--check-nested")
    std = capsys.readouterr()
    assert docsig.messages.E[101].description in std.out


def test_ignore_kwargs_doco_numpy(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Test ignore-kwarg documented in numpy format.

    :param capsys: Capture sys out.
    :param main: Patch package entry point.
    :param init_file: Initialize a test file.
    """
    template = '''
def function(param1, param2, **kwargs) -> None:
    """Proper docstring.

    Parameters
    ----------
        param1 : int
            Pass.
        param2 : int
            Pass.
        **kwargs : int
            Pass
    """
'''
    init_file(template)
    assert main(".") == 0
    main(".", "--ignore-kwargs")
    std = capsys.readouterr()
    assert docsig.messages.E[202].description in std.out


def test_ignore_kwargs_no_doco_numpy(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Test ignore-kwarg not documented in numpy format.

    :param capsys: Capture sys out.
    :param main: Patch package entry point.
    :param init_file: Initialize a test file.
    """
    template = '''
def function(param1, param2, **kwargs) -> None:
    """Proper docstring.

    Parameters
    ----------
        param1 : int
            Pass.
        param2 : int
            Pass.
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert docsig.messages.E[203].description in std.out
    assert main(".", "--ignore-kwargs") == 0


def test_ignore_typechecker_numpy(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Test ignore-typechecker not typed in numpy format.

    :param capsys: Capture sys out.
    :param main: Patch package entry point.
    :param init_file: Initialize a test file.
    """
    template = '''
def function(*_, **__):
    """Proper docstring.

    Returns
    -------
        int
            Returncode.
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert docsig.messages.E[501].description in std.out
    assert main(".", "--ignore-typechecker") == 0


def test_ignore_typechecker_prop_numpy(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Test ignore-typechecker property typed in numpy format.

    :param capsys: Capture sys out.
    :param main: Patch package entry point.
    :param init_file: Initialize a test file.
    """
    template = '''
class Klass:
    @property
    def function() -> int:
        """Proper docstring.

        Returns
        -------
        int
        Returncode.
        """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert docsig.messages.E[505].description in std.out
    assert main(".", "--ignore-typechecker") == 0


def test_compressed_short_form_warning(
    main: MockMainType,
    make_tree: FixtureMakeTree,
) -> None:
    """Test warnings for short form options.

    :param main: Mock ``main`` function.
    :param make_tree: Create the directory tree from dict mapping.
    """
    template = """\
def function(a, b) -> None:
    pass
"""
    make_tree({"module": {"file.py": [template]}})
    with pytest.warns(FutureWarning):
        main(".", "-cDmNopPiaI", test_flake8=False)
