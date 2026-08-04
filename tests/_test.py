"""
tests._test
===========
"""

# pylint: disable=protected-access,too-many-lines
from __future__ import annotations

import argparse
import contextlib
import io
import json
import logging
import os
import pickle
import re
import sys
import warnings
from argparse import Namespace
from pathlib import Path

import astroid
import pytest

import docsig
from docsig import docsig as _docsig

# noinspection PyProtectedMember
from docsig._config import Ignore

# noinspection PyProtectedMember
from docsig._main import _excepthook

# noinspection PyProtectedMember
from docsig._report import pretty_print_error

# noinspection PyProtectedMember
from docsig._stub import Signature
from docsig.messages import FLAKE8 as F
from docsig.messages import TEMPLATE as T
from docsig.messages import E, Message
from docsig.plugin import ValidatePyproject

# noinspection PyProtectedMember
from docsig.plugin._flake8 import Flake8, _cwd_on_sys_path

from . import (
    CHECK_ARGS,
    PATH,
    WILL_ERROR,
    FixtureFlake8,
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

    # noinspection PyUnresolvedReferences
    pretty_print_error(
        BaseException,
        "a base exception",
        no_ansi=True,
    )
    std = capsys.readouterr()
    assert std.err.strip() == "BaseException: a base exception"


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
    assert main(".") == 1
    std = capsys.readouterr()
    assert E[306].ref in std.out


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
    to rst, the parameter is not parsed, and params-missing is reported.

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

    Editor plugins consume this contract when a run cannot start at all.

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


@pytest.mark.parametrize("core_first", [True, False])
def test_flake8_core_options_do_not_collide_with_plugin(
    core_first: bool,
) -> None:
    """Only the plugin's own options are read off the namespace.

    Problem: The sig prefix was stripped with an unanchored replace over
    every option flake8 owns, so flake8's core ``verbose`` and the
    plugin's ``sig_verbose`` both landed on ``verbose`` and the winner
    was decided by registration order alone.

    :param core_first: Register flake8's own options before the
        plugin's, the order flake8 happens to use today.
    """
    # flake8's own verbose must not be read as the plugin's, whichever
    # order the two were registered in
    core = {"verbose": 3, "max_line_length": 79}
    plugin = {"sig_verbose": False, "sig_check_class": True}
    namespace = Namespace(
        **({**core, **plugin} if core_first else {**plugin, **core}),
    )
    Flake8.parse_options(namespace)
    assert Flake8.a.verbose is False
    assert Flake8.a.check_class is True
    assert not hasattr(Flake8.a, "max_line_length")


def test_multi_file_json_is_one_valid_document(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    make_tree: FixtureMakeTree,
    main: FixtureMain,
) -> None:
    """Checking several files emits a single JSON array.

    One array was printed per file with nothing between them, so the
    output of any run over more than one file was rejected by every JSON
    parser, and no entry said which file it came from.

    :param monkeypatch: Mock patch environment and attributes.
    :param capsys: Capture sys out.
    :param make_tree: Create directory tree from dict mapping.
    :param main: Mock ``main`` function.
    """
    template = ["def function(param) -> None:", '    """Summary."""']
    make_tree({"one.py": template, "two.py": template})
    monkeypatch.setenv("_DOCSIG_FORMAT_JSON", "1")
    assert main(".", test_flake8=False) == 1
    std = capsys.readouterr()
    issues = json.loads(std.out)
    assert len(issues) == 2
    assert {Path(i["path"]).name for i in issues} == {"one.py", "two.py"}
    assert all(i["message"].startswith(E[203].ref) for i in issues)


def test_no_excepthook_when_debugging(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Default traceback is preserved when DOCSIG_DEBUG is enabled.

    :param monkeypatch: Mock patch environment and attributes.
    """
    hook = sys.excepthook
    monkeypatch.setattr("sys.excepthook", hook)
    monkeypatch.setenv("DOCSIG_DEBUG", "1")
    _excepthook(no_ansi=False)
    assert sys.excepthook is hook


def test_cwd_already_on_sys_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A search path entry docsig did not add is left in place on exit.

    :param monkeypatch: Mock patch environment and attributes.
    """
    monkeypatch.syspath_prepend(os.getcwd())
    with _cwd_on_sys_path():
        pass
    assert os.path.abspath(os.getcwd()) in sys.path


def test_signature_of_unknown_args() -> None:
    """An unknown argument list produces a signature with no params.

    astroid types ``Arguments.args`` as optional, so a node whose
    arguments could not be resolved must yield an empty signature
    rather than raise.
    """
    node = astroid.extract_node("def function(): ...")
    node.args.args = None
    signature = Signature.from_ast(node, Ignore())
    assert not signature.args.names


def test_validate_pyproject_uncommon_options(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test schema for option shapes the commandline does not have.

    A scalar option with a non-list default is typed as neither
    boolean nor array, an option without help gets no description, a
    mutually exclusive group with fewer than two schema entries is not
    constrained, and a second group appends to the existing ``allOf``
    list.

    :param monkeypatch: Mock patch environment and attributes.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--custom",
        action="store",
        help="a plain string option",
    )
    parser.add_argument("--quiet", action="store_true")
    lonely = parser.add_mutually_exclusive_group()
    lonely.add_argument("--lonely", action="store_true", help="lonely option")
    first = parser.add_mutually_exclusive_group()
    first.add_argument("--first-a", action="store_true", help="first a")
    first.add_argument("--first-b", action="store_true", help="first b")
    second = parser.add_mutually_exclusive_group()
    second.add_argument("--second-a", action="store_true", help="second a")
    second.add_argument("--second-b", action="store_true", help="second b")
    monkeypatch.setattr(
        "docsig.plugin._validate_pyproject._build_parser",
        lambda: parser,
    )
    schema = ValidatePyproject()
    assert schema["properties"]["custom"] == {
        "default": None,
        "description": "a plain string option",
    }
    assert schema["properties"]["quiet"] == {
        "default": False,
        "type": "boolean",
    }
    assert schema["allOf"] == [
        {"not": {"required": ["first-a", "first-b"]}},
        {"not": {"required": ["second-a", "second-b"]}},
    ]


def test_readme_documents_current_help(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test README.rst's console block matches the parser's help output.

    scripts/update_readme.py regenerates the block, but only `make build`
    ever compares it against the parser, so an option's help text,
    metavar, or flags can drift from what is documented without the suite
    noticing.

    :param monkeypatch: Mock patch environment and attributes.
    """
    monkeypatch.setattr(
        "shutil.get_terminal_size",
        lambda *_, **__: os.terminal_size((93, 24)),
    )
    monkeypatch.setattr("sys.argv", ["docsig", "--help"])
    helpio = io.StringIO()
    with (
        contextlib.redirect_stdout(helpio),
        contextlib.suppress(SystemExit),
    ):
        docsig.main()

    readme = Path(__file__).parent.parent / "README.rst"
    assert re.sub(
        r"^(?=.)",
        "    ",
        helpio.getvalue(),
        flags=re.MULTILINE,
    ) in readme.read_text(encoding="utf-8")


_FLAKE8_CONFIG_OPTIONS = (
    (
        "check-class",
        '''
class Klass:
    """Docstring."""

    def __init__(self, param) -> None:
        pass
''',
    ),
    (
        "check-class-constructor",
        '''
class Klass:
    """Docstring."""

    def __init__(self, param) -> None:
        pass
''',
    ),
    (
        "check-dunders",
        '''
class Klass:
    """Docstring."""

    def __call__(self, param) -> None:
        """Docstring."""
''',
    ),
    (
        "check-nested",
        '''
def function() -> None:
    """Docstring."""

    def nested(param) -> None:
        """Docstring."""
''',
    ),
    (
        "check-overridden",
        '''
class Base:
    """Docstring."""

    def method(self, param) -> None:
        """Docstring.

        :param param: Description of param.
        """


class Child(Base):
    """Docstring."""

    def method(self, param) -> None:
        """Docstring."""
''',
    ),
    (
        "check-property-returns",
        '''
class Klass:
    """Docstring."""

    @property
    def prop(self) -> int:
        """Docstring."""
        return 1
''',
    ),
    (
        "check-protected",
        '''
def _function(param) -> None:
    """Docstring."""
''',
    ),
    (
        "check-protected-class-methods",
        '''
class _Klass:
    """Docstring."""

    def method(self, param) -> None:
        """Docstring."""
''',
    ),
    (
        "ignore-args",
        '''
def function(*args) -> None:
    """Docstring."""
''',
    ),
    (
        "ignore-kwargs",
        '''
def function(**kwargs) -> None:
    """Docstring."""
''',
    ),
    (
        "ignore-no-params",
        '''
def function(param) -> None:
    """Docstring."""
''',
    ),
)


@pytest.mark.parametrize(("option", "template"), _FLAKE8_CONFIG_OPTIONS)
def test_flake8_option_read_from_config(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    flake8: FixtureFlake8,
    option: str,
    template: str,
) -> None:
    """Test each --sig-* option takes effect from a flake8 config file.

    Every option is registered with ``parse_from_config=True``, but the
    suite only ever passes them on the commandline, so an option that
    stopped being read from setup.cfg would go unnoticed.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param flake8: Flake8 plugin fixture.
    :param option: Option to set, without the ``--sig-`` prefix.
    :param template: Source the option changes the result for.
    """
    init_file(template)
    flake8(".")
    baseline = capsys.readouterr()
    flake8(f"--sig-{option}", ".")
    commandline = capsys.readouterr()
    # a template the option makes no difference to would pass the
    # comparison below without testing anything
    assert commandline != baseline
    init_file(f"[flake8]\nsig-{option} = true\n", Path("setup.cfg"))
    flake8(".")
    assert capsys.readouterr() == commandline


def test_confirm_return_needed_carries_hint(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test SIG501 is reported with its hint attached.

    The hint is the only thing telling the user an annotation resolves
    the ambiguity, and nothing asserted it was ever printed.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file('''
def function(a):
    """Summary.

    :param a: Description of a.
    """
''')
    main(".", test_flake8=False)
    std = capsys.readouterr()
    assert E[501].ref in std.out
    assert E[501].hint in std.out


def test_bad_closing_token_carries_hint(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test SIG304 is reported with its hint attached.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file('''
def function(a) -> None:
    """Summary.

    :param a- Description of a.
    """
''')
    main(".", test_flake8=False)
    std = capsys.readouterr()
    assert E[304].ref in std.out
    assert E[304].hint in std.out


def test_new_violation_warns_and_flags_the_report(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test a message flagged new warns rather than erroring outright.

    A new violation is announced with a FutureWarning and its report
    line carries a reminder, so a check can land before it starts
    failing builds. No message sets the flag today, so nothing
    exercised the path.

    :param monkeypatch: Mock patch environment and attributes.
    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    monkeypatch.setitem(E, 203, E[203]._replace(new=True))
    init_file('''
def function(a) -> None:
    """Summary."""
''')
    with pytest.warns(FutureWarning, match=E[203].ref):
        main(".", test_flake8=False)

    std = capsys.readouterr()
    assert "warning: please remember to fix this or disable it" in std.out


def test_new_violation_warning_silenced_for_json(
    monkeypatch: pytest.MonkeyPatch,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test the new-violation warning stays out of json output.

    The warning would be written to stderr alongside the document, so
    _DOCSIG_FORMAT_JSON silences it.

    :param monkeypatch: Mock patch environment and attributes.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    monkeypatch.setitem(E, 203, E[203]._replace(new=True))
    monkeypatch.setenv("_DOCSIG_FORMAT_JSON", "1")
    init_file('''
def function(a) -> None:
    """Summary."""
''')
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        main(".", test_flake8=False)

    assert not [i for i in caught if issubclass(i.category, FutureWarning)]


def test_param_at_match_lower_bound_is_not_spelling_error(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test a name matching at exactly the lower bound is not a typo.

    "para" and "params" match at a ratio of exactly 0.8, and the bound
    is exclusive, so the pair is too far apart to call a misspelling.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file('''
def function(para) -> None:
    """Summary.

    :param params: Description of params.
    """
''')
    main(".", test_flake8=False)
    std = capsys.readouterr()
    assert E[404].ref in std.out
    assert E[403].ref not in std.out


def test_list_description_needs_no_period(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test a description ending on a list item is not missing a period.

    A list item is not a sentence, so SIG306 does not apply to it.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file('''
def function(a) -> None:
    """Summary.

    :param a: - item one
        - item two
    """
''')
    assert main(".", test_flake8=False) == 0
    assert E[306].ref not in capsys.readouterr().out


def test_directive_ending_description_needs_no_period(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test a description ending in a directive needs no terminator.

    The directive and its indented body are not prose, so the last
    sentence terminator before them is the one that counts.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file('''
def function(a) -> None:
    """Summary.

    :param a: Text.

        .. versionadded:: 1.0
            Indented content
    """
''')
    assert main(".", test_flake8=False) == 0
    assert E[306].ref not in capsys.readouterr().out


def test_similar_param_names_partly_documented(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test near-identical names left undocumented report only once.

    param1 is almost equal to param2, so lining the two lists up has to
    look ahead to the next signature param, or the documented names read
    as merely out of order on top of the one that is missing.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file('''
def function(param1, param2, param3) -> None:
    """Summary.

    :param param2: Second.
    :param param3: Third.
    """
''')
    main(".", test_flake8=False)
    std = capsys.readouterr()
    assert E[203].ref in std.out
    assert E[402].ref not in std.out


def test_sentence_after_abbreviation_must_be_capitalized(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test tokenizing continues past an abbreviation.

    "e.g." is not a sentence boundary, but the sentence that really does
    follow it still has to start with a capital.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file('''
def function(a) -> None:
    """Summary.

    :param a: See e.g. this. also lowercase.
    """
''')
    main(".", test_flake8=False)
    assert E[305].ref in capsys.readouterr().out


def test_indent_anomaly_after_field_at_margin(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test an odd indent is found after a field sitting at the margin.

    The first field establishes the margin without being an anomaly
    itself, so the scan continues to the field that is misaligned.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file('''
def function(a, b) -> None:
    """Summary.

    :param a: At margin.
     :param b: Odd indent.
    """
''')
    main(".", test_flake8=False)
    assert E[401].ref in capsys.readouterr().out


def test_docstring_of_only_a_field_has_no_margin(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test a docstring that is a single field line is handled.

    There is no line below the summary to take a margin from, so the
    margin falls back to zero rather than to nothing at all.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file('''
def function(a) -> None:
    """:param a: Only a field."""
''')
    assert main(".", test_flake8=False) == 0
    assert not capsys.readouterr().out.strip()


def test_string_input_header_has_no_path_prefix(
    capsys: pytest.CaptureFixture,
    main: FixtureMain,
) -> None:
    """Test a string parsed with --string reports no file prefix.

    There is no file to name, so the header is the line number alone.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    """
    main("--string", "def function(a):\n    pass\n", test_flake8=False)
    std = capsys.readouterr()
    assert std.out.startswith("1 in function")


def test_syntax_error_reported_at_line_zero(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test an unparsable module is reported against line zero.

    The module never parsed, so there is no line to blame, and the
    report says so rather than pointing at the first line.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file("def function(:\n    pass\n")
    assert main(".", test_flake8=False) == 123
    std = capsys.readouterr()
    assert f"{PATH}:0 in module" in std.out


def test_json_report_carries_the_line_number(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test each json diagnostic reports the line it was found on.

    Editor plugins position their diagnostics with it.

    :param monkeypatch: Mock patch environment and attributes.
    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    monkeypatch.setenv("_DOCSIG_FORMAT_JSON", "1")
    init_file('''
def function(a) -> None:
    """Summary."""
''')
    main(".", test_flake8=False)
    diagnostics = json.loads(capsys.readouterr().out)
    assert diagnostics
    assert all(i["line"] == 2 for i in diagnostics)


def test_protected_method_skipped_by_default(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test a protected method is only checked when asked for.

    A protected function at module level never reaches the check, so
    the guard only ever bites on a method.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file('''
class Klass:
    """Summary."""

    def _protected(self, param) -> None:
        """Summary."""
''')
    assert main(".", test_flake8=False) == 0
    assert not capsys.readouterr().out.strip()
    assert main(".", "--check-protected", test_flake8=False) != 0
    assert E[203].ref in capsys.readouterr().out


def test_string_parse_logs_against_stdin(
    patch_logger: io.StringIO,
    main: FixtureMain,
) -> None:
    """Test source given as a string is logged as coming from stdin.

    There is no file to name, and the log line is the only place the
    distinction shows.

    :param patch_logger: Logs as an io instance.
    :param main: Mock ``main`` function.
    """
    main(
        "--string",
        'def function(a) -> None:\n    """Summary.\n\n'
        '    :param a: Description of a.\n    """\n',
        "--verbose",
        test_flake8=False,
    )
    assert "stdin: parsing python code successful" in patch_logger.getvalue()


def test_syntax_error_logged_on_a_single_line(
    patch_logger: io.StringIO,
    main: FixtureMain,
) -> None:
    """Test a parse failure is logged folded onto one line.

    The error carries the offending source across several lines, and a
    log record spanning lines is unreadable next to the others.

    :param patch_logger: Logs as an io instance.
    :param main: Mock ``main`` function.
    """
    main(
        "--string",
        "def function(:\n    pass\n",
        "--verbose",
        test_flake8=False,
    )
    assert (
        "stdin: parsing python code failed: invalid syntax (<unknown>, line 1)"
        in patch_logger.getvalue()
    )


def test_module_name_derived_from_the_path(
    patch_logger: io.StringIO,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test the module a file is parsed as is named after its path.

    The suffix goes, separators become dots, and a hyphen is not legal
    in a module name so it becomes an underscore.

    :param patch_logger: Logs as an io instance.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file("def broken(:\n    pass\n", Path("mod-ule") / "fi-le.py")
    main(".", "--verbose", test_flake8=False)
    assert "(mod_ule.fi_le, line 1)" in patch_logger.getvalue()


def test_undecodable_file_logged_against_its_path(
    patch_logger: io.StringIO,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test a file that will not decode is logged with its path.

    :param patch_logger: Logs as an io instance.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    file = init_file("")
    file.write_bytes(b'def function():\n    """Summary \xff\xfe."""\n')
    main(".", "--verbose", test_flake8=False)
    assert (
        f"{PATH}: 'utf-8' codec can't decode byte 0xff"
        in patch_logger.getvalue()
    )


def test_directive_token_error_logged_against_the_file(
    patch_logger: io.StringIO,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test comments that will not tokenize are logged, not fatal.

    The ast parses, so the module is still worth checking; only the
    directives in it are given up on, and the log line is the only
    record that they were.

    :param patch_logger: Logs as an io instance.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = r'''
"""The problem is the trailing line continuation at the end of the line,
which produces a TokenError."""
# +2: [syntax-error]
""\
'''
    init_file(template)
    assert main(".", "--verbose", test_flake8=False) == 0
    assert (
        f"{PATH}: error parsing comments ('eof in multi-line statement'"
        in patch_logger.getvalue()
    )


def test_broken_symlink_logged_then_skipped(
    patch_logger: io.StringIO,
    tmp_path: Path,
    main: FixtureMain,
) -> None:
    """Test a link with no target is passed over, not raised on.

    A path that does not exist is an error worth stopping for, unless
    it is a link, which is only worth a note.

    :param patch_logger: Logs as an io instance.
    :param tmp_path: Create and return the temporary directory.
    :param main: Mock ``main`` function.
    """
    link = tmp_path / "broken.py"
    link.symlink_to(tmp_path / "does-not-exist")
    assert main(".", "--verbose", test_flake8=False) == 0
    assert "broken.py: broken link, skipping" in patch_logger.getvalue()


def test_verbose_output_goes_to_stdout(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test the log docsig sets up writes to stdout.

    The report goes to stdout, and the verbose log belongs alongside it
    rather than mixed into stderr.

    :param monkeypatch: Mock patch environment and attributes.
    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    monkeypatch.setattr(
        logging.getLogger(docsig.__name__),
        "handlers",
        [],
    )
    init_file('''
def function(a) -> None:
    """Summary.

    :param a: Description of a.
    """
''')
    main(".", "--verbose", test_flake8=False)
    std = capsys.readouterr()
    assert "parsing python code successful" in std.out
    assert "parsing python code successful" not in std.err


def test_main_installs_the_friendly_excepthook(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    main: FixtureMain,
) -> None:
    """Test an error escaping docsig prints without a traceback.

    A path that does not exist is the user's mistake, not a crash to
    debug, so main leaves behind a hook that prints the error alone,
    coloured unless ansi is turned off.

    :param monkeypatch: Mock patch environment and attributes.
    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    """
    monkeypatch.setattr("sys.excepthook", sys.excepthook)
    monkeypatch.setattr("sys.stdout.isatty", lambda: True)
    err = FileNotFoundError("does-not-exist")
    with pytest.raises(FileNotFoundError):
        main("does-not-exist", test_flake8=False, no_ansi=False)

    sys.excepthook(FileNotFoundError, err, None)
    assert capsys.readouterr().err.strip() == (
        "\033[1;31mFileNotFoundError\033[0m: does-not-exist"
    )
    with pytest.raises(FileNotFoundError):
        main("does-not-exist", test_flake8=False)

    sys.excepthook(FileNotFoundError, err, None)
    assert (
        capsys.readouterr().err.strip() == "FileNotFoundError: does-not-exist"
    )


def test_list_item_body_may_continue_indented(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test a list item in a field body may be continued deeper.

    An indent below a list item continues that item, so it is not the
    unexpected indentation that rst would reject.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file('''
def function(a) -> None:
    """Summary.

    :param a:
        - one
            continued deeper
    """
''')
    main(".", test_flake8=False)
    assert E[302].ref not in capsys.readouterr().out


def test_unexpected_indent_found_after_a_blank_line(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test a field body is checked past the paragraph it starts with.

    A blank line ends a paragraph rather than the body, so a paragraph
    below one is still rst that has to hold together.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file('''
def function(a) -> None:
    """Summary.

    :param a:
        Body line.

        Second para.
            Deeper unexpectedly.
    """
''')
    main(".", test_flake8=False)
    assert E[302].ref in capsys.readouterr().out


def test_literal_block_body_may_indent_deeper(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test a line opening a literal block may be indented under.

    A line ending in a double colon opens a literal block, and the
    block is indented under it by definition.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file('''
def function(a) -> None:
    """Summary.

    :param a:
        Body::
            literal deeper
    """
''')
    main(".", test_flake8=False)
    assert E[302].ref not in capsys.readouterr().out


def test_blank_description_is_not_missing_a_period(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test a description of only whitespace has no sentence to end.

    There is no prose in it, so there is no last character to hold to a
    terminator.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    # written this way so the trailing whitespace the case needs
    # survives the hook that strips it from the source
    blank = " " * 2
    init_file(f'''
def function(a) -> None:
    """Summary.

    :param a:{blank}
    """
''')
    main(".", test_flake8=False)
    assert E[306].ref not in capsys.readouterr().out


def test_bare_explicit_markup_starts_a_block(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test a lone double dot opens a block like a directive does.

    Rst explicit markup is two dots, with or without a directive after
    them, so what is indented under it belongs to it and is not prose
    needing a terminator.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file('''
def function(a) -> None:
    """Summary.

    :param a: Text.

        ..
            some content here
    """
''')
    main(".", test_flake8=False)
    assert E[306].ref not in capsys.readouterr().out


def test_list_item_ending_a_block_is_the_paragraph(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test the line that closes a block starts the paragraph after it.

    A literal block runs until something returns to the margin, and
    when that something is a list item the description ends on a list
    item, which needs no terminator.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file('''
def function(a) -> None:
    """Summary.

    :param a: Intro::
    - list at field indent
    """
''')
    main(".", test_flake8=False)
    assert E[306].ref not in capsys.readouterr().out
