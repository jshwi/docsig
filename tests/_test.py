"""
tests._test
===========
"""
# pylint: disable=protected-access
import pytest
import templatest
from templatest import Template, templates

import docsig.messages

from . import E101, E102, H101, H102, MULTI, InitFileFixtureType, MockMainType
from ._utils import NoColorCapsys


def test_print_version(
    monkeypatch: pytest.MonkeyPatch,
    main: MockMainType,
    nocolorcapsys: NoColorCapsys,
) -> None:
    """Test printing of version on commandline.

    :param monkeypatch: Mock patch environment and attributes.
    :param main: Patch package entry point.
    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    """
    monkeypatch.setattr("docsig._cli.__version__", "1.0.0")
    with pytest.raises(SystemExit):
        main("--version")

    assert nocolorcapsys.stdout().strip() == "1.0.0"


@pytest.mark.parametrize(
    "name,template,_",
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
    ids=templates.registered.filtergroup(MULTI).getids(),
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
        i.name
        for i in templatest.templates.registered
        if i.name.endswith("1-sum")
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
        i
        for i in dir(docsig.messages)
        if not i.startswith("__")
        and not getattr(docsig.messages, i) == template.expected
    ]
    main(file.parent)
    out = nocolorcapsys.readouterr()[0]
    assert template.expected in out
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
    report = docsig._report.Report("func")  # type: ignore
    report.append(E101)
    assert getattr(docsig.messages, E101) in report
    assert len(report) == 1
    report[0] = E102
    report.pop()
    assert E102 not in report


def test_message_sequence() -> None:
    """Test disabling of error messages.

    Assert that all following hints are disabled, until a new error
    message that has not been disabled is appended to the sequence.
    """
    msg_seq = docsig._report._MessageSequence(disable=[E101])  # type: ignore
    msg_seq.append(E101)
    msg_seq.append(H101)
    msg_seq.append(H102)
    assert getattr(docsig.messages, E101) not in msg_seq
    assert getattr(docsig.messages, H102) not in msg_seq
    assert getattr(docsig.messages, H102) not in msg_seq
    msg_seq.append(E102)
    msg_seq.append(H101)
    msg_seq.append(H102)
    assert getattr(docsig.messages, E102) in msg_seq
    assert getattr(docsig.messages, H101) in msg_seq
    assert getattr(docsig.messages, H102) in msg_seq
