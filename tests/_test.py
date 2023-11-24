"""Test suite of docsig.

Most tests run with all the args that start with ``check``, so passing
or failing of most tests depend on these passing. This means, by
default, that templates including classes, magic methods, overridden
methods, protected methods, and property returns, will be checked, even
though by default they aren't.

There are separate tests written to exclude these particular flags.
Their templates contain a specific string to include them in these
special case tests.

Some tests overlap, which is why some templates are found by their
prefix, their suffix, or whether they simply contain a substring.

All templates ending with ``S`` are ``Sphinx`` style docstrings, all
templates ending with ``N`` are ``NumPy`` style docstrings, all
templates ending with ``NI`` are ``NumPy`` style docstrings with an
unusual indent, and all templates ending with ``G`` are ``Google`` style
docstrings.
"""
# pylint: disable=protected-access

import pytest
import templatest
from templatest import Template, templates

import docsig.messages

from . import (
    CHECK,
    CHECK_ARGS,
    CROSS,
    E10,
    EXPECTED,
    FAIL,
    FAIL_CHECK_ARGS,
    MULTI,
    NAME,
    PASS,
    TEMPLATE,
    InitFileFixtureType,
    MockMainType,
    fail,
    long,
    passed,
)
from ._utils import errors


@pytest.mark.parametrize(
    [NAME, TEMPLATE, "_"],
    templates.registered.filtergroup(MULTI),
    ids=templates.registered.filtergroup(MULTI).getids(),
)
def test_exit_status(
    init_file: InitFileFixtureType,
    main: MockMainType,
    name: str,
    template: str,
    _: str,
) -> None:
    """Test for passing and failing checks.

    All templates prefixed with ``P`` will be tested for zero exit
    status.

    All templates prefixed with ``F`` will be tested for non-zero exit
    status.

    All templates prefixed with ``M`` will be excluded from this test,
    as this tests multiple functions in a file, some that may pass and
    some that may fail.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param name: Name of test.
    :param template: Contents to write to file.
    """
    init_file(template)
    assert main(".", *CHECK_ARGS) == int(name.startswith(FAIL))


@pytest.mark.parametrize(
    ["_", TEMPLATE, EXPECTED],
    templates.registered.filtergroup(MULTI).filtergroup(PASS),
    ids=[
        i.replace("-", "").upper()[4:8] if E10 in i else i
        for i in templates.registered.filtergroup(MULTI)
        .filtergroup(PASS)
        .getids()
    ],
)
def test_stdout(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
    _: str,
    template: str,
    expected: str,
) -> None:
    """Test stdout of failing tests.

    Passing tests will not print to stdout.

    All templates prefixed with ``P`` will be tested for no output.
    As passing templates return an empty str as their expected results,
    this test will confirm that tests that are not meant to pass do not
    include this, as "" will always be True for being in a str object.

    All templates prefixed with ``F`` will be tested for output.

    All templates prefixed with ``M`` will be excluded from this test,
    as this tests multiple functions in a file, some that may produce
    output and some that may not.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param template: String data.
    :param expected: Expected output.
    """
    init_file(template)
    main(".", *CHECK_ARGS)
    std = capsys.readouterr()
    assert expected
    assert expected in std.out


@pytest.mark.parametrize(
    ["_", TEMPLATE, EXPECTED],
    [i for i in templatest.templates.registered if "single-error" in i.name],
    ids=[
        i.replace("-", "").upper()[4:8] if E10 in i else i
        for i in templatest.templates.registered.getids()
        if "single-error" in i
    ],
)
def test_error_codes(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
    _: str,
    template: str,
    expected: str,
) -> None:
    """Test expected error codes are emitted to stdout.

    All templates containing ``SingleError`` are tested for error codes.

    Expected result for these tests are derived from
    ``docsig.messages``.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param template: String data.
    :param expected: Expected output.
    """
    init_file(template)
    messages = [i for i in errors if getattr(docsig.messages, i) != expected]
    main(".")
    std = capsys.readouterr()
    assert std.out.count(expected) == 1
    assert not any(getattr(docsig.messages, i) in std.out for i in messages)


@pytest.mark.parametrize(
    ["_", TEMPLATE, EXPECTED],
    templates.registered.getgroup(MULTI),
    ids=templates.registered.getgroup(MULTI).getids(),
)
def test_multiple(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
    _: str,
    template: str,
    expected: str,
) -> None:
    """Test for correct output for modules with multiple functions.

    Only test templates prefixed with ``M``, as these are designated
    templates containing 2 or more functions. There templates are
    generally excluded from other tests.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param template: Contents to write to file.
    :param expected: Expected result.
    """
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert std.out == expected


@pytest.mark.parametrize(
    [NAME, TEMPLATE, "_"],
    templates.registered.getgroup(fail.e_1_0),
    ids=[
        i.replace("-", "").upper()[4:8]
        for i in templates.registered.getgroup(fail.e_1_0).getids()
    ],
)
def test_disable_rule(
    init_file: InitFileFixtureType,
    main: MockMainType,
    name: str,
    template: str,
    _: str,
) -> None:
    """Test disabling of errors.

    Confirm that templates testing specific error codes, passed as a
    disable argument, do not result in a failed run.

    Any of the tests that would normally raise the particular error
    should pass with the error disabled.

    This test only tests templates prefixed with ``F<ERROR_CODE>``.

    Expected result for these tests are derived from
    ``docsig.messages``.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param name: Name of test.
    :param template: Contents to write to file.
    """
    init_file(template)
    assert main(".", long.disable, name.replace("-", "").upper()[1:5]) == 0


@pytest.mark.parametrize(
    TEMPLATE,
    templates.registered.getgroup(FAIL),
    ids=templates.registered.getgroup(FAIL).getids(),
)
def test_summary(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
    template: Template,
) -> None:
    """Test main for passing and failing checks with ``--summary``.

    Test for the differences and similarities in a standard run where
    the full function diagram is emitted.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param template: Contents to write to file.
    """
    init_file(template.template)
    main(".", *CHECK_ARGS, long.summary)
    std = capsys.readouterr()
    assert CHECK not in std.out
    assert CROSS not in std.out


@pytest.mark.parametrize(
    TEMPLATE,
    templates.registered.getgroup(PASS),
    ids=templates.registered.getgroup(PASS).getids(),
)
def test_no_stdout(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
    template: Template,
) -> None:
    """Test that all tests emit no output.

    Only test templates prefixed with `P` are collected for this test,
    and all tests should pass.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param template: String data.
    """
    init_file(template.template)
    main(".", *CHECK_ARGS)
    std = capsys.readouterr()
    assert not std.out


@pytest.mark.parametrize(
    [NAME, TEMPLATE, EXPECTED],
    templates.registered.filtergroup(MULTI),
    ids=templates.registered.filtergroup(MULTI).getids(),
)
def test_ignore_no_params(  # pylint: disable=too-many-arguments
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
    name: str,
    template: str,
    expected: str,
) -> None:
    """Test that failing funcs pass with `-i/--ignore-no-params` flag.

    ``E103``, ``E105``, ``E109``, and ``H102`` all indicate parameters
    missing from docstring. These should not trigger with this argument.

    All templates prefixed with ``M`` will be excluded from this test,
    as this tests multiple functions in a file, some that may pass and
    some that may fail.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param name: Name of test.
    :param template: String data.
    :param expected: Expected output.
    """
    # messages that indicate missing parameters from docstring, which
    # will not trigger when choosing to ignore docstrings that have no
    # parameters documented (only if docstring has no parameter info)
    missing_messages = (
        docsig.messages.E103,  # parameters missing
        docsig.messages.E105,  # return missing from docstring
        docsig.messages.E109,  # cannot determine whether a return ...
        docsig.messages.H102,  # it is possible a syntax error ...
    )
    parameter_keys = (
        ":param",
        ":return:",
        ":key:",
        ":keyword:",
        "Parameters",
        "Returns",
        "Args:",
        "Returns:",
    )
    init_file(template)
    returncode = main(".", *CHECK_ARGS, long.ignore_no_params)
    std = capsys.readouterr()

    # expected result one of the messages indicating missing params
    # does not include any strings indicating that params are documented
    # output should be none and the should result with a zero exit
    # status
    no_params = (
        expected in missing_messages
        and (
            not any(i in template for i in parameter_keys)
            # these tests have no :param: in the class docstring
            # but do in the __init__ docstring, which breaks
            # the above check within the template
            or "w-class-constructor" in name
        )
        and returncode == 0
    )
    assert expected in std.out or no_params


@pytest.mark.parametrize(
    TEMPLATE,
    templates.registered.getgroup(passed.property_return),
    ids=templates.registered.getgroup(passed.property_return).getids(),
)
def test_no_check_property_returns_flag(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
    template: Template,
) -> None:
    """Test that passing property fails without ``-P`` flag.

    Only test templates prefixed with ``PProperty`` are collected for
    this test, and all tests should fail.

    All tests will be tested for ``E108`` and ``H101``, which property
    related errors.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param template: Contents to write to file.
    """
    init_file(template.template)
    main(".")
    std = capsys.readouterr()
    assert docsig.messages.E108 in std.out
    assert docsig.messages.H101 in std.out


@pytest.mark.parametrize(
    [NAME, TEMPLATE, "_"],
    templates.registered.filtergroup(MULTI),
    ids=templates.registered.filtergroup(MULTI).getids(),
)
def test_ignore_args(
    init_file: InitFileFixtureType,
    main: MockMainType,
    name: str,
    template: str,
    _: str,
) -> None:
    """Test that for passing/failing tests with ``-a/--ignore-args``.

    Test that docs without args, where the signature contains args,
    don’t fail with ``-a/--ignore-args``.

    All templates containing args in their signature must have `WArgs` in
    their name.

    Passing templates with ``WArgs`` will fail and failing tests with
    ``WArgs`` will pass, as tests which pass will have args documented,
    which shouldn’t be to pass with this check. All other tests will
    have the usual result.

    All templates prefixed with ``M`` will be excluded from this test,
    as this tests multiple functions in a file, some that may pass and
    some that may fail.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param name: Name of test.
    :param template: Contents to write to file.
    """
    file = init_file(template)
    assert main(*CHECK_ARGS, long.ignore_args, file.parent) == int(
        name.startswith(FAIL)
        and "w-args" not in name
        or name.startswith(PASS)
        and "w-args" in name
    )


@pytest.mark.parametrize(
    [NAME, TEMPLATE, "_"],
    templates.registered.filtergroup(MULTI),
    ids=templates.registered.filtergroup(MULTI).getids(),
)
def test_ignore_kwargs(
    init_file: InitFileFixtureType,
    main: MockMainType,
    name: str,
    template: str,
    _: str,
) -> None:
    """Test that for passing/failing tests with ``-k/--ignore-kwargs``.

    Test that docs without args, where the signature contains args,
    don’t fail with ``-k/--ignore-kwargs``.

    All templates containing args in their signature must have
    ``WKwargs`` their name.

    Passing templates with ``WKwargs`` will fail and failing tests with
    ``WKwargs`` will pass, as tests which pass will have args documented,
    which shouldn’t be to pass with this check. All other tests will
    have the usual result.

    All templates prefixed with ``M`` will be excluded from this test,
    as this tests multiple functions in a file, some that may pass and
    some that may fail.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param name: Name of test.
    :param template: Contents to write to file.
    """
    file = init_file(template)
    assert main(*CHECK_ARGS, long.ignore_kwargs, file.parent) == int(
        name.startswith(FAIL)
        and "w-kwargs" not in name
        or name.startswith(PASS)
        and "w-kwargs" in name
    )


@pytest.mark.parametrize(
    TEMPLATE,
    templates.registered.getgroup(*FAIL_CHECK_ARGS),
    ids=templates.registered.getgroup(*FAIL_CHECK_ARGS).getids(),
)
def test_no_flag(
    init_file: InitFileFixtureType, main: MockMainType, template: Template
) -> None:
    """Test that failing tests pass without their corresponding flag.

    All tests that fail such as with ``--check-class`` should be
    prefixed with ``FClass``, and these particular tests should all
    pass.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param template: Contents to write to file.
    """
    init_file(template.template)
    assert main(".") == 0


@pytest.mark.parametrize(
    [NAME, TEMPLATE, "_"],
    templates.registered.getgroup(*FAIL_CHECK_ARGS),
    ids=templates.registered.getgroup(*FAIL_CHECK_ARGS).getids(),
)
def test_single_flag(
    init_file: InitFileFixtureType,
    main: MockMainType,
    name: str,
    template: str,
    _: str,
) -> None:
    """Test that failing templates pass with only corresponding flag.

    This tests that boolean expressions are all evaluated properly on
    their own.

    All tests that fail such as with `--check-class` should be prefixed
    with `FClass`, and these particular tests should all fail.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param name: Name of test.
    :param template: Contents to write to file.
    """
    init_file(template)
    assert main(".", f"--check-{name.split('-')[1]}") == 1


@pytest.mark.parametrize(
    [NAME, TEMPLATE, "_"],
    templates.registered.getgroup("f-w-class-constructor"),
    ids=templates.registered.getgroup("f-w-class-constructor").getids(),
)
def test_check_class_constructor(
    init_file: InitFileFixtureType,
    main: MockMainType,
    name: str,
    template: str,
    _: str,
) -> None:
    """Test behaviour of ``--check-class-constructor``.

    These tests all fail under the default setup with ``--check-class``,
    because they are missing parameters from the ``__init__`` under that
    regime.

    Tests that should fail when checked with ``--check-class-constructor`` have
    an 'F' just before the final part of the name relating to the docstring
    style. Otherwise, the test should pass.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param name: Name of test.
    :param template: Contents to write to file.
    """
    init_file(template)
    # exclude --check-class from CHECK_ARGS, because this is
    # mutually incompatible with --check-class-constructor
    assert main(".", *CHECK_ARGS[1:], "--check-class-constructor") == int(
        name[: name.rindex("-")].endswith(FAIL)
    )


@pytest.mark.parametrize(
    [NAME, TEMPLATE, EXPECTED],
    templates.registered.filtergroup(MULTI).filtergroup(fail.method_header),
    ids=[
        i.replace("-", "").upper()[4:8] if E10 in i else i
        for i in templates.registered.filtergroup(MULTI)
        .filtergroup(fail.method_header)
        .getids()
    ],
)
def test_string_argument(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    name: str,
    template: str,
    expected: str,
) -> None:
    """Test for passing and failing checks with ``-s/--string``.

    A combination of the test for exit status and the test for stdout.
    As this test could be done for every single test where the file is
    checked, without the ``-s/--string`` argument and with the path
    positional argument, this will only test those two. As long as the
    tests pass and are consistent with the result that the tests for a
    file produce, this test should be enough.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    :param name: Name of test.
    :param template: String data.
    :param expected: Expected output.
    """
    assert main(".", *CHECK_ARGS, long.string, template) == int(
        name.startswith(FAIL)
    )
    std = capsys.readouterr()
    assert expected in std.out
