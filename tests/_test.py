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
    ERR_GROUP,
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
    assert main(file.parent) == int(name.startswith("fail"))


@pytest.mark.parametrize(
    "template",
    templates.registered.filtergroup(MULTI),
    ids=[
        i.replace("-", "").upper()[4:8] if "e-1-0-" in i else i
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
    main(file.parent)
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
    "template",
    [i for i in templatest.templates.registered if i.name.endswith("1-sum")],
    ids=[
        i.replace("-", "").upper()[4:8] if "e-1-0-" in i else i
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
