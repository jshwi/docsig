"""
tests._test
===========
"""
# pylint: disable=protected-access,too-many-arguments
import typing as t
from pathlib import Path

import pytest
import templatest
import tomli_w
from templatest import Template, templates

import docsig.messages

from . import (
    CHECK,
    CHECK_CLASS,
    CHECK_DUNDERS,
    CHECK_OVERRIDDEN,
    CHECK_PROTECTED,
    CROSS,
    E10,
    ERR_GROUP,
    FAIL,
    FAIL_OVERRIDE,
    FAIL_PROTECT,
    FUNC,
    MULTI,
    NAME,
    TEMPLATE,
    InitFileFixtureType,
    MockMainType,
)
from ._utils import NoColorCapsys, errors, hints


@pytest.mark.parametrize("arg", ("-v", "--version"))
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
        CHECK_CLASS,
        CHECK_PROTECTED,
        CHECK_OVERRIDDEN,
        CHECK_DUNDERS,
        file.parent,
    ) == int(name.startswith(FAIL))


@pytest.mark.parametrize(
    TEMPLATE,
    templates.registered.filtergroup(MULTI),
    ids=[
        i.replace("-", "").upper()[4:8] if E10 in i else i
        for i in templates.registered.filtergroup(MULTI).getids()
    ],
)
def test_main_output(
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
        CHECK_CLASS,
        CHECK_PROTECTED,
        CHECK_DUNDERS,
        CHECK_OVERRIDDEN,
        file.parent,
    )
    assert template.expected in nocolorcapsys.readouterr()[0]


def test_no_params(init_file: InitFileFixtureType, main: MockMainType) -> None:
    """Test main for function without params.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    contents = templates.registered.getbyname("pass-no-params").template
    file = init_file(contents)
    with pytest.warns(None) as record:  # type: ignore
        main(file.parent)

    assert len(record) == 0


@pytest.mark.parametrize(
    TEMPLATE,
    [i for i in templatest.templates.registered if i.name.endswith("1-sum")],
    ids=[
        i.replace("-", "").upper()[4:8] if E10 in i else i
        for i in templatest.templates.registered.getids()
        if i.endswith("1-sum")
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
    report = docsig._report.Report(FUNC, [], [])  # type: ignore
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
            docsig.__name__: {"disable": [name.replace("-", "").upper()[4:8]]}
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
    assert main(".", "--disable", name.replace("-", "").upper()[4:8]) == 0


def test_main_cli_command_separated_list(
    monkeypatch: pytest.MonkeyPatch, main: MockMainType
) -> None:
    """Test main for disabling errors via the commandline.

    :param monkeypatch: Mock patch environment and attributes.
    :param main: Mock ``main`` function.
    """
    instance = []

    # noinspection PyUnresolvedReferences
    def _parser(_: t.Any) -> docsig._config.Parser:
        parser = docsig._config.Parser({})
        instance.append(parser)
        return parser

    monkeypatch.setattr("docsig._main._Parser", _parser)
    main(
        ".",
        "--disable",
        "{},{},{},{},{},{},{},{}".format(
            errors[0],
            errors[1],
            errors[2],
            errors[3],
            errors[4],
            errors[5],
            errors[6],
            errors[7],
        ),
    )
    assert instance[0].args.disable == [
        errors[0],
        errors[1],
        errors[2],
        errors[3],
        errors[4],
        errors[5],
        errors[6],
        errors[7],
    ]


@pytest.mark.parametrize("message", errors)
def test_target_report(message: str) -> None:
    """Test report only adds the target error provided.

    :param message: Error message code.
    """
    # noinspection PyUnresolvedReferences
    report = docsig._report.Report(
        FUNC, targets=[message], disable=[]  # type: ignore
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
        FUNC, targets=[], disable=[message]  # type: ignore
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
    init_file(templates.registered.getbyname("multi-fail").template)
    main(".")
    out = nocolorcapsys.stdout()
    assert "module/file.py::2" in out
    assert "module/file.py::11" in out
    assert "module/file.py::19" in out


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
        CHECK_CLASS,
        CHECK_PROTECTED,
        CHECK_OVERRIDDEN,
        CHECK_DUNDERS,
        "--string",
        template,
    ) == int(name.startswith(FAIL))


@pytest.mark.parametrize(
    TEMPLATE,
    templates.registered.filtergroup(MULTI).filtergroup("fail-class-header"),
    ids=[
        i.replace("-", "").upper()[4:8] if E10 in i else i
        for i in templates.registered.filtergroup(MULTI)
        .filtergroup("fail-class-header")
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
        CHECK_CLASS,
        CHECK_DUNDERS,
        CHECK_PROTECTED,
        CHECK_OVERRIDDEN,
        "--string",
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
    template = templates.registered.getbyname("fail-init")
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
    template = templates.registered.getbyname("fail-init")
    file = init_file(template.template)
    assert main(CHECK_CLASS, file.parent) == 1


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
    assert main(CHECK_PROTECTED, file.parent) == 1


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
    assert main(CHECK_OVERRIDDEN, file.parent) == 1


@pytest.mark.parametrize(
    ["_", TEMPLATE, "__"],
    templates.registered.getgroup("fail-dunder"),
    ids=templates.registered.getgroup("fail-dunder").getids(),
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
            "--summary",
            CHECK_CLASS,
            CHECK_PROTECTED,
            CHECK_OVERRIDDEN,
            CHECK_DUNDERS,
            file.parent,
        )
        == 1
    )
    out = nocolorcapsys.stdout()
    assert CHECK not in out
    assert CROSS not in out
    assert out.count(str(file)) == 1


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
            "--no-ansi",
            CHECK_CLASS,
            CHECK_PROTECTED,
            CHECK_OVERRIDDEN,
            CHECK_DUNDERS,
            file.parent,
        )
        == 1
    )
    assert "\x1b" not in capsys.readouterr()[0]
