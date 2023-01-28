"""
tests._test
===========
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
    FAIL,
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
def test_main_args(
    init_file: InitFileFixtureType,
    main: MockMainType,
    name: str,
    template: str,
    _: str,
) -> None:
    """Test main for passing and failing checks.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param name: Name of test.
    :param template: Contents to write to file.
    """
    init_file(template)
    assert main(*CHECK_ARGS) == int(name.startswith(FAIL))


@pytest.mark.parametrize(
    TEMPLATE,
    templates.registered.filtergroup(MULTI).filtergroup(PASS),
    ids=[
        i.replace("-", "").upper()[4:8] if E10 in i else i
        for i in templates.registered.filtergroup(MULTI)
        .filtergroup(PASS)
        .getids()
    ],
)
def test_main_output_negative(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
    template: Template,
) -> None:
    """Test main for stdout.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param template: String data.
    """
    init_file(template.template)
    main(*CHECK_ARGS)
    std = capsys.readouterr()
    assert template.expected
    assert template.expected in std.out


@pytest.mark.parametrize(
    TEMPLATE,
    [i for i in templatest.templates.registered if i.name.endswith("1-sum-s")],
    ids=[
        i.replace("-", "").upper()[4:8] if E10 in i else i
        for i in templatest.templates.registered.getids()
        if i.endswith("1-sum-s")
    ],
)
def test_main_no_sum(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
    template: Template,
) -> None:
    """Test main for stdout.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param template: String data.
    """
    init_file(template.template)
    messages = [
        i for i in errors if getattr(docsig.messages, i) != template.expected
    ]
    main()
    std = capsys.readouterr()
    assert template.expected in std.out
    assert std.out.count(template.expected) == 1
    assert not any(getattr(docsig.messages, i) in std.out for i in messages)


@pytest.mark.parametrize(
    "expected",
    templates.registered.getgroup(MULTI)[0].expected.split("\n\n\n"),
    ids=(
        c
        for c, _ in enumerate(
            templates.registered.getgroup(MULTI)[0].expected.split("\n\n\n")
        )
    ),
)
def test_main_multi(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
    expected: str,
) -> None:
    """Test output correct for modules with multiple funcs.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param expected: Expected result.
    """
    init_file(templates.registered.getgroup(MULTI)[0].template)
    main()
    std = capsys.readouterr()
    assert expected in std.out


@pytest.mark.parametrize(
    [NAME, TEMPLATE, "_"],
    templates.registered.getgroup(fail.e_1_0),
    ids=[
        i.replace("-", "").upper()[4:8]
        for i in templates.registered.getgroup(fail.e_1_0).getids()
    ],
)
def test_main_cli_disable(
    init_file: InitFileFixtureType,
    main: MockMainType,
    name: str,
    template: str,
    _: str,
) -> None:
    """Test main for disabling errors via the commandline.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param name: Name of test.
    :param template: Contents to write to file.
    """
    init_file(template)
    assert main(long.disable, name.replace("-", "").upper()[1:5]) == 0


@pytest.mark.parametrize(
    [NAME, TEMPLATE, "_"],
    templates.registered.filtergroup(MULTI),
    ids=templates.registered.filtergroup(MULTI).getids(),
)
def test_main_str(
    main: MockMainType, name: str, template: str, _: str
) -> None:
    """Test main for passing and failing checks with strings.

    :param main: Mock ``main`` function.
    :param name: Name of test.
    :param template: Contents to write to file.
    """
    assert main(*CHECK_ARGS, long.string, template) == int(
        name.startswith(FAIL)
    )


@pytest.mark.parametrize(
    TEMPLATE,
    templates.registered.filtergroup(MULTI).filtergroup(fail.method_header),
    ids=[
        i.replace("-", "").upper()[4:8] if E10 in i else i
        for i in templates.registered.filtergroup(MULTI)
        .filtergroup(fail.method_header)
        .getids()
    ],
)
def test_main_str_out(
    capsys: pytest.CaptureFixture, main: MockMainType, template: Template
) -> None:
    """Test main for stdout with strings.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    :param template: String data.
    """
    main(*CHECK_ARGS, long.string, template.template)
    std = capsys.readouterr()
    assert template.expected in std.out


def test_no_check_init_flag(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
) -> None:
    """Test that failing class passes without ``--check-init`` flag.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = templates.registered.getbyname(fail.class_s)
    init_file(template.template)
    assert main() == 0
    std = capsys.readouterr()
    assert not std.out


@pytest.mark.parametrize(
    ["_", TEMPLATE, "__"],
    templates.registered.getgroup(fail.protect),
    ids=templates.registered.getgroup(fail.protect).getids(),
)
def test_no_check_protected_flag(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
    _: str,
    template: str,
    __: str,
) -> None:
    """Test that failing func passes without ``--check-protected`` flag.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param template: Contents to write to file.
    """
    init_file(template)
    assert main() == 0
    std = capsys.readouterr()
    assert not std.out


def test_only_init_flag(
    init_file: InitFileFixtureType, main: MockMainType
) -> None:
    """Test that failing class passes with only ``--check-init`` flag.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = templates.registered.getbyname(fail.class_s)
    init_file(template.template)
    assert main(long.check_class) == 1


@pytest.mark.parametrize(
    ["_", TEMPLATE, "__"],
    templates.registered.getgroup(fail.protect),
    ids=templates.registered.getgroup(fail.protect).getids(),
)
def test_only_protected_flag(
    init_file: InitFileFixtureType,
    main: MockMainType,
    _: str,
    template: str,
    __: str,
) -> None:
    """Test that failing func passes with only ``--check-protected``.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param template: Contents to write to file.
    """
    init_file(template)
    assert main(long.check_protected) == 1


@pytest.mark.parametrize(
    ["_", TEMPLATE, "__"],
    templates.registered.getgroup(fail.overridden),
    ids=templates.registered.getgroup(fail.overridden).getids(),
)
def test_no_check_overridden_flag(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
    _: str,
    template: str,
    __: str,
) -> None:
    """Test that failing func passes without ``--check-overridden``.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param template: Contents to write to file.
    """
    init_file(template)
    assert main() == 0
    std = capsys.readouterr()
    assert not std.out


@pytest.mark.parametrize(
    ["_", TEMPLATE, "__"],
    templates.registered.getgroup(fail.overridden),
    ids=templates.registered.getgroup(fail.overridden).getids(),
)
def test_only_overridden_flag(
    init_file: InitFileFixtureType,
    main: MockMainType,
    _: str,
    template: str,
    __: str,
) -> None:
    """Test that failing func passes with only ``--check-overridden``.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param template: Contents to write to file.
    """
    init_file(template)
    assert main(long.check_overridden) == 1


@pytest.mark.parametrize(
    ["_", TEMPLATE, "__"],
    templates.registered.getgroup(fail.dunder),
    ids=templates.registered.getgroup(fail.dunder).getids(),
)
def test_no_check_dunder_flag(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
    _: str,
    template: str,
    __: str,
) -> None:
    """Test that failing func passes without ``--check-dunders`` flag.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param template: Contents to write to file.
    """
    init_file(template)
    assert main() == 0
    std = capsys.readouterr()
    assert not std.out


@pytest.mark.parametrize(
    ["_", TEMPLATE, "__"],
    templates.registered.getgroup(FAIL),
    ids=templates.registered.getgroup(FAIL).getids(),
)
def test_main_sum(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
    _: str,
    template: str,
    __: str,
) -> None:
    """Test main for passing and failing checks with ``--summary``.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param template: Contents to write to file.
    """
    init_file(template)
    assert main(*CHECK_ARGS, long.summary) == 1
    std = capsys.readouterr()
    assert CHECK not in std.out
    assert CROSS not in std.out


@pytest.mark.parametrize(
    TEMPLATE,
    templates.registered.getgroup(PASS),
    ids=templates.registered.getgroup(PASS).getids(),
)
def test_main_output_positive(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
    template: Template,
) -> None:
    """Test main for stdout.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param template: String data.
    """
    init_file(template.template)
    main(*CHECK_ARGS)
    std = capsys.readouterr()
    assert template.expected == std.out


@pytest.mark.parametrize(
    ["_", TEMPLATE, "expected"],
    templates.registered.filtergroup(MULTI),
    ids=templates.registered.filtergroup(MULTI).getids(),
)
def test_ignore_no_params(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
    _: str,
    template: str,
    expected: str,
) -> None:
    """Test that failing func passes with ``--ignore-no-params`` flag.

    `E103`, `E105`, `109`, and `H102` all indicate parameters missing
    from docstring. These should not trigger with this argument.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
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
    returncode = main(*CHECK_ARGS, long.ignore_no_params)
    std = capsys.readouterr()

    # expected result one of the messages indicating missing params
    # does not include any strings indicating that params are documented
    # output should be none and the should result with a zero exit
    # status
    no_params = (
        expected in missing_messages
        and not any(i in template for i in parameter_keys)
        and std.out == ""
        and returncode == 0
    )
    assert expected in std.out or no_params


@pytest.mark.parametrize(
    ["_", TEMPLATE, "__"],
    templates.registered.getgroup(fail.property_returns),
    ids=templates.registered.getgroup(fail.property_returns).getids(),
)
def test_no_check_property_returns_flag_wo(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
    _: str,
    template: str,
    __: str,
) -> None:
    """Test that failing property passes without ``-P`` flag.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param template: Contents to write to file.
    """
    init_file(template)
    assert main() == 0
    std = capsys.readouterr()
    assert not std.out


@pytest.mark.parametrize(
    ["_", TEMPLATE, "__"],
    templates.registered.getgroup(passed.property_return),
    ids=templates.registered.getgroup(passed.property_return).getids(),
)
def test_no_check_property_returns_flag_w(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
    _: str,
    template: str,
    __: str,
) -> None:
    """Test that passing property fails without ``-P`` flag.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param template: Contents to write to file.
    """
    init_file(template)
    assert main() == 1
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
    """Test docs without args don't fail with ``-a/--ignore_args``.

    Passing tests will fail and failing tests will pass, as tests which
    generally pass will have args documented, which shouldn't be with
    this argument.

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
    """Test docstrings without kwargs don't fail with ``-k``.

    Passing tests will fail and failing tests will pass, as tests which
    generally pass will have kwargs documented, which shouldn't be with
    this argument.

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
