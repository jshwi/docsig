"""
tests._test
===========
"""
# pylint: disable=protected-access
from pathlib import Path

import pytest
import templatest
import tomli_w
from templatest import Template, templates

import docsig.messages

from . import (
    CHECK,
    CROSS,
    E10,
    ERR_GROUP,
    FAIL,
    FAIL_OVERRIDE,
    FAIL_PROTECT,
    MULTI,
    NAME,
    PASS,
    TEMPLATE,
    InitFileFixtureType,
    MockMainType,
    long,
    short,
)
from ._utils import DummyFunc, NoColorCapsys, errors, hints


@pytest.mark.parametrize("arg", (short.v, long.version))
def test_print_version(
    monkeypatch: pytest.MonkeyPatch,
    main: MockMainType,
    nocolorcapsys: NoColorCapsys,
    arg: str,
) -> None:
    """Test printing of version on commandline.

    :param monkeypatch: Mock patch environment and attributes.
    :param main: Patch package entry point.
    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    :param arg: Version argument.
    """
    monkeypatch.setattr("docsig._config.__version__", "1.0.0")
    with pytest.raises(SystemExit):
        main(arg)

    assert nocolorcapsys.stdout().strip() == "1.0.0"


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
    file = init_file(template)
    assert main(
        long.check_class,
        long.check_protected,
        long.check_overridden,
        long.check_dunders,
        long.check_property_returns,
        file.parent,
    ) == int(name.startswith(FAIL))


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
    init_file: InitFileFixtureType,
    main: MockMainType,
    nocolorcapsys: NoColorCapsys,
    template: Template,
) -> None:
    """Test main for stdout.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    :param template: String data.
    """
    file = init_file(template.template)
    main(
        long.check_class,
        long.check_protected,
        long.check_dunders,
        long.check_overridden,
        long.check_property_returns,
        file.parent,
    )
    assert template.expected != ""
    assert template.expected in nocolorcapsys.readouterr()[0]


def test_no_params(init_file: InitFileFixtureType, main: MockMainType) -> None:
    """Test main for function without params.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    contents = templates.registered.getbyname("p-no-params-s").template
    file = init_file(contents)
    with pytest.warns(None) as record:  # type: ignore
        main(file.parent)

    assert len(record) == 0


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
    init_file: InitFileFixtureType,
    main: MockMainType,
    nocolorcapsys: NoColorCapsys,
    template: Template,
) -> None:
    """Test main for stdout.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    :param template: String data.
    """
    file = init_file(template.template)
    messages = [
        i for i in errors if getattr(docsig.messages, i) != template.expected
    ]
    main(file.parent)
    out = nocolorcapsys.readouterr()[0]
    assert template.expected in out
    assert out.count(template.expected) == 1
    for message in messages:
        assert not getattr(docsig.messages, message) in out


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
    init_file: InitFileFixtureType,
    main: MockMainType,
    nocolorcapsys: NoColorCapsys,
    expected: str,
) -> None:
    """Test output correct for modules with multiple funcs.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    :param expected: Expected result.
    """
    file = init_file(templates.registered.getgroup(MULTI)[0].template)
    main(file.parent)
    out = nocolorcapsys.readouterr()[0]
    # all_expected = expected.split("\n\n\n")
    assert expected in out


def test_mutable_sequence() -> None:
    """Get coverage on ``MutableSequence``."""
    report = docsig._report.Report(DummyFunc(), [], [], False)  # type: ignore
    report.append(errors[0])
    assert getattr(docsig.messages, errors[0]) in report
    assert len(report) == 1
    report[0] = errors[1]
    report.pop()
    assert errors[1] not in report


def test_message_sequence() -> None:
    """Test disabling of error messages.

    Assert that all following hints are disabled, until a new error
    message that has not been disabled is appended to the sequence.
    """
    # noinspection PyUnresolvedReferences
    msg_seq = docsig._report._MessageSequence(disable=[errors[0]])
    msg_seq.append(errors[0])
    msg_seq.append(hints[0])
    msg_seq.append(hints[1])
    assert getattr(docsig.messages, errors[0]) not in msg_seq
    assert getattr(docsig.messages, hints[1]) not in msg_seq
    assert getattr(docsig.messages, hints[1]) not in msg_seq
    msg_seq.append(errors[1])
    msg_seq.append(hints[0])
    msg_seq.append(hints[1])
    assert getattr(docsig.messages, errors[1]) in msg_seq
    assert getattr(docsig.messages, hints[0]) in msg_seq
    assert getattr(docsig.messages, hints[1]) in msg_seq


@pytest.mark.parametrize(
    [NAME, TEMPLATE, "_"],
    templates.registered.getgroup(ERR_GROUP),
    ids=[
        i.replace("-", "").upper()[4:8]
        for i in templates.registered.getgroup(ERR_GROUP).getids()
    ],
)
def test_main_toml_disable(
    tmp_path: Path,
    init_file: InitFileFixtureType,
    main: MockMainType,
    name: str,
    template: str,
    _: str,
) -> None:
    """Test main for disabling errors via pyproject.toml file.

    :param tmp_path: Create and return temporary directory.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param name: Name of test.
    :param template: Contents to write to file.
    """
    pyproject_file = tmp_path / "pyproject.toml"
    pyproject_obj = {
        "tool": {
            docsig.__name__: {"disable": [name.replace("-", "").upper()[1:5]]}
        }
    }
    init_file(template)
    pyproject_file.write_text(tomli_w.dumps(pyproject_obj))
    assert main(".") == 0


@pytest.mark.parametrize(
    [NAME, TEMPLATE, "_"],
    templates.registered.getgroup(ERR_GROUP),
    ids=[
        i.replace("-", "").upper()[4:8]
        for i in templates.registered.getgroup(ERR_GROUP).getids()
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
    assert main(".", "--disable", name.replace("-", "").upper()[1:5]) == 0


@pytest.mark.parametrize("message", errors)
def test_target_report(message: str) -> None:
    """Test report only adds the target error provided.

    :param message: Error message code.
    """
    # noinspection PyUnresolvedReferences
    report = docsig._report.Report(
        DummyFunc(),  # type: ignore
        targets=[message],
        disable=[],
        check_property_returns=False,
    )
    report.extend(errors)
    assert getattr(docsig.messages, message) in report
    assert len(report) == 1


@pytest.mark.parametrize("message", errors)
def test_disable_report(message: str) -> None:
    """Test report adds all errors provided except for the disabled one.

    :param message: Error message code.
    """
    # noinspection PyUnresolvedReferences
    report = docsig._report.Report(
        DummyFunc(),  # type: ignore
        targets=[],
        disable=[message],
        check_property_returns=False,
    )
    report.extend(errors)
    assert getattr(docsig.messages, message) not in report
    assert len(report) == len(errors) - 1


def test_lineno(
    init_file: InitFileFixtureType,
    main: MockMainType,
    nocolorcapsys: NoColorCapsys,
) -> None:
    """Test printing of three function errors with line number.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    """
    init_file(templates.registered.getbyname("m-fail-s").template)
    main(".")
    out = nocolorcapsys.stdout()
    assert "module/file.py:2" in out
    assert "module/file.py:11" in out
    assert "module/file.py:19" in out


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
    assert main(
        long.check_class,
        long.check_protected,
        long.check_overridden,
        long.check_dunders,
        long.check_property_returns,
        long.string,
        template,
    ) == int(name.startswith(FAIL))


@pytest.mark.parametrize(
    TEMPLATE,
    templates.registered.filtergroup(MULTI).filtergroup("f-class-header"),
    ids=[
        i.replace("-", "").upper()[4:8] if E10 in i else i
        for i in templates.registered.filtergroup(MULTI)
        .filtergroup("f-class-header")
        .getids()
    ],
)
def test_main_str_out(
    main: MockMainType, nocolorcapsys: NoColorCapsys, template: Template
) -> None:
    """Test main for stdout with strings.

    :param main: Mock ``main`` function.
    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    :param template: String data.
    """
    main(
        long.check_class,
        long.check_dunders,
        long.check_protected,
        long.check_overridden,
        long.check_property_returns,
        long.string,
        template.template,
    )
    assert template.expected in nocolorcapsys.readouterr()[0]


def test_no_check_init_flag(
    init_file: InitFileFixtureType,
    main: MockMainType,
    nocolorcapsys: NoColorCapsys,
) -> None:
    """Test that failing class passes without ``--check-init`` flag.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    """
    template = templates.registered.getbyname("f-init-s")
    file = init_file(template.template)
    assert main(file.parent) == 0
    assert not nocolorcapsys.stdout()


@pytest.mark.parametrize(
    ["_", TEMPLATE, "__"],
    templates.registered.getgroup(FAIL_PROTECT),
    ids=templates.registered.getgroup(FAIL_PROTECT).getids(),
)
def test_no_check_protected_flag(
    init_file: InitFileFixtureType,
    main: MockMainType,
    nocolorcapsys: NoColorCapsys,
    _: str,
    template: str,
    __: str,
) -> None:
    """Test that failing func passes without ``--check-protected`` flag.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    :param template: Contents to write to file.
    """
    file = init_file(template)
    assert main(file.parent) == 0
    assert not nocolorcapsys.stdout()


def test_only_init_flag(
    init_file: InitFileFixtureType, main: MockMainType
) -> None:
    """Test that failing class passes with only ``--check-init`` flag.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = templates.registered.getbyname("f-init-s")
    file = init_file(template.template)
    assert main(long.check_class, file.parent) == 1


@pytest.mark.parametrize(
    ["_", TEMPLATE, "__"],
    templates.registered.getgroup(FAIL_PROTECT),
    ids=templates.registered.getgroup(FAIL_PROTECT).getids(),
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
    file = init_file(template)
    assert main(long.check_protected, file.parent) == 1


@pytest.mark.parametrize(
    ["_", TEMPLATE, "__"],
    templates.registered.getgroup(FAIL_OVERRIDE),
    ids=templates.registered.getgroup(FAIL_OVERRIDE).getids(),
)
def test_no_check_overridden_flag(
    init_file: InitFileFixtureType,
    main: MockMainType,
    nocolorcapsys: NoColorCapsys,
    _: str,
    template: str,
    __: str,
) -> None:
    """Test that failing func passes without ``--check-overridden``.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    :param template: Contents to write to file.
    """
    file = init_file(template)
    assert main(file.parent) == 0
    assert not nocolorcapsys.stdout()


@pytest.mark.parametrize(
    ["_", TEMPLATE, "__"],
    templates.registered.getgroup(FAIL_OVERRIDE),
    ids=templates.registered.getgroup(FAIL_OVERRIDE).getids(),
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
    file = init_file(template)
    assert main(long.check_overridden, file.parent) == 1


@pytest.mark.parametrize(
    ["_", TEMPLATE, "__"],
    templates.registered.getgroup("f-dunder"),
    ids=templates.registered.getgroup("f-dunder").getids(),
)
def test_no_check_dunder_flag(
    init_file: InitFileFixtureType,
    main: MockMainType,
    nocolorcapsys: NoColorCapsys,
    _: str,
    template: str,
    __: str,
) -> None:
    """Test that failing func passes without ``--check-dunders`` flag.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    :param template: Contents to write to file.
    """
    file = init_file(template)
    assert main(file.parent) == 0
    assert not nocolorcapsys.stdout()


def test_mutable_mapping() -> None:
    """Get coverage on ``MutableMapping``."""
    mapping = docsig._objects.MutableMapping()  # type: ignore
    assert len(mapping) == 0
    mapping[1] = 1
    assert 1 in mapping
    assert mapping[1] == 1
    assert len(mapping) == 1
    del mapping[1]
    assert len(mapping) == 0


@pytest.mark.parametrize(
    ["_", TEMPLATE, "__"],
    templates.registered.getgroup(FAIL),
    ids=templates.registered.getgroup(FAIL).getids(),
)
def test_main_sum(
    init_file: InitFileFixtureType,
    main: MockMainType,
    nocolorcapsys: NoColorCapsys,
    _: str,
    template: str,
    __: str,
) -> None:
    """Test main for passing and failing checks with ``--summary``.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    :param template: Contents to write to file.
    """
    file = init_file(template)
    assert (
        main(
            long.summary,
            long.check_class,
            long.check_protected,
            long.check_overridden,
            long.check_dunders,
            long.check_property_returns,
            file.parent,
        )
        == 1
    )
    out = nocolorcapsys.stdout()
    assert CHECK not in out
    assert CROSS not in out


@pytest.mark.parametrize(
    ["_", TEMPLATE, "__"],
    templates.registered.getgroup(FAIL),
    ids=templates.registered.getgroup(FAIL).getids(),
)
def test_no_ansi(
    init_file: InitFileFixtureType,
    main: MockMainType,
    capsys: pytest.CaptureFixture,
    _: str,
    template: str,
    __: str,
) -> None:
    """Test main for failing checks with the ``--no-ansi`` flag.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param capsys: Capture and return stdout and stderr stream.
    :param template: Contents to write to file.
    """
    file = init_file(template)
    assert (
        main(
            long.no_ansi,
            long.check_class,
            long.check_protected,
            long.check_overridden,
            long.check_dunders,
            long.check_property_returns,
            file.parent,
        )
        == 1
    )
    assert "\x1b" not in capsys.readouterr()[0]


@pytest.mark.parametrize(
    TEMPLATE,
    templates.registered.getgroup(PASS),
    ids=templates.registered.getgroup(PASS).getids(),
)
def test_main_output_positive(
    init_file: InitFileFixtureType,
    main: MockMainType,
    nocolorcapsys: NoColorCapsys,
    template: Template,
) -> None:
    """Test main for stdout.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    :param template: String data.
    """
    file = init_file(template.template)
    main(
        long.check_class,
        long.check_protected,
        long.check_dunders,
        long.check_overridden,
        long.check_property_returns,
        file.parent,
    )
    assert template.expected == nocolorcapsys.readouterr()[0]


def test_param_ne() -> None:
    """Get coverage on `Param.__eq__`."""
    # noinspection PyUnresolvedReferences
    assert docsig._function.Param() != object


@pytest.mark.parametrize(
    ["_", TEMPLATE, "expected"],
    templates.registered.filtergroup(MULTI),
    ids=templates.registered.filtergroup(MULTI).getids(),
)
def test_ignore_no_params(
    init_file: InitFileFixtureType,
    main: MockMainType,
    nocolorcapsys: NoColorCapsys,
    _: str,
    template: str,
    expected: str,
) -> None:
    """Test that failing func passes with ``--ignore-no-params`` flag.

    `E103`, `E105`, `109`, and `H102` all indicate parameters missing
    from docstring. These should not trigger with this argument.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
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
    file = init_file(template)
    returncode = main(
        long.check_class,
        long.check_protected,
        long.check_dunders,
        long.check_overridden,
        long.ignore_no_params,
        file.parent,
    )
    out = nocolorcapsys.readouterr()[0]

    # expected result one of the messages indicating missing params
    # does not include any strings indicating that params are documented
    # output should be none and the should result with a zero exit
    # status
    no_params = (
        expected in missing_messages
        and not any(i in template for i in parameter_keys)
        and out == ""
        and returncode == 0
    )
    assert expected in out or no_params


@pytest.mark.parametrize(
    ["_", TEMPLATE, "__"],
    templates.registered.getgroup("f-property-no-return"),
    ids=templates.registered.getgroup("f-property-no-return").getids(),
)
def test_no_check_property_returns_flag_wo(
    init_file: InitFileFixtureType,
    main: MockMainType,
    nocolorcapsys: NoColorCapsys,
    _: str,
    template: str,
    __: str,
) -> None:
    """Test that failing property passes without ``-P`` flag.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    :param template: Contents to write to file.
    """
    file = init_file(template)
    assert main(file.parent) == 0
    assert not nocolorcapsys.stdout()


@pytest.mark.parametrize(
    ["_", TEMPLATE, "__"],
    templates.registered.getgroup("p-property-return"),
    ids=templates.registered.getgroup("p-property-return").getids(),
)
def test_no_check_property_returns_flag_w(
    init_file: InitFileFixtureType,
    main: MockMainType,
    nocolorcapsys: NoColorCapsys,
    _: str,
    template: str,
    __: str,
) -> None:
    """Test that passing property fails without ``-P`` flag.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    :param template: Contents to write to file.
    """
    file = init_file(template)
    assert main(file.parent) == 1
    out = nocolorcapsys.stdout()
    assert docsig.messages.E108 in out
    assert docsig.messages.H101 in out


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
    """Test docstrings without args don't fail wih ``-a/--ignore_args``.

    Passing tests will fail and failing tests will pass, as tests which
    generally pass will have args documented, which shouldn't be with
    this argument.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param name: Name of test.
    :param template: Contents to write to file.
    """
    file = init_file(template)
    assert main(
        long.check_class,
        long.check_protected,
        long.check_overridden,
        long.check_dunders,
        long.check_property_returns,
        long.ignore_args,
        file.parent,
    ) == int(
        name.startswith(FAIL)
        and "w-args" not in name
        or name.startswith(PASS)
        and "w-args" in name
    )
