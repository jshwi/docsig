"""
tests._test
===========
"""

# pylint: disable=protected-access,too-many-lines
from __future__ import annotations

import argparse
import io
import json
import os
import pickle
from pathlib import Path

import pytest

import docsig
from docsig import docsig as _docsig

# noinspection PyProtectedMember
from docsig._report import pretty_print_error
from docsig.messages import FLAKE8 as F
from docsig.messages import TEMPLATE as T
from docsig.messages import E, Message
from docsig.plugin import ValidatePyproject

from . import (
    CHECK_ARGS,
    PATH,
    WILL_ERROR,
    FixtureInitFile,
    FixtureInitPyprojectTomlFile,
    FixtureMain,
    FixtureMakeTree,
)


@pytest.mark.parametrize(
    "arg",
    (
        "-V",
        "--version",
    ),
)
def test_print_version(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    main: FixtureMain,
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


def test_class_and_class_constructor_with_commandline(
    capsys: pytest.CaptureFixture,
    main: FixtureMain,
) -> None:
    """Test that docsig errors when passed incompatible options.

    :param capsys: Capture sys out.
    :param main: Patch package entry point.
    """
    with pytest.raises(SystemExit):
        main(".", "--check-class", "--check-class-constructor")

    std = capsys.readouterr()
    assert "not allowed with argument" in std.err.strip()


def test_class_and_class_constructor_in_interpreter(
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that docsig errors when passed incompatible options.

    :param capsys: Capture sys out.
    """
    assert (
        _docsig(
            string="def function(): pass",
            check_class=True,
            check_class_constructor=True,
        )
    ) == 2
    std = capsys.readouterr()
    assert std.err.strip() == """\
argument to check class constructor not allowed with argument to check class\
"""


def test_class_and_class_constructor_in_commandline_with_config(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    init_pyproject_toml: FixtureInitPyprojectTomlFile,
    main: FixtureMain,
) -> None:
    """Test that docsig errors when passed incompatible options.

    :param monkeypatch: Mock patch environment and attributes.
    :param capsys: Capture sys out.
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
    assert main(".", test_flake8=False) == 2
    std = capsys.readouterr()
    assert std.err.strip() == """\
argument to check class constructor not allowed with argument to check class
please check your pyproject.toml configuration\
"""


@pytest.mark.parametrize(
    "error",
    [
        E[201].ref,
        E[303].ref,
    ],
)
def test_target_report(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
    error: str,
) -> None:
    """Test report only adds the target error provided.

    The test should fail as it matches with the selected target.

    Assert that the error appears in the report to confirm it has
    triggered.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param error: Error to target.
    """
    template = '''
def function(a, b, c) -> None:
    """Description summary.

    :param a: Description of a.
    :param a: Description of a.
    :param b: Description of b.
    :param: Description of d.
    """
'''
    _errors = E[202].ref, E[201].ref, E[303].ref
    init_file(template)
    main(".", "--target", error, test_flake8=False)
    std = capsys.readouterr()
    assert E.from_ref(error).ref in std.out
    assert not any(E.from_ref(e).ref in std.out for e in _errors if e != error)


def test_invalid_target(
    capsys: pytest.CaptureFixture,
    main: FixtureMain,
) -> None:
    """Test invalid target provided.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    """
    assert main(".", "--target", "unknown", test_flake8=False) == 2
    std = capsys.readouterr()
    assert std.err.strip() == "unknown option to target 'unknown'"


def test_lineno(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test printing of three function errors with the line number.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''
def function_1(a, b, c) -> None:
    """Docstring summary.

    :param b: Description of b.
    :param c: Description of c.
    :param a: Description of a.
    """

def function_2(a, b) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """

def function_3(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert f"{PATH}:2" in std.out
    assert f"{PATH}:10" in std.out
    assert f"{PATH}:18" in std.out


def test_file_not_found_error(main: FixtureMain) -> None:
    """Test file-not-found error for incorrect path arg.

    :param main: Mock ``main`` function.
    """
    with pytest.raises(FileNotFoundError) as err:
        main("does-not-exist")

    assert str(err.value) == "does-not-exist"


@pytest.mark.parametrize(
    "args,expected",
    [
        [
            ("--check-class",),
            "",
        ],
        [
            ("--check-class-constructor",),
            "",
        ],
        [
            (
                "--check-protected-class-methods",
                "--check-class",
            ),
            f"""\
{PATH}:6 in _Messages.method_1
    {E[503].fstring(T)}
{PATH}:12 in _Messages.method_2
    {E[503].fstring(T)}
.{os.sep}{PATH}:6:1: {E[503].fstring(F)} '_Messages.method_1'
.{os.sep}{PATH}:12:1: {E[503].fstring(F)} '_Messages.method_2'
""",
        ],
        [
            (
                "--check-protected-class-methods",
                "--check-class-constructor",
            ),
            f"""\
{PATH}:6 in _Messages.method_1
    {E[503].fstring(T)}
{PATH}:12 in _Messages.method_2
    {E[503].fstring(T)}
.{os.sep}{PATH}:6:1: {E[503].fstring(F)} '_Messages.method_1'
.{os.sep}{PATH}:12:1: {E[503].fstring(F)} '_Messages.method_2'
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
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
    args: tuple[str],
    expected: str,
) -> None:
    """Test methods are flagged for protected class.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param args: Args to pass to main.
    :param expected: Expected stdout.
    """
    template = '''
class _Messages(_t.Dict[int, Message]):
    def __init__(self) -> None:
        self._this_should_not_need_a_docstring

    def method_1(self, a: str) -> Message:
        """Docstring summary.

        :param a: Description of a.
        """

    def method_2(self, a: int) -> tuple[Message, ...]:
        """Docstring summary.

        :param a: Description of a.
        """
'''
    init_file(template)
    main(".", *args)
    std = capsys.readouterr()
    assert std.out == expected


def test_no_path_or_string(
    capsys: pytest.CaptureFixture,
    main: FixtureMain,
) -> None:
    """Test error raised when missing essential arguments.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    """
    assert main(test_flake8=False) == 2
    std = capsys.readouterr()
    assert (
        std.err.strip()
        == "the following arguments are required: path(s) or string"
    )


def test_str_path_via_api() -> None:
    """Test passing a path as a string when using api.

    No need to make any assertions, we only need to avoid the following:

        AttributeError: 'str' object has no attribute 'exists'
    """
    _docsig(".")


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
    capsys: pytest.CaptureFixture,
    main: FixtureMain,
) -> None:
    """Test listing of all available checks.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    """
    main("--list-checks", test_flake8=False)
    std = capsys.readouterr()
    assert all(i.ref in std.out for i in E.values())


def test_bad_py_file(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test invalid syntax on a Python file.

    :param monkeypatch: Mock patch environment and attributes.
    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    monkeypatch.setattr("sys.stdout.isatty", lambda: True)
    init_file(WILL_ERROR)
    assert main(".", test_flake8=False) == 123
    std = capsys.readouterr()
    assert E[901].fstring(T) in std.out


def test_bash_script(
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test bash script.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(WILL_ERROR, Path("module") / "file")
    assert main(".") == 0


@pytest.mark.parametrize(
    "test_main,test_flake8",
    [(True, False), (False, True)],
    ids=["main-verbose", "flake8-verbose"],
)
def test_verbose(
    init_file: FixtureInitFile,
    patch_logger: io.StringIO,
    main: FixtureMain,
    test_main: bool,
    test_flake8: bool,
) -> None:
    """Test verbose.

    :param init_file: Initialize a test file.
    :param patch_logger: Logs as an io instance.
    :param main: Mock ``main`` function.
    :param test_main: Whether to test main.
    :param test_flake8: Whether to test flake8.
    """
    template = '''\
def function_1(a, b, c) -> None:
    """Docstring summary.

    :param b: Description of b.
    :param c: Description of c.
    :param a: Description of a.
    """
'''
    init_file(template)
    main(".", "--verbose", test_main=test_main, test_flake8=test_flake8)
    assert "parsing python code successful" in patch_logger.getvalue()


def test_no_color_with_pipe(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Ensure colors are removed when piping output to a file.

    :param monkeypatch: Mock patch environment and attributes.
    :param capsys: Capture sys out.
    """
    template = '''
def function(a, b) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """
'''
    monkeypatch.setattr("sys.stdout.isatty", lambda: True)
    _docsig(string=template)
    std = capsys.readouterr()
    assert "\033[35m" in std.out
    monkeypatch.setattr("sys.stdout.isatty", lambda: False)
    _docsig(string=template)
    std = capsys.readouterr()
    assert "\033[35m" not in std.out


@pytest.mark.parametrize(
    "template,expected",
    [
        (
            '''
def function() -> None:
    """Docstring summary.

    :return: Return description.
    """
''',
            E[502].fstring(T),
        ),
        (
            '''
def function() -> int:
    """Docstring summary."""
''',
            E[503].fstring(T),
        ),
        (
            '''
def function():
    """Docstring summary.

    Returns
    -------
        int
            Return description.
    """
''',
            E[501].fstring(T),
        ),
        (
            '''
class Klass:
    @property
    def method() -> int:
        """Docstring summary.

        Returns
        -------
        int
        Return description.
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
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
    template: str,
    expected: str,
) -> None:
    """Test ignore typechecker.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param template: The template to test.
    :param expected: Expected message.
    """
    init_file(template)
    assert main(".") == 1
    std = capsys.readouterr()
    assert expected in std.out
    assert (
        main(
            ".",
            "--disable=SIG501,SIG502,SIG503,SIG504,SIG505,SIG506",
            test_flake8=False,
        )
        == 0
    )
    std = capsys.readouterr()
    assert expected not in std.out


def test_sorted(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test modules evaluated in sorted order.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Patch package entry point.
    """
    template = '''
def function() -> None:
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
    {E[502].fstring(T)}
{Path('module') / 'file2'}.py:2 in function
    {E[502].fstring(T)}
{Path('module') / 'file3'}.py:2 in function
    {E[502].fstring(T)}
{Path('module') / 'file4'}.py:2 in function
    {E[502].fstring(T)}
"""


def test_multiple_exit_codes(
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test multiple files, where the last exit code is 0.

    Ensure 0 does not override 1.

    :param init_file: Initialize a test file.
    :param main: Patch package entry point.
    """
    t1 = '''\
def function(a, b) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """
'''
    t2 = '''\
def function(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    """
'''
    t3 = """\
def function(a, b, c) -> None:
    pass
"""
    t4 = '''\
def function(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """
'''
    init_file(t1, Path("module") / "file1.py")
    init_file(t2, Path("module") / "file2.py")
    init_file(t3, Path("module") / "file3.py")
    init_file(t4, Path("module") / "file4.py")
    assert main(".", *CHECK_ARGS) == 1


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
    pretty_print_error(
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
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test the necessity of handling index error when getting args.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''\
class ArgumentParser(_a.ArgumentParser):
    def method(self, *args: str, **kwargs: _t.Any) -> None:
        """Docstring summary.

        :param args: Description of args.
        :param kwargs: Description of kwargs.
        """
'''
    init_file(template)
    main(".", "--ignore-args", "--ignore-kwargs")
    std = capsys.readouterr()
    assert E[202].ref in std.out


def test_always_fail_on_astroid_syntax_error_with_string(
    capsys: pytest.CaptureFixture,
    main: FixtureMain,
) -> None:
    """Test invalid syntax on .py file.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    """
    assert (
        main("--string", WILL_ERROR, test_flake8=False, no_ansi=False) == 123
    )
    std = capsys.readouterr()
    assert E[901].fstring(T) in std.out


def test_fail_on_unicode_decode_error_if_py_file(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
    main: FixtureMain,
) -> None:
    """Ensure that the unicode-decode error is handled without error.

    :param tmp_path: Create and return the temporary directory.
    :param capsys: Capture sys out.
    :param main: Patch package entry point.
    """
    pkl = tmp_path / "test.py"
    serialize = [1, 2, 3]
    with open(pkl, "wb") as fout:
        pickle.dump(serialize, fout)  # type: ignore

    assert main(pkl, test_flake8=False) == 2
    std = capsys.readouterr()
    assert E[902].fstring(T) in std.out


def test_pre_commit_compatibility_issue_with_pythonpath_522(
    init_file,
    capsys: pytest.CaptureFixture,
    main: FixtureMain,
) -> None:
    """Test compatibility issues with a Python path.

    :param init_file: Initialize a test file.
    :param capsys: Capture sys out.
    :param main: Patch package entry point.
    """
    t1 = '''\
class BaseClass:
    """My base class."""

    def method(self, a) -> None:
        """Docstring summary.

        :param a: Description of a.
        """
'''
    t2 = '''\
from .bases.base_class import BaseClass

class Implementation(BaseClass):
    """My implementation."""

    def method(self, a) -> None:
        """Docstring summary."""
'''
    init_file("", Path("folder") / "__init__.py")
    init_file(t1, Path("folder") / "bases" / "base_class.py")
    init_file(t2, Path("folder") / "implementation1.py")
    main(".")
    std = capsys.readouterr()
    assert not std.out


@pytest.mark.parametrize(
    "template",
    [
        '''
def function(a) -> None:
    """Test for docsig.

    :param a: this is all lower case.
    """
''',
        '''
def function(a) -> None:
    """Test for docsig.

    :param a: This is all lower case. but this is not.
    """
''',
    ],
    ids=[
        "lowercase",
        "uppercase-sentence-lowercase-sentence",
    ],
)
def test_enforce_capitalisation_should_591(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
    template: str,
) -> None:
    """Test enforce capitalization.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Patch package entry point.
    :param template: Contents to write to file.
    """
    init_file(template)
    assert main(".") == 1
    std = capsys.readouterr()
    assert E[305].ref in std.out


def test_enforce_capitalisation_should_not_after_nonalpha(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test enforce capitalization after nonalpha character.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Patch package entry point.
    """
    template = '''
def function(a=False) -> None:
    """Docstring summary.

    :param a: (Optional) Description of a.
    """
'''
    init_file(template)
    assert main(".") == 0
    std = capsys.readouterr()
    assert E[305].ref not in std.out


def test_enforce_capitalisation_should_not_591(
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test enforce capitalization.

    :param init_file: Initialize a test file.
    :param main: Patch package entry point.
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
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test check-nested in numpy format.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Patch package entry point.
    """
    template = '''
def function(a: int = 42) -> int:
    """
    Function that prints a message and returns the argument + 1

    Parameters
    ----------
    a : int, optional
        Description of a.

    Returns
    -------
    int
        Return description.
    """
    def nested_function(a: int = 42) -> int:
        pass
'''
    init_file(template)
    assert main(".") == 0
    main(".", "--check-nested")
    std = capsys.readouterr()
    assert E[101].ref in std.out


def test_ignore_kwargs_doco_numpy(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test ignore-kwarg documented in numpy format.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Patch package entry point.
    """
    template = '''
def function(a, b, **kwargs) -> None:
    """Proper docstring.

    Parameters
    ----------
        a : int
            Description of a.
        b : int
            Description of b.
        **kwargs : int
            Description of kwargs.
    """
'''
    init_file(template)
    assert main(".") == 0
    main(".", "--ignore-kwargs")
    std = capsys.readouterr()
    assert E[202].ref in std.out


def test_ignore_kwargs_no_doco_numpy(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test ignore-kwarg not documented in numpy format.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Patch package entry point.
    """
    template = '''
def function(a, b, **kwargs) -> None:
    """Proper docstring.

    Parameters
    ----------
        a : int
            Description of a.
        b : int
            Description of b.
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert E[203].ref in std.out
    assert main(".", "--ignore-kwargs") == 0


def test_ignore_typechecker_numpy(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test ignore-typechecker not typed in numpy format.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Patch package entry point.
    """
    template = '''
def function():
    """Proper docstring.

    Returns
    -------
        int
            Return description.
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert E[501].ref in std.out
    assert (
        main(
            ".",
            "--disable=SIG501,SIG502,SIG503,SIG504,SIG505,SIG506",
            test_flake8=False,
        )
        == 0
    )


def test_ignore_typechecker_prop_numpy(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test ignore-typechecker property typed in numpy format.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Patch package entry point.
    """
    template = '''
class Klass:
    @property
    def method() -> int:
        """Docstring summary.

        Returns
        -------
        int
        Return description.
        """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert E[505].ref in std.out
    assert (
        main(
            ".",
            "--disable=SIG501,SIG502,SIG503,SIG504,SIG505,SIG506",
            test_flake8=False,
        )
        == 0
    )


def test_compressed_short_form_warning(
    make_tree: FixtureMakeTree,
    main: FixtureMain,
) -> None:
    """Test warnings for short form options.

    :param make_tree: Create the directory tree from dict mapping.
    :param main: Mock ``main`` function.
    """
    template = """\
def function(a, b) -> None:
    pass
"""
    make_tree({"module": {"file.py": [template]}})
    with pytest.warns(FutureWarning):
        main(".", "-Iv", test_flake8=False)


def test_ignore_no_params(
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test ignore no params.

    :param init_file: Initialize a test file.
    :param main: Patch package entry point.
    """
    template = '''
def function(a=False) -> None:
    """Docstring summary."""
'''
    init_file(template)
    assert main(".", "--ignore-no-params") == 0


@pytest.mark.parametrize(
    "template,expected,retcode",
    [
        (
            """
def function(a, b, c) -> None:
    pass
""",
            (E[101].ref, "warning"),
            0,
        ),
        (
            '''
class Class:
    """Docstring summary."""
    def run(self, leaves) -> defaultdict[BaseFix, list[Node | Leaf]]:
        """Docstring summary.

        Args:
           The leaves of the AST tree to be matched

        Returns:
           A dictionary of node matches with fixers as the keys
        """
''',
            (E[302].ref,),
            1,
        ),
    ],
    ids=[
        "fail-sig101",
        "fail-for-syntax",
    ],
)
# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def test_new_violation(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
    template: str,
    expected: tuple[str, ...],
    retcode: int,
) -> None:
    """Test new violations that don't fail pipeline yet.

    :param monkeypatch: Mock patch environment and attributes.
    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Patch package entry point.
    :param template: The template to test.
    :param expected: Expected in stdout.
    :param retcode: Exit status.
    """
    monkeypatch.setitem(
        docsig.messages.E,
        101,
        Message(
            "SIG101",
            "function is missing a docstring",
            "function-doc-missing",
            new=True,
        ),
    )
    init_file(template)
    assert main(".") == retcode
    std = capsys.readouterr()
    assert all(i in std.out for i in expected)


def test_missing_period(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test missing period.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Patch package entry point.
    """
    template = '''
def function(a) -> None:
    """Docstring summary.

    :param a: Description of a
    """
'''
    init_file(template)
    assert main(".") == 0
    std = capsys.readouterr()
    assert E[306].ref in std.out
    assert "warning" in std.out


def test_validate_pyproject(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test validate pyproject schema plugin.

    :param monkeypatch: Mock patch environment and attributes.
    """
    schema = {
        "$comment": "schema for the docsig tool section in pyproject.toml",
        "$id": "https://docsig.io/en/latest/usage/configuration/schema.json",
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "no-ansi": {
                "type": "boolean",
                "description": "disable ansi output",
                "default": False,
            },
            "verbose": {
                "type": "boolean",
                "description": "increase output verbosity",
                "default": False,
            },
            "check-class": {
                "type": "boolean",
                "description": "check class docstrings",
                "default": False,
            },
            "check-class-constructor": {
                "type": "boolean",
                "description": "check __init__ methods",
                "default": False,
            },
            "check-dunders": {
                "type": "boolean",
                "description": "check dunder methods",
                "default": False,
            },
            "check-nested": {
                "type": "boolean",
                "description": "check nested functions and classes",
                "default": False,
            },
            "check-overridden": {
                "type": "boolean",
                "description": "check overridden methods",
                "default": False,
            },
            "check-property-returns": {
                "type": "boolean",
                "description": "check property return values",
                "default": False,
            },
            "check-protected": {
                "type": "boolean",
                "description": "check protected functions and classes",
                "default": False,
            },
            "check-protected-class-methods": {
                "type": "boolean",
                "description": (
                    "check public methods belonging to protected classes"
                ),
                "default": False,
            },
            "ignore-args": {
                "type": "boolean",
                "description": "ignore args prefixed with an asterisk",
                "default": False,
            },
            "ignore-kwargs": {
                "type": "boolean",
                "description": "ignore kwargs prefixed with two asterisks",
                "default": False,
            },
            "ignore-no-params": {
                "type": "boolean",
                "description": (
                    "ignore docstrings where parameters are not documented"
                ),
                "default": False,
            },
            "disable": {
                "type": "array",
                "items": {"type": "string"},
                "description": "list of rules to disable",
                "default": [],
            },
            "target": {
                "type": "array",
                "items": {"type": "string"},
                "description": "list of rules to target",
                "default": [],
            },
            "exclude": {
                "type": ["string", "array"],
                "items": {"type": "string"},
                "description": (
                    "regular expression of files or dirs to exclude from"
                    " checks"
                ),
                "default": [],
            },
            "excludes": {
                "type": "array",
                "items": {"type": "string"},
                "description": "path glob patterns to exclude from checks",
                "default": None,
            },
            "include-ignored": {
                "type": "boolean",
                "description": (
                    "check files even if they match a gitignore pattern"
                ),
                "default": False,
            },
        },
        "allOf": [
            {"not": {"required": ["check-class", "check-class-constructor"]}},
        ],
    }

    parser = argparse.ArgumentParser(
        description="Check signature params for proper documentation",
    )
    parser.add_argument(
        "path",
        nargs="*",
        action="store",
        type=Path,
        help="directories or files to check",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=docsig.__version__,
    )
    parser.add_argument(
        "-l",
        "--list-checks",
        action="store_true",
        help="display a list of all checks and their messages",
    )
    parser.add_argument(
        "-n",
        "--no-ansi",
        action="store_true",
        help="disable ansi output",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="increase output verbosity",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-c",
        action="store_true",
        help=argparse.SUPPRESS,
        dest="check_class",
    )
    group.add_argument(
        "--check-class",
        action="store_true",
        help="check class docstrings",
        dest="check_class",
    )
    group.add_argument(
        "-C",
        action="store_true",
        help=argparse.SUPPRESS,
        dest="check_class_constructor",
    )
    group.add_argument(
        "--check-class-constructor",
        action="store_true",
        help="check __init__ methods",
        dest="check_class_constructor",
    )
    parser.add_argument(
        "-D",
        action="store_true",
        help=argparse.SUPPRESS,
        dest="check_dunders",
    )
    parser.add_argument(
        "--check-dunders",
        action="store_true",
        help="check dunder methods",
        dest="check_dunders",
    )
    parser.add_argument(
        "-N",
        action="store_true",
        help=argparse.SUPPRESS,
        dest="check_nested",
    )
    parser.add_argument(
        "--check-nested",
        action="store_true",
        help="check nested functions and classes",
        dest="check_nested",
    )
    parser.add_argument(
        "-o",
        action="store_true",
        help=argparse.SUPPRESS,
        dest="check_overridden",
    )
    parser.add_argument(
        "--check-overridden",
        action="store_true",
        help="check overridden methods",
        dest="check_overridden",
    )
    parser.add_argument(
        "-P",
        action="store_true",
        help=argparse.SUPPRESS,
        dest="check_property_returns",
    )
    parser.add_argument(
        "--check-property-returns",
        action="store_true",
        help="check property return values",
        dest="check_property_returns",
    )
    parser.add_argument(
        "-p",
        action="store_true",
        help=argparse.SUPPRESS,
        dest="check_protected",
    )
    parser.add_argument(
        "--check-protected",
        action="store_true",
        help="check protected functions and classes",
        dest="check_protected",
    )
    parser.add_argument(
        "-m",
        action="store_true",
        help=argparse.SUPPRESS,
        dest="check_protected_class_methods",
    )
    parser.add_argument(
        "--check-protected-class-methods",
        action="store_true",
        help="check public methods belonging to protected classes",
        dest="check_protected_class_methods",
    )
    parser.add_argument(
        "--ignore-args",
        action="store_true",
        help="ignore args prefixed with an asterisk",
    )
    parser.add_argument(
        "--ignore-kwargs",
        action="store_true",
        help="ignore kwargs prefixed with two asterisks",
    )
    parser.add_argument(
        "-i",
        action="store_true",
        help=argparse.SUPPRESS,
        dest="ignore_no_params",
    )
    parser.add_argument(
        "--ignore-no-params",
        action="store_true",
        help="ignore docstrings where parameters are not documented",
        dest="ignore_no_params",
    )
    parser.add_argument(
        "--ignore-typechecker",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-d",
        "--disable",
        metavar="LIST",
        action="store",
        default=[],
        help="comma separated list of rules to disable",
    )
    parser.add_argument(
        "-t",
        "--target",
        metavar="LIST",
        action="store",
        default=[],
        help="comma separated list of rules to target",
    )
    parser.add_argument(
        "-e",
        "--exclude",
        action="append",
        default=[],
        metavar="PATTERN",
        help="regular expression of files or dirs to exclude from checks",
    )
    parser.add_argument(
        "-E",
        "--excludes",
        nargs="+",
        metavar="PATH",
        help="path glob patterns to exclude from checks",
    )
    parser.add_argument(
        "-I",
        "--include-ignored",
        action="store_true",
        help="check files even if they match a gitignore pattern",
    )
    parser.add_argument(
        "-s",
        "--string",
        action="store",
        metavar="STR",
        help="string to parse instead of files",
    )

    monkeypatch.setattr(
        "docsig.plugin._validate_pyproject._build_parser",
        lambda: parser,
    )
    assert ValidatePyproject() == schema


def test_prose_after_rst_directive_period_check_applies(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Period check applies to prose that follows a directive block.

    When prose continues after a directive and its indented content,
    SIG306 should evaluate the final prose, not the directive.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''
def func(x) -> None:
    """Summary.

    :param x: A value.

    .. note::
        Some important note.

    See the notes for more
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert E[306].ref in std.out


def test_rst_code_block_mid_description_period_check_applies_to_prose(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Period check applies to prose that follows a code block.

    When a code block appears in the middle of a description and prose
    continues after it, SIG306 should evaluate the final prose, not the
    code block content.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''
def func(x) -> None:
    """Summary.

    :param x: Example usage::

        foo(x=1)

    See the notes for more
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert E[306].ref in std.out


def test_fix_async_function_params_are_checked(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Async functions are subject to the same parameter checks.

    astroid.AsyncFunctionDef is a subclass of FunctionDef, so it is
    handled by the same isinstance check and must not be silently
    skipped.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''
async def fetch(url, timeout):
    """Fetch a resource.

    :param url: The URL to fetch.
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert E[203].ref in std.out


def test_prose_after_list_period_check_applies(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Period check applies to prose that follows a list.

    When a list appears in the middle of a description and prose
    continues after it, SIG306 should evaluate the final prose, not
    exempt it as a list item.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''
def func(x) -> None:
    """Summary.

    :param x: Valid values are:

        - 'bool'
        - 'int'

        See the notes for more
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert E[306].ref in std.out


@pytest.mark.parametrize(
    "description",
    (
        "Send it to Mr. smith for review.",
        "Send it to Dr. smith for review.",
        "Compare option a vs. option b.",
        "Handles lists, dicts, etc. and other types.",
        "Only valid in the U.S. for now.",
    ),
)
def test_abbreviations_do_not_trigger_sig305(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
    description: str,
) -> None:
    """Every known sentence abbreviation is exempt from SIG305.

    The sentence tokenizer knows mr., dr., vs., etc., and u.s. as well
    as the e.g. and i.e. abbreviations asserted elsewhere. Without the
    exemption the text after the abbreviation becomes its own sentence
    fragment, and its lowercase first letter fires SIG305.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Patch package entry point.
    :param description: Parameter description with an abbreviation.
    """
    template = f'''
def function(x) -> None:
    """Docstring summary.

    :param x: {description}
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert E[305].ref not in std.out


def test_numpy_style_detected_by_other_parameters(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Numpy style is detected when Other Parameters is the only header.

    Style detection falls back to rst when no numpy section header
    matches, in which case the numpy-documented parameter would not be
    parsed and params-missing would be reported.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Patch package entry point.
    """
    template = '''
def function(a) -> None:
    """Docstring summary.

    Other Parameters
    ----------------
    a : int
        Description of a.
    """
'''
    init_file(template)
    assert main(".") == 0
    std = capsys.readouterr()
    assert not std.out


def test_google_style_detected_by_arguments(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Google style is detected via the Arguments section header.

    Arguments is an accepted alias for Args, and the only marker of
    google style in this docstring. Without it the docstring falls back
    to rst, the parameter is not parsed, and params-missing is
    reported.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Patch package entry point.
    """
    template = '''
def function(a) -> None:
    """Docstring summary.

    Arguments:
        a (int): Description of a.
    """
'''
    init_file(template)
    assert main(".") == 0
    std = capsys.readouterr()
    assert not std.out


def test_auto_enumerated_list_does_not_trigger_sig306(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Descriptions ending with an auto-enumerated list are exempt.

    The rst auto-enumerator (#.) is a list marker like - or 1. and a
    description ending on a list item does not need to end in a period.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Patch package entry point.
    """
    template = '''
def function(x) -> None:
    """Docstring summary.

    :param x: Steps to run are:

        #. First step
        #. Second step
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert E[306].ref not in std.out


def test_sig503_hint_not_shown_for_param_return(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """The SIG503 syntax hint is not shown for a return param.

    The hint fires when the last docstring line mentions a return that
    looks like a documentation attempt, but :param return: is already
    reported as a parameter that does not exist, so the hint would be
    noise.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Patch package entry point.
    """
    template = '''
def function(a) -> int:
    """Docstring summary.

    :param a: Description of a.
    :param return: Return value.
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert E[503].fstring(T) in std.out
    assert E[503].hint not in std.out


def test_json_line_null_for_file_error(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
    main: FixtureMain,
) -> None:
    """JSON reports use a null line number for whole-file errors.

    Editor plugins consume this contract to mark the whole file rather
    than a single line when a file cannot be checked at all.

    :param monkeypatch: Mock patch environment and attributes.
    :param tmp_path: Create and return the temporary directory.
    :param capsys: Capture sys out.
    :param main: Patch package entry point.
    """
    pkl = tmp_path / "test.py"
    with open(pkl, "wb") as fout:
        pickle.dump([1, 2, 3], fout)  # type: ignore

    monkeypatch.setenv("_DOCSIG_FORMAT_JSON", "1")
    assert main(pkl, test_flake8=False) == 2
    std = capsys.readouterr()
    issues = json.loads(std.out)
    assert issues[0]["line"] is None
    assert issues[0]["exit"] == 2


def test_json_usage_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    main: FixtureMain,
) -> None:
    """JSON usage errors use a null line number.

    Editor plugins consume this contract when a run cannot start at
    all.

    :param monkeypatch: Mock patch environment and attributes.
    :param capsys: Capture sys out.
    :param main: Patch package entry point.
    """
    monkeypatch.setenv("_DOCSIG_FORMAT_JSON", "1")
    assert main(test_flake8=False) == 2
    std = capsys.readouterr()
    issues = json.loads(std.out)
    assert issues[0]["line"] is None
    assert issues[0]["exit"] == 2
    assert "required" in issues[0]["message"]
